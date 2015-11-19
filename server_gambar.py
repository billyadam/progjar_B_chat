import sys
import socket
import io


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
sock.bind(server_address)
sock.listen(1)

print >>sys.stderr, 'starting up on %s port %s' % server_address


while True: 
    	connection, client_address = sock.accept()
        data = connection.recv(1000)
	nama = data.split()
	gambar=open("halo.jpg")
	if nama[1]=="/1":
		gambar= open("Kopaka.jpg")
	elif nama[1]=="/2":
		gambar=open("Pohatu.jpg")	
	elif nama[1]=="/3":
		gambar=open("lewa.jpg")
	elif nama[1]=="/4":
		gambar=open("Tahu.png")
	elif nama[1]=="/5":
		gambar=open("gali.jpg")
	isinyagambar =gambar.read()	
	gambar.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%isinyagambar

	connection.sendall(http_response)
	connection.close()
