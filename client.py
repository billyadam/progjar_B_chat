
import sys, socket, select
 
def chat_client():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    try :
        s.connect(('localhost', 10000))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                data = sock.recv(1000)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
