#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
import time

PORT_NUMBER = 8080
CONFIG_FILE = 'clean_response_config.json'

class CleanResponseServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.create_json_response('get')

    def do_PUT(self):
        self.create_json_response('put')

    def do_POST(self):
        self.create_json_response('post')

    def do_DELETE(self):
        self.create_json_response('delete')

    def set_response_headers(self, responseCode=200):
        self.send_response(responseCode)
        if responseCode == 204:
            self.send_header('Content-type', 'application/json; charset=utf-8')
        else:
            self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

    def default_response(self):
        return '{"error" : "url not found"}'

    def default_response_code(self):
        return 200

    def create_json_response(self, method):
        try:
            json_file = json.load(open(CONFIG_FILE))
            json_post_object = json_file[method]
            return_payload = self.default_response()
            return_code = self.default_response_code()
            search_path = urlparse(self.path).path

            time.sleep(0.2)

            if search_path in json_post_object:
                json_object = json_post_object[search_path]
                if "fileResponse" in json_object:
                    txt = open(json_object["fileResponse"])
                    return_payload = txt.read()
                elif "response" in json_object:
                    json_dictionary = json_object["response"]
                    return_payload = json.dumps(json_dictionary)
                if "responseCode" in json_object:
                    return_code = json_object["responseCode"]

            self.set_response_headers(responseCode=return_code)
            self.wfile.write(bytes(return_payload, 'utf-8'))

            print(f" [INFO] {method} {search_path}")
            print(f" [PAYLOAD] \n{return_payload}\n")

        except IOError:
            self.send_error(
                404, f' [FAIL] Path ({method}.{self.path}) not found in JSON')


if __name__ == "__main__":
    try:
        server = HTTPServer(('', PORT_NUMBER), CleanResponseServer)

        print(' [OK] Clean Response Server started...')
        print(f' [INFO] PORT: {PORT_NUMBER}')
        print(f' [INFO] Config file: {CONFIG_FILE}\n\n')
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
    server.socket.close()