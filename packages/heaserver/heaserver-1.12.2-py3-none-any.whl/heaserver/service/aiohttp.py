"""
Utility classes and functions for working with aiohttp.
"""
import asyncio
from contextlib import AbstractContextManager
from multiprocessing.connection import Connection
from io import BytesIO
from aiohttp.streams import StreamReader
from aiohttp.web import StreamResponse, Request, HTTPError
from aiohttp.client import ClientSession
from aiohttp.typedefs import LooseHeaders
from typing import Protocol, AsyncIterator, BinaryIO
from heaobject.root import json_dumps
from heaobject.user import NONE_USER
from .oidcclaimhdrs import SUB
from .appproperty import HEA_COMPONENT
from contextlib import asynccontextmanager
import logging
import os
import platform
import time
from typing import ParamSpec, Callable

from yarl import URL

if platform.system() == 'Windows':
    try:
        import msvcrt
        from ctypes import windll, byref, wintypes, GetLastError, POINTER
        from ctypes.wintypes import HANDLE, BOOL

        LPDWORD = POINTER(wintypes.DWORD)
        PIPE_NOWAIT = wintypes.DWORD(0x00000001)
        ERROR_NO_DATA = 232


        class WindowsNonBlockingFD:
            """
            Won't need this anymore in Python 3.12, per https://docs.python.org/3.12/library/os.html#os.set_blocking.

            A wrapper for a file descriptor so that we can call:
                `<AdvancedFD>.read(number_of_bytes)` and
                `<AdvancedFD>.write(data_as_bytes)`

            It also makes the `read_fd` non blocking. When reading from a non-blocking
            pipe with no data it returns b"".

            Methods:
                write(data: bytes) -> None
                read(number_of_bytes: int) -> bytes
                rawfd() -> int
                close() -> None
            """

            def __init__(self, fd: int):
                self.fd = fd
                self.closed = False
                self.config_non_blocking()

            def __del__(self) -> None:
                """
                When this object is garbage collected close the fd
                """
                self.close()

            def close(self) -> None:
                """
                Closes the file descriptor.
                Note: it cannot be reopened and might raise an error if it is
                being used. You don't have to call this function. It is automatically
                called when this object is being garbage collected.
                """
                self.closed = True

            def write(self, data: bytes) -> None:
                """
                Writes a string of bytes to the file descriptor.
                Note: Must be bytes.
                """
                os.write(self.fd, data)

            def read(self, x: int) -> bytes | None:
                """
                Reads `x` bytes from the file descriptor.
                Note: `x` must be an int
                      Returns the bytes. Use `<bytes>.decode()` to convert it to a str
                """
                try:
                    res = os.read(self.fd, x)
                    logging.debug('Result is %s', res)
                    return res
                except OSError as error:
                    err_code = GetLastError()
                    # If the error code is `ERROR_NO_DATA`
                    if err_code == ERROR_NO_DATA:
                        # Return an empty string of bytes
                        logging.debug('Returning None')
                        return None
                    else:
                        logging.debug('Returning error')
                        # Otherwise raise the error
                        website = "https://learn.microsoft.com/en-us/windows/win32/" + \
                                  "debug/system-error-codes--0-499-"
                        raise OSError(
                            f'An exception occurred. Error code: {err_code} Look up the error code here: {website}')

            def config_non_blocking(self) -> bool:
                """
                Makes the file descriptor non blocking.
                Returns `True` if sucessfull, otherwise returns `False`
                """
                # https://stackoverflow.com/a/34504971/11106801
                SetNamedPipeHandleState = windll.kernel32.SetNamedPipeHandleState
                SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
                SetNamedPipeHandleState.restype = BOOL

                handle = msvcrt.get_osfhandle(self.fd)

                res = windll.kernel32.SetNamedPipeHandleState(handle,
                                                              byref(PIPE_NOWAIT), None,
                                                              None)
                logging.debug('config_non_blocking %s', res)
                return not (res == 0)

            def rawfd(self) -> int:
                """
                Returns the raw fd as an int.
                """
                return self.fd
    except ModuleNotFoundError:
        raise ModuleNotFoundError('Neither set_blocking nor msvcrt found; this module will not work')


CHUNK_SIZE = 16 * 1024


@asynccontextmanager
async def client_session(*args, **kwargs) -> AsyncIterator[ClientSession]:
    """
    Gets a new aiohttp ClientSession. The session's json_serialize parameter is set to heaobject.root.json_dumps,
    which unlike Python's native json serialization supports serializing timestamps. It supports any arguments that
    ClientSession's constructor supports.
    """
    session = ClientSession(json_serialize=json_dumps, *args, **kwargs)
    try:
        yield session
    finally:
        await session.close()


class ConnectionFileLikeObjectWrapper(AbstractContextManager):
    """
    Wraps a multiprocessing.connection.Connection object and provides file-like object methods.

    This class is a context manager, so it can be used in with statements.
    """

    def __init__(self, conn: Connection):
        """
        Creates a new ConnectionFileLikeObjectWrapper object, passing in the connection to wrap.

        :param conn: a multiprocessing.connection.Connection object (required).
        """
        if conn is None:
            raise ValueError('conn cannot be None')
        self.__conn = conn
        self.__buffer = BytesIO()

    def read(self, n=-1):
        """
        Reads up to n bytes. If n is not provided, or set to -1, reads until EOF and returns all read bytes.

        If the EOF was received and the internal buffer is empty, returns an empty bytes object.

        :param n: how many bytes to read, -1 for the whole stream.
        :return: the data.
        """
        if len(b := self.__buffer.read(n)) > 0:
            return b
        try:
            result = self.__conn.recv_bytes()
            if -1 < n < len(result):
                pos = self.__buffer.tell()
                self.__buffer.write(result[n:])
                self.__buffer.seek(pos)
                return result[:n]
            else:
                return result
        except EOFError:
            return b''

    def write(self, b):
        """
        Sends some bytes to the connection.

        :param b: some bytes (required).
        """
        self.__conn.send_bytes(b)

    def fileno(self) -> int:
        """
        Returns the integer file descriptor that is used by the connection.

        :return: the integer file descriptor.
        """
        return self.__conn.fileno()

    def close(self) -> None:
        """
        Closes the connection and any other resources associated with this object.
        """
        try:
            self.__buffer.close()
            self.__conn.close()
        finally:
            if not self.__conn.closed:
                try:
                    self.__conn.close()
                except OSError:
                    pass

    def __exit__(self, *exc_details):
        self.close()


class SupportsAsyncRead(Protocol):
    """
    Protocol with an async read() method and a close() method.
    """

    async def read(self, n=-1):
        """
        Reads up to n bytes. If n is not provided, or set to -1, reads until EOF and returns all read bytes.

        If the EOF was received and the internal buffer is empty, returns an empty bytes object.

        :param n: how many bytes to read, -1 for the whole stream.
        :return: the data.
        """
        pass

    def close(self):
        """
        Closes any resources associated with this object.
        """
        pass


class AsyncReader:
    """
    Wraps a bytes object in a simple reader with an asynchronous read method and a close method.
    """

    def __init__(self, b: bytes):
        """
        Creates a new AsyncReader, passing in a bytes object.

        :param b: bytes (required).
        """
        self.__b = BytesIO(b)

    async def read(self, n=-1):
        """
        Reads up to n bytes. If n is not provided, or set to -1, reads until EOF and returns all read bytes.

        If the EOF was received and the internal buffer is empty, returns an empty bytes object.

        :param n: how many bytes to read, -1 for the whole stream.
        :return: the data.
        """
        return self.__b.read(n)

    def close(self):
        """
        Closes any resources associated with this object.
        """
        self.__b.close()


class StreamReaderWrapper:
    """
    Wraps an aiohttp StreamReader in an asyncio StreamReader-like object with a read() method and a no-op close()
    method.
    """

    def __init__(self, reader: StreamReader):
        if reader is None:
            raise ValueError('reader cannot be None')
        self.__reader = reader

    async def read(self, n=-1):
        """
        Reads up to n bytes. If n is not provided, or set to -1, reads until EOF and returns all read bytes.

        If the EOF was received and the internal buffer is empty, returns an empty bytes object.

        :param n: how many bytes to read, -1 for the whole stream.
        :return: the data.
        """
        return await self.__reader.read(n)

    def close(self):
        pass


class StreamResponseFileLikeWrapper:
    """
    Wraps an aiohttp StreamResponse in a file-like object wrapper. The write() method must be called in a separate
    thread.
    """

    def __init__(self, resp: StreamResponse, loop: asyncio.AbstractEventLoop | None = None):
        if loop is not None:
            self.loop = loop
        else:
            self.loop = asyncio.get_running_loop()
        self.resp = resp
        self.__logger = logging.getLogger(__name__)
        read_fd, write_fd = os.pipe()
        self.__logger.debug('File handles %d and %d', read_fd, write_fd)
        self.__writer = os.fdopen(write_fd, 'wb')
        # https://stackoverflow.com/questions/34504970/non-blocking-read-on-os-pipe-on-windows
        if hasattr(os, 'set_blocking'):
            os.set_blocking(read_fd, False)  # type:ignore  # not available on Windows
            self.__reader: BinaryIO | WindowsNonBlockingFD = os.fdopen(read_fd, 'rb')
        elif platform.system() == 'Windows':
            self.__logger.debug('On Windows')
            self.__reader = WindowsNonBlockingFD(read_fd)


        self.__task = self.loop.create_task(self.__pump_bytes_into_fd())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def write(self, data: bytes) -> int:
        """
        Writes to the StreamResponse and returns how many bytes were written.

        :param data: the bytes to write (required).
        :return: the number of bytes written.
        """
        self.__logger.debug('Writing %s', data)
        return self.__writer.write(data)

    def flush(self):
        """
        Flush the write buffers of the stream if applicable.
        """
        self.__writer.flush()

    async def close(self):
        """
        Cleans up all resources in this file-like object.
        """
        self.__logger.debug('Closing')
        try:
            self.__writer.close()
        finally:
            await self.__task
        self.__logger.debug('Task done')
        self.__logger.debug('Closed')

    async def __pump_bytes_into_fd(self):
        try:
            self.__logger.debug('About to write')
            while True:
                effective_log_level = self.__logger.getEffectiveLevel()
                while (chunk := await self.loop.run_in_executor(None, self.__reader.read, CHUNK_SIZE)) != b'':
                    if chunk is None:
                        self.__logger.debug('Did not get anything; will busy wait and try again')
                        await asyncio.sleep(0.1)
                        self.__logger.debug('Trying again')
                        continue
                    if effective_log_level == logging.DEBUG:
                        self.__logger.debug('Read %d bytes from download', len(chunk))
                    await self.resp.write(chunk)
                    if effective_log_level == logging.DEBUG:
                        self.__logger.debug('Wrote %d bytes to stream writer', len(chunk))
                break
            self.__logger.debug('Done reading file')
        finally:
            # Close the read end in the task. We need to close the write end in the parent.
            self.__reader.close()
        self.__logger.debug('Exiting task')


class RequestFileLikeWrapper:
    """
    Wraps an aiohttp request's content in a file-like object with read() and close() functions. Before doing any
    reading, call the initialize() method. The read() method must be called in a separate thread.
    """

    def __init__(self, request: Request, loop: asyncio.AbstractEventLoop | None = None) -> None:
        """
        Creates the file-like object wrapper.

        :param request: the aiohttp request (required).
        :param loop: the current event loop. If None, it will use asyncio.get_running_loop().
        """
        if loop is not None:
            self.loop = loop
        else:
            self.loop = asyncio.get_running_loop()
        self.request = request
        self.__pump_task: asyncio.Task | None = None
        self.__reader: BinaryIO | None = None
        self.__writer: BinaryIO | None = None

    def initialize(self):
        """
        Creates resources needed for reading.
        """
        read_fd, write_fd = os.pipe()
        self.__pump_task = self.loop.create_task(self.__pump_bytes_into_fd())
        self.__reader = os.fdopen(read_fd, 'rb')
        self.__writer = os.fdopen(write_fd, 'wb')

    def read(self, n=-1, /) -> bytes:
        """
        Reads some bytes.

        :param n: the number of bytes to read (or -1 for everything).
        :return: the bytes that were read.
        """
        logger = logging.getLogger(__name__)
        logger.debug('Reading %s bytes', n)
        assert self.__reader is not None, 'Must call initialize() before calling read()'
        output = self.__reader.read(n)
        logger.debug('Read %s bytes', len(output))
        return output

    def close(self):
        """
        Cleans up all resources in this file-like object.
        """
        logger = logging.getLogger(__name__)
        logger.debug('Closing')
        try:
            if self.__writer is not None:
                self.__writer.close()
                self.__writer = None
            if self.__reader is not None:
                self.__reader.close()
                self.__reader = None
            while self.__pump_task is not None and not self.__pump_task.done():
                time.sleep(0.1)
            self.__pump_task = None
        except Exception as e:
            logger.exception('Failed to close pipe')
            if self.__reader is not None:
                try:
                    self.__reader.close()
                    self.__reader = None
                except:
                    pass
            try:
                while self.__pump_task is not None and not self.__pump_task.done():
                    time.sleep(0.1)
                self.__pump_task = None
            except:
                pass
            raise e

    async def __pump_bytes_into_fd(self):
        logger = logging.getLogger(__name__)
        writer_closed = False
        content_type = self.request.headers.get('Content-Type', '')
        try:
            if content_type.startswith('multipart/form-data'):
                logger.debug(f'Is multipart')
                mp_reader = await self.request.multipart()
                while True:
                    part = await mp_reader.next()
                    if part is None:
                        break
                    logger.debug("the part's headers %s" % part.headers)
                    while True:
                        chunk = await part.read_chunk(CHUNK_SIZE)
                        if not chunk or chunk == b'':
                            break
                        logger.debug('Read %d bytes from upload', len(chunk))
                        bytes_written = await self.loop.run_in_executor(None, self.__writer.write, chunk)
                        logger.debug('Wrote %d bytes to pipe', bytes_written)
            else:
                while not self.request.content.at_eof():
                    chunk = await self.request.content.read(CHUNK_SIZE)
                    logger.debug('Read %d bytes from upload', len(chunk))
                    bytes_written = await self.loop.run_in_executor(None, self.__writer.write, chunk)
                    logger.debug('Wrote %d bytes to pipe', bytes_written)
            self.__writer.close()
            writer_closed = True
            logger.debug('Done reading file')
        except Exception as e:
            logger.exception('Failed to read file')
            if not writer_closed:
                try:
                    self.__writer.close()
                except:
                    pass
                writer_closed = False
                raise e

def absolute_url_minus_base(request: Request, url: URL | str | None = None) -> str:
    """
    Removes the current service's base URL from the beginning of the provided URL. If no URL is provided, the request
    URL is used. If the provided URL is not prefixed with the service's base URL, the URL is returned unaltered.

    :param request: the HTTP request (required).
    :param url: optional URL.
    :return: the resulting URL.
    """
    if url is None:
        url_ = str(request.url)
    else:
        url_ = str(url)
    base_url = request.app[HEA_COMPONENT]
    if not url_.startswith(base_url):
        return url_
    else:
        return url_.removeprefix(base_url).lstrip('/')


P = ParamSpec('P')

def http_error_message(http_error: HTTPError, object_display_name: Callable[P, str], *args: P.args, **kwargs: P.kwargs) -> HTTPError:
    """
    If the HTTPError object has an empty body, it will try filling in the body with a message appropriate for the given
    status code for operations on desktop objects.

    :param http_error: the HTTPError (required). This object's body may be modified by this call if it is None or an
    empty byte array.
    :param object_display_name: a callable that generates a description of a desktop object for inclusion in an error
    message.
    :param args: positional arguments to pass to object_display_name.
    :param kwargs: keyword arguments to pass to object_display_name. The encoding keyword argument is reserved and will
    be used to set the encoding of the error message when encoded to bytes (the default is utf-8).
    :return: the updated HTTPError (the same object as the http_error argument).
    """
    encoding = kwargs.get('encoding')
    if encoding:
        encoding_ = str(encoding)
    else:
        encoding_ = 'utf-8'
    if not http_error.body:
        match http_error.status:
            case 403:
                http_error.body = f'Access to {object_display_name(*args, **kwargs)} is denied because you do not have sufficient permission for it'.encode(encoding=encoding_)
            case 404:
                http_error.body = f'{object_display_name(*args, **kwargs)} not found'.encode(encoding=encoding_)
    return http_error


def extract_sub(request: Request) -> str:
    """
    Extracts the current user (subject) from the request's OIDC_CLAIM_sub header.

    :param request: the HTTP request (required).
    :return: the user id, or system|none if the header has no value or is absent.
    """
    return request.headers.get(SUB, NONE_USER)
