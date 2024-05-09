from testServer import MyServer
from drops.DropsDriver import myClient
from multiprocessing import Process, Event 
from http.server import HTTPServer
import json
import time

def launch_web_server(event):
  hostName = "127.0.0.1"
  serverPort = 8081
  supportedJson = 'drops/supported.json'
  webServer = HTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))

  go_again = True
  while (go_again):
      webServer.handle_request()
      time.sleep(0.1)
      go_again = not event.is_set()

  webServer.server_close()
  print("Server stopped.")


class TestResponse:
  def test_get_status(self, capsys):
    ev = Event()
    proc = Process(target=launch_web_server, args=(ev,))
    proc.start()
    time.sleep(0.1)
    client = myClient(ip="127.0.0.1", port=8081, supported_json="drops/supported.json", reload=False)

    client.send("/DoD/get/Status")
    time.sleep(0.1)
    resp = client.get_response()
    print(f"got response {resp}")

    # # TODO(josue): this sucks so bad please fix it
    fd = open("drops/supported.json", "r")
    data = json.load(fd)
    expected_response = data["endpoints"][2]["payload"]

    client.send("/DoD/get/Status")  # TODO: this sucks, make the process die nicely wihtout another get request 
    # send kill signal to test server
    ev.set()
    proc.join()

    assert resp.RESULTS == expected_response
