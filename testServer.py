# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

hostName = "localhost"
serverPort = 8081
capabilities = dict()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self): 

        try:
            payLoad = capabilities[self.path];
        except:
            self.send_response(404)

        self.send_response(200)
        self.wfile.write(bytes(payLoad, "utf-8"))



if __name__ == "__main__":        

    fd = open('supported.json')
    data = json.load(fd)
    for endpoint in data['endpoints']:
        capabilities[endpoint["API"]] = endpoint["payload"]
    fd.close()

    print(capabilities)

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
