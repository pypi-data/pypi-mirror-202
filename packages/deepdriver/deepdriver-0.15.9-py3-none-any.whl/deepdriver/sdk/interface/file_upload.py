import base64
import json
import os
import sys
from typing import IO, TYPE_CHECKING, Optional
import requests
import math
import logging
import contextlib
try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

class Progress:
    """A helper class for displaying progress."""



    def __init__(
        self, file: IO[bytes], iter_bytes: int ,callback: Optional["ProgressFn"] = None
    ) -> None:
        self.file = file
        self.file_name =file.name
        if callback is None:

            def callback_(new_bytes: int, total_bytes: int) -> None:
                pass

            callback = callback_

        self.callback: "ProgressFn" = callback
        self.bytes_read = 0
        self.chunk_num =0
        self.len = os.fstat(file.fileno()).st_size
        self.iter_bytes = iter_bytes
        self.total_chunk = math.ceil(self.len / self.iter_bytes)

    def read(self, size=-1):
        """Read bytes and call the callback."""
        bites = self.file.read(size)
        self.bytes_read += len(bites)
        if not bites and self.bytes_read < self.len:
            # Files shrinking during uploads causes request timeouts. Maybe
            # we could avoid those by updating the self.len in real-time, but
            # files getting truncated while uploading seems like something
            # that shouldn't really be happening anyway.
            print(
                "File {} size shrank from {} to {} while it was being uploaded.".format(
                    self.file.name, self.len, self.bytes_read
                )
            )
        # Growing files are also likely to be bad, but our code didn't break
        # on those in the past so it's riskier to make that an error now.
        self.callback(len(bites), self.bytes_read)
        base64_str =str( base64.b64encode(bites), encoding='utf-8')
        chunk_json = {
            "file_name" : self.file_name,
            "chunk": base64_str,
            "chunk_num": self.chunk_num,
            "chunk_size": len(bites),
            "total_size": self.len,
            "total_chunk":self.total_chunk
        }
        self.chunk_num = self.chunk_num + 1
        if len(bites)>0:
            return json.dumps(chunk_json).encode("utf-8")
        return ""

    def rewind(self) -> None:
        self.callback(-self.bytes_read, 0)
        self.bytes_read = 0
        self.file.seek(0)

    def __getattr__(self, name):
        """Fallback to the file object for attrs not defined here."""
        if hasattr(self.file, name):
            return getattr(self.file, name)
        else:
            raise AttributeError

    def __iter__(self):
        return self

    def __next__(self):
        bites = self.read(self.iter_bytes)
        if len(bites) == 0:
            raise StopIteration
        return bites

    def __len__(self):
        return self.len

    next = __next__