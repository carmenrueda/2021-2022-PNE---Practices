import http.server
import socketserver
import termcolor

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print("GET received! Request line:")
        termcolor.cprint("  " + self.requestline, 'green')
        print("  Command: " + self.command)
        print("  Path: " + self.path)
        return

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
