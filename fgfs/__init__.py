import xml.etree.ElementTree as ET
import socket
import threading


class UDP_Process(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.queue = conn
        UDP_IP = ""
        UDP_PORT = 34200

        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.running = 1

    def run(self):
        while self.running:
            #Reads the UDP packet splits then sends it to the Queue
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            data_test = data
            if (data_test):
                self.queue.put(data_test)
            else:
                pass

    def stop(self):
        self.running = 0

if __name__ == '__main__':
    import queue
    q = queue.Queue()
    t = UDP_Process(q)
    t.start()

    f = 'pyefis.xml'
    tree = ET.parse(f)

    Name_List = []
    Name_Value = []

    for node in tree.findall('.//name'):
        Name_List.append(node.text)

    for node in tree.findall('.//node'):
        Name_Value.append(node.text)

    while True:
        try:
            data_test = q.get(0)
            for data in data_test:
                if len(Name_List) == len(Name_Value):
                    for l, a, d in zip(Name_List, Name_Value, data_test):
                        print((l, a, d))
                else:
                    print(('Name value mismatch in :', f))
        except queue.Empty:
            pass
    t.join()
