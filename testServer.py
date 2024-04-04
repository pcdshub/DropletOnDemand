# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


hostName = "localhost"
serverPort = 8081
supportedJson = 'supported.json'


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        # Parse command
        parsePath = self.path.split('?')
        command = parsePath.pop(0)
        args = parsePath

        print(command, args)

        # Check if command exists
        fd = open(supportedJson)
        data = json.load(fd)
        capabilities = dict()
        for endpoint in data['endpoints']:
            capabilities[endpoint["API"]] = endpoint["payload"]

        fd.close()

        if command not in capabilities.keys():
            self.send_response(404)
            self.end_headers()
            return

        # Respond to client
        payLoad = capabilities[command];
        header = data['header']
        header['Result'] = payLoad

        # Response Json
        payLoad = json.dumps(header,ensure_ascii=False)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(payLoad, "utf-8"))



if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
