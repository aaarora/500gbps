import logging
import socket

def checkSocket(*args) -> None:
  for url in set(args):
    hostname, port = url.split(":")
    sock = socket.socket()
    try:
      sock.connect((hostname, int(port)))
      logging.info("Succesfully contacted socket on port %s for %s", port, hostname)
      sock.close()
    except Exception as error:
      sock.close()
      logging.error("Error %s while connecting to socket for %s", error, url)
      return False
  return True
