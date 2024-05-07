
from http.client import HTTPConnection, HTTPResponse
import json

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

