import sys
import socket
import re

class LoadBalancer(object):

        def __init__(self):
                self.host = None
                self.port = None
                self.EXIST_CONNS = {}
                self.MAX_RECV_SIZE = 13107200 #DONE put size to 100mb
                self.cliCount = 0

        def connectNode(self, deviceInformation):
                #Do some work on deviceInfo
                if deviceInformation == 1:
                        return '', 4723
                elif deviceInformation == 2:
                        return '192.168.0.111', 4723

        def createCookie(self):
                cookie_num = 'client'+str(self.cliCount)
                retStr = 'Set-Cookie: id='+str(cookie_num)
                self.cliCount+=1
                return retStr, cookie_num

        def sendCookie(self, conn, create_cookie):
                conn.sendall('HTTP/1.0 200 OK\r\n')
                conn.sendall(create_cookie)
                conn.sendall('\n')
                conn.sendall('Conection: close')
                conn.sendall('\n')
                conn.sendall("Content-Type: text/html\r\n\r\n")
                conn.sendall('\n')

        def cookiePresent(self, req_headers):
                temp = req_headers['Cookie'].split('=')[1]
                sess_id = temp.split(',')[0]
                serv_id = temp.split(',')[1]
                if sess_id not in self.EXIST_CONNS.keys():
                        create_cookie, cookie_num = self.createCookie()
                        self.EXIST_CONNS[cookie_num] = serv_id
                elif sess_id in self.EXIST_CONNS.keys():
                        print "[ROBUSTEST] Client exists"
                        create_cookie = ''
                return create_cookie

        def cookieAbsent(self, req_headers):
                create_cookie, cookie_num = self.createCookie()
                create_cookie = create_cookie+',serv_id=server1'
                self.EXIST_CONNS[cookie_num] = 'server1'
                return create_cookie
       
        def run(self):
                IN_SOCK=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                IN_SOCK.bind((self.host, self.port))
                IN_SOCK.listen(3)
                while True:
                        try:
                                conn, client_addr = IN_SOCK.accept()
                                data_client = conn.recv(self.MAX_RECV_SIZE)
                                req_headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", data_client))
                                if 'Cookie' in req_headers:
                                        create_cookie = self.cookiePresent(req_headers)
                                else:
                                        phOpt = int(raw_input("Enter phone type: "))
                                        create_cookie = self.cookieAbsent(req_headers)
                                if create_cookie != '':
                                        self.sendCookie(conn, create_cookie)
                                OUT_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                outHost, outPort = self.connectNode(phOpt)
                                OUT_SOCK.connect((outHost, outPort))
                                OUT_SOCK.send(data_client)
                                data_server = OUT_SOCK.recv(self.MAX_RECV_SIZE)
                                if(len(data_server)>0):
                                        conn.sendall(data_server)
                                conn.close()
                                OUT_SOCK.close()
                        except KeyboardInterrupt:
                                IN_SOCK.close()
                                print "[ROBUSTEST] Load balancer is shutting down..."
                                sys.exit(1)
                IN_SOCK.close()


if __name__ == "__main__":
   
        loadBalancer = LoadBalancer()
        loadBalancer.host = 'localhost'
        loadBalancer.port = 8085
        loadBalancer.run()
