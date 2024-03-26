import pytest 
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from testServer import MyServer


class TestResponse:
  def test_responses(self, capsys):
    hostName = "localhost"
    serverPort = 8081
    supportedJson = '../supported.json'

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    webServer.handle_request()

    webServer.server_close()
    print("Server stopped.")