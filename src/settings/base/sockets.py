# Problem:
# + ConnectionError or Connection reset by peer raised randomly in Dramatiq
#   workers.
# State:
# + Currently disabled, as we want to test if it wasn't temporary.
# Reason:
# + https://github.com/getsentry/sentry-python/issues/1198
# + https://github.com/psf/requests/issues/4937#issuecomment-788899804
# import socket
#
# from urllib3.connection import HTTPConnection
#
#
# HTTPConnection.default_socket_options = HTTPConnection.default_socket_options + [
#     (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
#     BELOW WON'T WORK ON OSX!
#     Make conditional check if the program is running on Linux?
#     (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
#     (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
#     (socket.SOL_TCP, socket.TCP_KEEPCNT, 6),
# ]
