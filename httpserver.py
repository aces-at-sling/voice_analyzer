from http.server import HTTPServer, BaseHTTPRequestHandler

class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        print('GET Method')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        print(content_length)
        post_data = self.rfile.read(content_length)
        self.wfile.write("Female_voice".encode("utf-8"))
        print(post_data)

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print('POST Method')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        print(content_length)
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # print(self.headers)
        with open("samples/sample.wav", "wb") as binary_file:
   
            # Write bytes to file
            binary_file.write(post_data)
        # self.wfile.write("Female_voice")
        # print(post_data)
    
def main():
    IP = '192.168.56.1'
    PORT = 8000
    server =HTTPServer((IP,PORT),helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()


