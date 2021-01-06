# UDP-Chatroom-Server-And-Client
A UDP based chatroom that support high concurrency through multiprocessing

This program does not support Windows as the multiprocessing part is done by os.fork(), please change that part to fit your needs if necessary.


To run the programs, simply type:
 
**python3 server.py YOUR_IP YOUR_PORT**
<br>
**python3 client.py YOUR_IP YOUR_PORT**

for example, I will use

**python3 server.py 192.168.0.XXX 8888**

for testing

more functions will be included in the future
