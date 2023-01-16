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
query = 'CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY AUTOINCREMENT, device text, onTime int, offTime int, duration int);'
cursor.execute(query)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parse_result = urlparse(self.path)
        dict_result = parse_qs(parse_result.query)
        self.wfile.write(bytes("<html>", "utf-8"))
        if (parse_result.path=="/write"):
                query = "insert into logs(dtg, state, device) values ("+str(int(time.time()))+", '"+dict_result['state'][0]+"', '"+dict_result['device'][0]+"');"
                cursor.execute(query)
                sqliteConnection.commit()
                if ( dict_result['state'][0]=="pumpOn" ):
                    query = "insert into readings(device, onTime) values ("+dict_result['device'][0]+"Pump, "+str(int(time.time()))+");"
                    cursor.execute(query)
                    sqliteConnection.commit()
                if ( dict_result['state'][0]=="floatOn" ):
                    query = "insert into readings(device, onTime) values ("+dict_result['device'][0]+"Float, "+str(int(time.time()))+");"
                    cursor.execute(query)
                    sqliteConnection.commit()

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

