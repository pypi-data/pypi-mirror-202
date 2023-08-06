from __future__ import annotations

from logging.handlers import SocketHandler


class RawTCPHandler(SocketHandler):
    def emit(self, record):
        try:
            self.send((self.format(record)).encode())
        except Exception:
            self.handleError(record)
