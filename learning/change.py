from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import _thread

port = 8000
server_name = ''
server_address =(server_name, port) #use to identify the address of the server

''' HTTPServer is a socketServer.TCPServer subclass, and it implements the socket socketServer.BaseServer interface. It creates and
listens at the http socket, dispatching the requests to a handler. It stores the server address as instance variable name server_name and port. The server is accessible by the handler typically through the Handler's server instance variable'''

'''
BaseHTTPRequestHandler
this class handles the http request that arrives at the server. 
The method name is constructed from the request. For example, for the request method SPAM, the do_SPAM() method will be called with no arguments. All of the relevant information is stored in instance variables of the handler. Subclasses should not need to override or extend the __init__() method.
So the __init__() methods somehow initiates the the methods and calls them.
'''
def webHandlerProcedure(env):
	env.protocol_version = 'HTTP/1.1'
	env.parsePath()
	#env.cookieParser()
	
	#main(env)
	env.write("Hola Lubwimi")
	env.addHeaders("Content-Type", "text/html; char-encoding: ISO-8859-1")
	env.send_response(env.responseCode)
	for pair in env.responseHeaders:
		env.send_header(pair[0], pair[1])
	env.end_headers()
	responseMessage = bytes("sverige är sämst", "ISO-8859-1")
	env.wfile.write(responseMessage)
	'''if env.autosend:
		env.send_response(env.responseCode)#---
		for pair in env.responseHeaders:
			env.send_header(pair[0], pair[1])#---
		env.end_headers()#--
	
		for data in env.responseBuffer:
			dataClass = data.__class__
			if dataClass == str:
				outData = bytes(data,"UTF-8")
			elif dataClass == bytes:
				outData = data
			env.wfile.write(outData)#----
'''
class TheHttpHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        webHandlerProcedure(self)
    def do_POST(self):
        webHandlerProcedure(self)
    
    def __init__(self, request, client_address, server):
        self.responseCode = 200
        self.responseHeaders = []
        self.responseBuffer = list()
        self.autosend = False 
        super().__init__(request, client_address, server)
        
        
    def addHeaders(self, headerName, headerValue):
        self.responseHeaders.append((headerName, headerValue))
        
    def write(self, *args):
        for data in args:
            self.responseBuffer.append(data)
    
    def parsePath(self):
        splitList = self.path.split("?",1)
        pathPart  = splitList[0].split("/")
    '''Handles the http, that is parses the headers and override the post and get methods giving them the correct behavior '''
    
    
    '''
    What do you find in a request? In a request message we have:
    1) Request line. e.g. Get/images/logo.png HTTP/1.1--> the Get stuff, request something from the server
    2) Request header fields such as Accept-Language: en
    3) An empty line
    4)An optional message body
    
    what do you find in a response message? In a response message we have:
    1) a status-line, which include the status code and reason messsae. e.g. HTTP/1.1 200 ok
    2) Response header fields such as, Content-Type: text/html
    3) An empty line
    4) An optional message body
    '''
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Handle the request in a separate thread'''
    
def webHandlerThreadThunk():
	httpd = ThreadedHTTPServer(server_address, TheHttpHandler)
	httpd.serve_forever()


webHandlerThread = _thread.start_new_thread(webHandlerThreadThunk, ())