import logging
import json
import pprint
import argparse

from http.client import HTTPConnection
from multiprocessing import Queue, Semaphore


def parse_arguments(obj):
  # arg parse and validation
  parser = argparse.ArgumentParser(
                    prog='DoDMiddleware',
                    description='allows users to interact with droplet on demand http api')

  group = parser.add_mutually_exclusive_group(required=True)  # only accept one of the following
  # get, trivial
  group.add_argument("-g", "--get", help="Call HTTP get on endpoint", type=str, choices=obj.supported_ends['get'])
  # do
  group.add_argument("-m", "--move", help="move to enumerated position", type=str, choices=obj.supported_ends['do']["/DoD/do/Move?PositionName={value}"])
  group.add_argument("-t", "--task", help='execute enumerated task', type=str, choices=obj.supported_ends['do']["/DoD/do/ExecuteTask?TaskName={value}"])

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

    self.enumerate_ends()  # expensive file io, do once in constructor. 

    self.conn = HTTPConnection(host=self.__IP__, port=self.__PORT__)
    logging.info(f"Connected to ip: {ip} port: {port}")

    self.enumerate_valid_dos()
  
  '''
  TODO: I would like these moved to an 'update fiducual' section, to be persisted in a source of truth json file
        the object can then decide to load the held fiducal list or generate a new one via these calls
  '''
  def enumerate_valid_dos(self):
    for ent in self.supported_ends['do'].keys():
      # check this do endpoint takes an argument
      if '?' in ent:
        # Any float is acceptable for pure moves
        if 'MoveX' in ent or 'MoveY' in ent or "MoveZ" in ent:
          continue
        # slightly evil but this queries for supported argument lists per do end point
        cursed = f"/DoD/get/{ent.split('?')[1].split('=')[0]}s"
        print(f"Cursed endpoint: {cursed}")
        self.send(cursed)
        self.supported_ends['do'][ent] = json.loads(self.get_response().read().decode('utf-8'))["Result"]  # i should be shot for this

    pprint.pprint(self.supported_ends)

  def enumerate_ends(self):
    self.supported_ends = {
      'get' : [],
      'do' : {},
      'conn' : []
    }
    # attempt to ingest supported.json which enumerates API end points
    try:
      f = open('supported.json')
    except FileNotFoundError:
      logging.error("File supported.json not found")
    with f:
      json_data = json.load(f)["endpoints"]
      self.supported_ends['get'] = [x['API'] for x in json_data if x['API'][5:8] == 'get']
      self.supported_ends['do'] = {x['API'] : None for x in json_data if x['API'][5:7] == 'do'}
      self.supported_ends['conn'] = [x['API'] for x in json_data if 'connect' in x['API'][5:].lower()]

    pprint.pprint(self.supported_ends)

  '''
  send transmits a formatted HTTP GET request
  it will not check the validity of request
  it will persist result in a place that can be read... TODO: actually do this
  '''
  def send(self, endpoint):
    logging.info(f"attempting to send: {endpoint}...")
    self.conn.request("GET", endpoint)
    logging.info("issued request")
    reply = self.conn.getresponse()
    logging.info("got response")

    if (self.__queue__ is not None):
      self.__queue__.put(reply)
      self.__queue_ready__.release()
    return

  '''
  Pops most recent response from response queue
  '''
  def get_response(self):
    self.__queue_ready__.acquire()
    print("NOOO BLOCK")
    return self.__queue__.get()


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  # init connection to client
  # client = myClient(ip="172.21.148.101", port=9999)
  client = myClient(ip="127.0.0.1", port=8081)
  # check validity of user specified arg
  args = parse_arguments(client)
  # transmit command
  x = client.send(args.get)
  print(x.read())
