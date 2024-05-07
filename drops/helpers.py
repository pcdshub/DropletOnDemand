
from http.client import HTTPConnection, HTTPResponse
from multiprocessing import Queue, Semaphore
import json
import logging

logger = logging.getLogger(__name__)

class ServerResponse:
    """
        Object for parsing incomming HTTPResponse from Robot
    """
    def __init__(self, httObj: HTTPResponse):
        response = json.loads(httObj.read())
        self.TIME = response["Time"]
        self.STATUS = response["Status"]
        self.LAST_ID = response["LastID"]
        self.ERROR_CODE = response["ErrorCode"]
        self.ERROR_MESSAGE = response["ErrorMessage"]
        self.RESULTS = response["Results"]


class SupportedEndsHandler:
    """
        Class ment to handle supported endpoints Json file.
            Reloads endpoints, keeps track of API args, and possible 'do' actions

            TODO: Write updates to JSON file?
    """
    def __init__(self, file : str, conn : HTTPConnection):
        self.file = file
        self.__queue__ = Queue()
        self.__queue_ready__ = Semaphore(value=0)
        self.__conn__ = conn
        self.supported_ends = {
          'get' : [],
          'do' : {},
          'conn' : []
        }
        self.reload_all()

    def get_endpoints(self):
        return self.supported_ends

    def reload_endpoint(self, endpoint : str):
        if endpoint in self.supported_ends['do'].keys():
            cursed = f"/DoD/get/{endpoint.split('?')[1].split('=')[0]}s"
            send(self.__conn__, self.__queue__, self.__queue_ready__, cursed)
            self.supported_ends['do'][endpoint] = get_response(self.__queue__,
                                                              self.__queue_ready__).RESULTS

    def reload_all(self):
        try:
          f = open(self.file)
        except FileNotFoundError:
          logger.error("File supported.json not found")

        with f:
          json_data = json.load(f)["endpoints"]
          self.supported_ends['get'] = [x['API'] for x in json_data if x['API'][5:8] == 'get']
          self.supported_ends['do'] = {x['API'] : None for x in json_data if x['API'][5:7] == 'do'}
          self.supported_ends['conn'] = [x['API'] for x in json_data if 'connect' in x['API'][5:].lower()]

        for ent in self.supported_ends['do'].keys():
          # check this do endpoint takes an argument
          if '?' in ent:
            # Any float is acceptable for pure moves
            if 'MoveX' in ent or 'MoveY' in ent or "MoveZ" in ent:
              continue
            # slightly evil but this queries for supported argument lists per do end point
            cursed = f"/DoD/get/{ent.split('?')[1].split('=')[0]}s"
            send(self.__conn__, self.__queue__, self.__queue_ready__, cursed)
            self.supported_ends['do'][ent] = get_response(self.__queue__,
                                                          self.__queue_ready__).RESULTS

'''
send transmits a formatted HTTP GET request
it will not check the validity of request
it will persist result in a place that can be read.
'''
def send(conn : HTTPConnection, queue : Queue, q_ready : Semaphore, endpoint : str):
    logger.info(f"attempting to send: {endpoint}...")

    conn.request("GET", endpoint)
    logger.info("issued request")
    reply = conn.getresponse()
    logger.info("got response")

    reply_obj = ServerResponse(reply)

    if (queue is not None):
      queue.put(reply_obj)
      q_ready.release()
    return

'''
Pops most recent response from response queue
'''
def get_response(queue : Queue, q_ready : Semaphore):
    q_ready.acquire()
    return queue.get()
