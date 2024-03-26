from http.client import HTTPSConnection
from multiprocessing import Queue

'''
Simple HTTP Client wrapper.
Takes ip and port on construction can send data on socket and print reply
'''

class myClient:
  def __init__(self, ip, port, queue = None):
    self.__IP__ = ip
    self.__PORT__ = port
    self.__queue__ = queue
    self.conn = http.client.HTTPSConnection(host=self.__IP__, port=self.__PORT__)

  def send(self, endpoint):
    self.conn.request("GET", endpoint)
    reply = self.con.get_response()
    if (self.__queue__ is not None):
      self.__queue__.put(reply)
    print(reply)

  def example_endpoint(example_endpoint_arg = non)