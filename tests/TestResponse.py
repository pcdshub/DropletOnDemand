from testServer import MyServer
from drops.DropsDriver import myClient
from multiprocessing import Process, Event 
from http.server import HTTPServer


def launch_web_server(event):
  hostName = "localhost"
  serverPort = 8081
  supportedJson = 'drops/supported.json'
  webServer = HTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))

  while (not event.is_set()):
      webServer.handle_request()

  webServer.server_close()
  print("Server stopped.")


class TestResponse:
  def test_responses(self, capsys):
    ev = Event()
    proc = Process(target=launch_web_server, args=(ev,))
    proc.start()

    ev.set()
    proc.join()
