# + https://github.com/getsentry/sentry-python/issues/1198
# + https://github.com/psf/requests/issues/4937#issuecomment-788899804
import socket

from urllib3.connection import HTTPConnection


HTTPConnection.default_socket_options = HTTPConnection.default_socket_options + [
    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
    # BELOW WON'T WORK ON OSX!
    # Should we make a conditional check whether the program is running on Linux?
    # (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
    (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
    (socket.SOL_TCP, socket.TCP_KEEPCNT, 6),
]
