
import sys, socket, select

SOCKET_LIST = []
NAME = []
def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 10000))
    server_socket.listen(2)
 
    SOCKET_LIST.append(server_socket)
    NAME.append("")
 
    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
			
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
                NAME.append("")
                
            else:
                try:
                    data = sock.recv(1000)
                    if data:
						temp = data.split()
						
						for i in range(len(SOCKET_LIST)):
							
							if SOCKET_LIST[i] == sock :
								if NAME[i] == "" :
									if temp[0] == "login":
										if len(temp) >2:
											sock.send("\rLogin command syntax invalid\n")
										else:
											NAME[i] = temp[1]
											sock.send ("\rYou are Logged in as %s\n" % NAME[i])
											broadcast(server_socket, sock, "\r[%s] logged in as %s\n" % (addr, NAME[i]))
									elif temp[0] == "send" or temp[0] == "sendall" or temp[0] == "list" :
										sock.send("\rPlease Log in First\n")
									else:
										sock.send("\rCommand unknown\n")
								else: 
									if temp[0] == "login":
										sock.send("\rYou have been Logged In\n")
									elif temp[0] == "send":
										if len(temp)<3:
											sock.send("\rSend command syntax invalid\n")
										else:
											pesan = ""
											for i in range(2, len(temp)):
												pesan += str(temp[i])
												if i != len(temp):
													pesan+=" "
											for i in range(len(SOCKET_LIST)):
												if SOCKET_LIST[i] == sock :
													pengirim = str(NAME[i])
													break
											for i in range(len(SOCKET_LIST)):
												if NAME[i] == temp[1]:
													SOCKET_LIST[i].send("\r" +pengirim +": "+pesan+"\n")
													break
										
												
									elif temp[0] == "sendall":
										if len(temp)<2:
											sock.send("\rSendall command syntax invalid\n")
										else:
											pesan = ""
											for i in range(1, len(temp)):
												pesan += str(temp[i])
												if i != len(temp):
													pesan+=" "
											for i in range(len(SOCKET_LIST)):
												if SOCKET_LIST[i] == sock :
													pengirim = str(NAME[i])
													break
											broadcast(server_socket, sock, "\r"+pengirim+": "+ pesan+"\n")
										
									elif temp[0] == "list" :
										if len(temp)>1:
											sock.send("\rList command syntax invalid\n")
										else:
											sock.send("\rList of logged in users:\n")
											for i in range (len(SOCKET_LIST)):
												if (NAME[i] != ""):
													sock.send("\r- %s \n" % str(NAME[i]))
									else:
										sock.send("\rCommand unknown\n")
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
def broadcast (server_socket, sock, message):
    for i in range(len(SOCKET_LIST)):
        if SOCKET_LIST[i] != server_socket and SOCKET_LIST[i] != sock and NAME[i]!="":
            try :
                SOCKET_LIST[i].send(message)
            except :
                SOCKET_LIST[i].close()
                if SOCKET_LIST[i] in SOCKET_LIST:
                    SOCKET_LIST.remove(SOCKET_LIST[i])
 
if __name__ == "__main__":

    sys.exit(chat_server())
