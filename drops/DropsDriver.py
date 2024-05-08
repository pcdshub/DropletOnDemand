import logging
import pprint
import argparse

from http.client import HTTPConnection
from multiprocessing import Queue, Semaphore
from drops.helpers import ServerResponse, SupportedEndsHandler
from drops.helpers import send as h_send
from drops.helpers import get_response as h_get_response

logger = logging.getLogger(__name__)


def parse_arguments(obj):
  # arg parse and validation
  parser = argparse.ArgumentParser(
                    prog='DoDMiddleware',
                    description='allows users to interact with droplet on demand http api')

  group = parser.add_mutually_exclusive_group(required=True)  # only accept one of the following
  # get, trivial
  group.add_argument("-g", "--get", help="Call HTTP get on endpoint", type=str, choices=obj.supported_ends()['get'])
  # do
  group.add_argument("-m", "--move", help="move to enumerated position", type=str, choices=obj.supported_ends()['do']["/DoD/do/Move?PositionName={value}"])
  group.add_argument("-t", "--task", help='execute enumerated task', type=str, choices=obj.supported_ends()['do']["/DoD/do/ExecuteTask?TaskName={value}"])

  return parser.parse_args()


'''
Simple HTTP Client wrapper.
Takes ip and port on construction can send data on socket and print reply
Can be invoked via command line args or as orchestrated by higher level software
'''


class myClient:
  def __init__(self, ip, port, queue=None, **kwargs):
    self.__IP__ = ip
    self.__PORT__ = port
    self.__queue__ = Queue()
    self.__queue_ready__ = Semaphore(value=0)

    self.conn = HTTPConnection(host=self.__IP__, port=self.__PORT__)
    self.supported_ends_handler = SupportedEndsHandler('supported.json',
                                                        self.conn)

    logger.info(f"Connected to ip: {ip} port: {port}")
    self.supported_ends = lambda : self.supported_ends_handler.get_endpoints()
    pprint.pprint(self.supported_ends())

  '''
  send transmits a formatted HTTP GET request
  it will not check the validity of request
  it will persist result in a place that can be read... TODO: actually do this
  '''
  def send(self, endpoint):
      h_send(self.conn, self.__queue__, self.__queue_ready__, endpoint)
      return

  '''
  Pops most recent response from response queue
  '''
  def get_response(self):
    return h_get_response(self.__queue__, self.__queue_ready__)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  # init connection to client
  # client = myClient(ip="172.21.148.101", port=9999)
  client = myClient(ip="127.0.0.1", port=8081)
  # check validity of user specified arg
  args = parse_arguments(client)

  # transmit command
  client.send(args.get)
  x = client.get_response()
  print(x.RESULTS)
