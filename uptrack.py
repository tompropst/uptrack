# Copyright Thomas Propst 2017

import time
import BaseHTTPServer

# Set HOST to a valid address to limit to a specific interface.
# Leave empty for all interfaces, wired, wireless, localhost, etc.
# HOST = "192.168.0.1" 
HOST = ""
# Set the port you want to listen on. Standard ports such as 80 may require
# elevated privileges.
PORT = 8000
# Provide a unique and obscure path to avoid logging web scanners.
# A method might be to use a hash of the server name. e.g.:
# $ echo -n example.com | md5sum
# PATH = "/5ababd603b22780302dd8d83498e5172"
PATH = "/test"
# Clients to be tracked should connect to:
# http://<HOST>:<PORT>/<PATH>

# Specify an accessible path for the log file (CSV format).
LOG_PATH = "uptrack.log"

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"

# Subclass the BaseHTTPServer request handler and define a request handler for
# any type of supported request. Each handler has the pattern 'do_TYPE'.
# See the docs for detail on class variables:
# https://docs.python.org/2/library/basehttpserver.html
class httpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><head><title>uptrack</title></head>")
		s.wfile.write("<body><p>uptrack: ")
		# The client_address is a tuple: (IP, port)
		fileString = s.client_address[0] + "," + time.strftime(TIME_FORMAT)
		if s.path == PATH:
			s.wfile.write("recorded")
			trackClient(fileString)
		else:
			s.wfile.write("ignored")
		s.wfile.write("</br>")
		s.wfile.write(fileString)
		s.wfile.write("</p></body></html>")

def trackClient(fileString):
	with open(LOG_PATH, 'a') as f:
		f.write(fileString + '\n')
	return fileString

if __name__ == '__main__':
	server = BaseHTTPServer.HTTPServer
	httpd = server((HOST, PORT), httpHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST, PORT)
