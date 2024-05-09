import logging
import pprint
import argparse

from http.client import HTTPConnection
from multiprocessing import Queue, Semaphore
from drops.helpers.ServerResponse import ServerResponse
from drops.helpers.SupporEndsHandler import SupportedEndsHandler
from drops.helpers.HTTPTransceiver import HTTPTransceiver

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
  def __init__(self, ip, port, supported_json="supported.json", reload=True, queue=None, **kwargs):
    # dto pipelines
    self.__queue__ = Queue()
    self.__queue_ready__ = Semaphore(value=0)
    # configure connection object
    self.__IP__ = ip
    self.__PORT__ = port
    self.conn = HTTPConnection(host=self.__IP__, port=self.__PORT__)
    self.transceiver = HTTPTransceiver(self.conn, self.__queue__, self.__queue_ready__)
    # configuration persitence, updating
    self.supported_ends_handler = SupportedEndsHandler(supported_json,
                                                       self.conn)

    if (reload):
      self.supported_ends_handler.reload_all()

    logger.info(f"Connected to ip: {ip} port: {port}")
    # convinient member lambda for grabbing supported endpoitns
    self.supported_ends = lambda : self.supported_ends_handler.get_endpoints()
    pprint.pprint(self.supported_ends())

  def connect(self):
      """
        Required to send 'Do' requests
      """
      logger.info(f"Sending: /DoD/Connect")
      self.send("/DoD/Connect")
      return self.get_response()

  def disconnect(self):
      """
        The client can end the connection with access to ‘Do’ requests.
        Clicking the button ‘Disable API Control’ on the UI has the same effect.
      """
      logger.info(f"Sending: /DoD/Disconnect")
      self.send("/DoD/Disconnect")
      return self.get_response()

  def get_status(self):
      """
        Returns Robot Status
      """
      logger.info(f"Sending: /DoD/get/Status")
      self.send("/DoD/get/Status")
      return self.get_response()

  def move(self, position : str):
      """
        Moves the drive to a position taken from the list of 'PositionNames'
      """
      logger.info(f"Sending: /DoD/do/Move?PositionName={position}")
      self.send(f"/DoD/do/Move?PositionName={position}")
      return self.get_response()

  def get_position_names(self):
      """
        Returns the list of positions in DOD robot
      """
      logger.info(f"Sending: /DoD/get/PositionNames")
      self.send(f"/DoD/get/PositionNames")
      return self.get_response()

  def get_task_names(self):
      """
        Returns the list of tasks that are stored in the Robot by name
      """
      logger.info(f"Sending: /DoD/get/TaskNames")
      self.send(f"/DoD/get/TaskNames")
      return self.get_response()

  def get_current_positions(self):
      """
        Returns the name and properties of the last selected position,
        together with the real current position coordinates.
        (The drives can have been stepped away from the stored position or
         they include small dispenser related offsets.)
      """
      logger.info(f"Sending: /DoD/get/CurrentPosition")
      self.send(f"/DoD/get/TaskNames")
      return self.get_response()

  def execute_task(self, value : str):
      """
        Runs a task from the list of ‘TaskName’.
        This operation is safe in general.
        It simulates the analog action on the UI.
      """
      logger.info(f"Sending: DoD/do/ExecuteTask?TaskName={value}")
      self.send(f"DoD/do/ExecuteTask?TaskName={value}")
      return self.get_response()

  def auto_drop(self):
      """
        Runs the particular task that is linked to the UI button.
        Its name is ‘AutoDropDetection’. In principalm this endpoint is not needed.
        ‘ExecuteTask’ can be used instead.
      """
      logger.info(f"Sending: /DoD/do/AutoDrop")
      self.send(f"/DoD/do/AutoDrop")
      return self.get_response()

  def move_to_interaction_point(self):
      """
        The moving to the predefined position of the interaction point corresponds
        to the use of the endpoint ‘Move’. But only with this endpoint the UI
        elemts for the dispensers’ position adjustment become visible on the UI.
        The request simulates the button (beam simbol) on the UI.
      """

      logger.info(f"Sending: /DoD/do/InteractionPoint")
      self.send(f"/DoD/do/InteractionPoint")
      return self.get_response()

  def move_x(self, value : float):
      """
        The X drive can be sent to any coordinate (the value’s unit is µm)
        within the allowed range.

        NOTE: This does not include a Z move up to the safe height nor any
        other safety feature checking whether the move from the current position
        to the selected coordinate can lead to collision or breaking of a
        dispenser Tip.
      """

      logger.info(f"Sending: /DoD/do/MoveX?X={value}")
      self.send(f"/DoD/do/MoveX?X={value}")
      return self.get_response()

  '''
  send transmits a formatted HTTP GET request
  it will not check the validity of request
  it will persist result in a place that can be read... TODO: actually do this
  '''
  def send(self, endpoint):
      self.transceiver.send(endpoint)
      return

  '''
  Pops most recent response from response queue
  '''
  def get_response(self):
    return self.transceiver.get_response()


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
