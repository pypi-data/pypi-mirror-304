import filetype
import mimetypes
from contextlib import suppress
from flask import Request
from pathlib import Path
from tempfile import gettempdir
from typing import Final
from werkzeug.datastructures import FileStorage

from .env_pomes import APP_PREFIX, env_get_path

TEMP_FOLDER: Final[Path] = env_get_path(key=f"{APP_PREFIX}_TEMP_FOLDER",
                                        def_value=Path(gettempdir()))


def file_from_request(request: Request,
                      file_name: str = None,
                      file_seq: int = 0) -> bytes:
    """
    Retrieve and return the contents of the file returned in the response to a request.

    The file may be referred to by its name (*file_name*), or if no name is specified,
    by its sequence number (*file_seq*).

    :param request: the request
    :param file_name: optional name for the file
    :param file_seq: sequence number for the file, defaults to the first file
    :return: the contents retrieved from the file
    """
    # inicialize the return variable
    result: bytes | None = None

    count: int = len(request.files) \
                 if hasattr(request, "files") and request.files else 0
    # has a file been found ?
    if count > 0:
        # yes, retrieve it
        file: FileStorage | None = None
        if isinstance(file_name, str):
            file = request.files.get(file_name)
        elif (isinstance(file_seq, int) and
              len(request.files) > file_seq >= 0):
            file_in: str = list(request.files)[file_seq]
            file = request.files[file_in]

        if file:
            result: bytes = file.stream.read()

    return result


def file_get_data(file_data: Path | str | bytes,
                  max_len: int = None,
                  chunk_size: int = None) -> bytes:
    """
    Retrieve the data in *file_data*, or in a file in path *file_data*.

    The distinction is made with the parameter's type:
        - type *bytes*: *file_data* holds the data
        - type *Path* or *str*: *file_data* is a path to a file holding the data

    :param file_data: the data, or the path to locate the file containing the data
    :param max_len: optional maximum length of the data to return, or all data if not provided
    :param chunk_size: optional chunk size to use in reading the data, defaults to 128 KB
    :return: the data, or 'None' if the file data could not be obtained
    """
    # initialize the return variable
    result: bytes | None = None

    # normalize the maximum length parameter
    if isinstance(max_len, bool) or \
       not isinstance(max_len, int) or max_len < 0:
        max_len = 0

    # normalize the chunk size
    if isinstance(chunk_size, bool) or \
       not isinstance(chunk_size, int) or chunk_size <= 0:
        chunk_size = 128 * 1024

    # what is the argument type ?
    if isinstance(file_data, bytes):
        # argument is type 'bytes'
        result = file_data

    elif isinstance(file_data, Path | str):
        # argument is a file path
        file_bytes: bytearray = bytearray()
        file_path: Path = Path(file_data)
        # get the data
        with file_path.open(mode="rb") as f:
            buf_size: int = min(max_len, chunk_size) if max_len else chunk_size
            in_bytes: bytes = f.read(buf_size)
            while in_bytes:
                file_bytes += in_bytes
                if max_len:
                    if max_len <= len(file_bytes):
                        break
                    buf_size = min(max_len - len(file_bytes), chunk_size)
                else:
                    buf_size = chunk_size
                in_bytes = f.read(buf_size)
        result = bytes(file_bytes)

    if result and max_len and len(result) > max_len:
        result = result[:max_len]

    return result


def file_get_mimetype(file_data: Path | str | bytes) -> str:
    """
    Heuristics to determine the mimetype for *file_data*.

    The parameter *file_data* might be the data itself (type *bytes*), or a filepath (type *Path* or *str*).
    The heuristics used, as heuristics go, provide an educated guess, not an accurate result.

    :param file_data: file data, or the path to locate the file
    :return: the probable mimetype, or None if a determination was not possible
    """
    # initialize the return variable
    result: str | None = None

    # inspect the filepath
    if isinstance(file_data, Path | str):
        result, _ = mimetypes.guess_file_type(path=file_data)

    if not result:
        with suppress(TypeError):
            kind: filetype.Type = filetype.guess(obj=file_data)
            if kind:
                result = kind.mime

    return result


def file_is_binary(file_data: Path | str | bytes) -> bool:
    """
    Heuristics to determine whether the content of *file_data* is binary.

    The parameter *file_data* might be the data itself (type *bytes*), or a filepath (type *Path* or *str*).
    The heuristics used, as heuristics go, provide an educated guess, not an accurate result.
    Empty or null content is considered to be non-binary.

    :param file_data: file data, or the path to locate the file
    :return: 'True' if the determination resulted positive, 'False' otherwise
    """
    # obtain up to 1024 bytes of content for analysis
    chunk: bytes = file_get_data(file_data=file_data,
                                 max_len=1024) or b""
    # check for null byte
    result: bool = b'\0' in chunk
    # check for non-printable characters
    if not result:
        # remove the chars listed below - chars remaining indicates content is binary
        #    7: \a (bell)
        #    8: \b (backspace)
        #    9: \t (horizontal tab)
        #   10: \n (newline)
        #   12: \f (form feed)
        #   13: \r (carriage return)
        #   27: \x1b (escape)
        #   0x20 - 0x100, less 0x7f: 32-255 char range, less 127 (the DEL control char)
        text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        result = bool(chunk.translate(None, text_characters))

    return result
