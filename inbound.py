from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs
import sqlite3

hostName = "0.0.0.0"
serverPort = 8887
sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()
query = 'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, dtg int, state text, device text);'
cursor.execute(query)
query = 'CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY AUTOINCREMENT, device text, on int, off int, duration int);'
cursor.execute(query)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parse_result = urlparse(self.path)
        dict_result = parse_qs(parse_result.query)
        self.wfile.write(bytes("<html>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        if (parse_result.path=="/write"):
                query = "insert into readings(dtg, state, device) values ("+str(int(time.time()))+", '"+dict_result['state'][0]+"', '"+dict_result['device'][0]+"');"
                cursor.execute(query)
                sqliteConnection.commit()
                self.wfile.write(bytes(query, "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

