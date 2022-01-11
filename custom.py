from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi





tasklist = ['Task 1', 'Task 2', 'Task 3']

#creating a class which will handle the request using basehhtprequesthandler
class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/tasklist'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            

            output = '' 
            output += '<html><body>'
            output += '<h1> Here are the tasks assigned</h1>'
            output += '<h3><a href="/tasklist/new">Add New Task here</a></h3>'
            for task in tasklist:
                output += task
                output += '</br>'
                output += '</body></html>'
            self.wfile.write(output.encode())

        
        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = '' 
            output += '<html><body>'
            output += '<h1> Add New Tasks </h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="task" type="text" placeholder="Add New task">'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())


    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile,pdict)
                new_task = fields.get('task')
                tasklist.append(new_task[0])


            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()
                  


def main():
    PORT = 9000
    server = HTTPServer(('', PORT), requestHandler)
    print('Server is running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()