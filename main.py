from http.server import BaseHTTPRequestHandler,HTTPServer
import logging
import requests
import os

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel("ERROR")

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET(body=False)
    
    def do_GET(self, body=True):
        sent = False
        try:
            resp = None
            try:
                hostname = '200.232.172.61:8888'
                url = 'http://{}{}'.format(hostname, self.path)
                logger.debug(f"forward {self.path} to {url}")

                resp = requests.get(url, headers=self.headers, verify=False)
                self.send_response(resp.status_code)

                for header in resp.headers:
                    self.send_header(header, resp.headers[header])
                self.end_headers()
                if body:
                    self.wfile.write(resp.content)
                sent = True
                return
            finally:
                pass
        except IOError as e:
            logger.error('error during proxy', exc_info=1)
            if not sent:
                self.send_error(404, 'error trying to proxy: {}'.format(str(e)))

if __name__ == '__main__':
    port = int(os.getenv("PORT") or 10000)
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()