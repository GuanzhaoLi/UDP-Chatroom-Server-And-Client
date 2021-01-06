# chatroom client

from socket import *
import sys
import os
import signal


def do_child(s, addr, name): # send
    while True:
        text = input('Talk: ')
        if text == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), addr)
            os.kill(os.getppid(), signal.SIGKILL) # kill parent process
            sys.exit(0)

        else: # continue chat
            msg = 'C %s %s'%(name,text)
            s.sendto(msg.encode(), addr)



def do_parent(s): # listen
    while True:
        msg, addr = s.recvfrom(1024)
        print(msg.decode() + '\nTalk: ',end= '')


def main():
    if len(sys.argv) != 3:
        print("argv error")
        return

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    while True:
        name = input("Please enter your id: ")
        msg = 'L '+ name
        print("try to send useranme")
        s.sendto(msg.encode(), ADDR)
        print("sended")
        data, addr = s.recvfrom(1024)
        print("recvfrom server")
        if data.decode() == 'OK':
            break
        else:
            print('already exist user id')

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    pid = os.fork()
    if pid<0:
        print("create process failed")
        return
    elif pid ==0:
        do_child(s, addr, name)
    else:
        do_parent(s)


if __name__ == '__main__':
    main()
