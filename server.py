# chatroom server

from socket import *
import sys
import os
import signal


def do_login(s, users, user_name, addr):

    for item in users: # check duplicate username
        if item == user_name or item == 'admin':
            s.sendto("FAIL BECAUSE DUP USER".encode(), addr)
            return
    s.sendto("OK".encode(), addr) # let client go ahead

    msg = "\nWelcome %s to chatroom" % user_name
    for user in users:
        s.sendto(msg.encode(), users[user])

    users[user_name] = addr # add cur client to book
    return


def do_chat(s, users, tmp):

    msg = "\n%-4s : %s"%(tmp[1], tmp[2])
    for user in users:
        if user != tmp[1]:
            s.sendto(msg.encode(), users[user])


def do_quit(s, users, name):
    del users[name]
    msg = "\n" + name + "quit chatroom"
    for user in users:
        s.sendto(msg.encode(), users[user])

    return


def do_child(s): # listen
    users = {}

    while True:
        msg, addr = s.recvfrom(1024)
        msg = msg.decode()
        tmp = msg.split(' ') # will get "L name"

        if tmp[0] == 'L':  # login
            do_login(s, users, tmp[1], addr)
        elif tmp[0] == 'C':  # chat
            do_chat(s, users, tmp)
        elif tmp[0] == 'Q':  # quit
            do_quit(s, users, tmp[1])


def do_parent(s, ADDR): # send system msg
    name = "C admin "
    while True:
        msg = input("admin: ")
        msg = name + msg
        s.sendto(msg.encode(), ADDR) # send to myself
    s.close()
    sys.exit()


def main():
    if len(sys.argv) != 3:
        print("argv error")
        return

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
   
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)


    pid = os.fork()
    if pid < 0:
        print("create process failed")
        return
    elif pid == 0:
        do_child(s)
    else:
        do_parent(s, ADDR)


if __name__ == "__main__":
    main()
