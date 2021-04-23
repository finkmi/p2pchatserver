# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 14:21:18 2021

@author: mfink
"""

import socket
import threading
import queue
import time
from tkinter import *

PORT = 1114
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

class GUI:
    def __init__(self, master, g_queue, io_queue):
        self.g_queue = g_queue
        self.io_queue = io_queue
        
        #Set up GUI Window
        self.master = master
        self.master.withdraw()
          
        # Login window
        self.login = Toplevel()
        self.login.title("Begin")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 500,
                             height = 300)
        # Create Label
        self.pls = Label(self.login, 
                       text = "Please select an option to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")

        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
          
        # Create "server" button
        self.srv = Button(self.login,
                         text = "Create", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.name_entry())
          
        self.srv.place(relx = 0.3,
                      rely = 0.55)
        
        # Create "client" button
        self.cli = Button(self.login,
                         text = "Join", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.get_conn_info())
          
        self.cli.place(relx = 0.5,
                      rely = 0.55)
        
        # self.Window.mainloop()
        
    def get_conn_info(self):
        self.login.destroy()
        
        # Connection window
        self.cli_connect = Toplevel()
        self.cli_connect.title("Connect")
        self.cli_connect.resizable(width = False, 
                              height = False)
        self.cli_connect.configure(width = 500,
                              height = 300)
        
        # IP Label
        self.ip_label = Label(self.cli_connect,
                                text = "IP Address: ",
                                font = "Helvetica 12")
          
        self.ip_label.place(relheight = 0.2,
                              relx = 0.1, 
                              rely = 0.2)
          
        # IP Entry box
        self.ip_entry = Entry(self.cli_connect, 
                              font = "Helvetica 14")
          
        self.ip_entry.place(relwidth = 0.4, 
                              relheight = 0.12,
                              relx = 0.35,
                              rely = 0.2)
        
        # Port Label
        self.port_label = Label(self.cli_connect,
                                text = "Port #: ",
                                font = "Helvetica 12")
          
        self.port_label.place(relheight = 0.2,
                              relx = 0.1, 
                              rely = 0.4)
          
        # port Entry box
        self.port_entry = Entry(self.cli_connect, 
                              font = "Helvetica 14")
          
        self.port_entry.place(relwidth = 0.4, 
                              relheight = 0.12,
                              relx = 0.35,
                              rely = 0.4)
        
        # Name Label
        self.name_label = Label(self.cli_connect,
                                text = "Name: ",
                                font = "Helvetica 12")
          
        self.name_label.place(relheight = 0.2,
                              relx = 0.1, 
                              rely = 0.6)
          
        # Name Entry box
        self.name_entry = Entry(self.cli_connect, 
                              font = "Helvetica 14")
          
        self.name_entry.place(relwidth = 0.4, 
                              relheight = 0.12,
                              relx = 0.35,
                              rely = 0.6)
        
        # Connect button
        self.conn_btn = Button(self.cli_connect,
                          text = "Connect", 
                          font = "Helvetica 14 bold", 
                          command = lambda: self.client(self.ip_entry.get(), self.port_entry.get(), self.name_entry.get()))
          
        self.conn_btn.place(relx = 0.3,
                      rely = 0.75)
          
        # set the focus of the curser
        self.ip_entry.focus()
        
        
    def name_entry(self):
        self.login.destroy()
        
        # Connection window
        self.name_window = Toplevel()
        self.name_window.title("Enter Name")
        self.name_window.resizable(width = False, 
                              height = False)
        self.name_window.configure(width = 500,
                              height = 300)
        
        # IP Label
        self.name_label = Label(self.name_window,
                                text = "Name: ",
                                font = "Helvetica 12")
          
        self.name_label.place(relheight = 0.2,
                              relx = 0.1, 
                              rely = 0.2)
          
        # IP Entry box
        self.name_entry = Entry(self.name_window, 
                              font = "Helvetica 14")
          
        self.name_entry.place(relwidth = 0.4, 
                              relheight = 0.12,
                              relx = 0.35,
                              rely = 0.2)
        
        # Create button
        self.conn_btn = Button(self.name_window,
                          text = "Start", 
                          font = "Helvetica 14 bold", 
                          command = lambda: self.server(self.name_entry.get()))
          
        self.conn_btn.place(relx = 0.3,
                      rely = 0.35)
          
        # set the focus of the curser
        self.name_entry.focus()
        
    def client(self, ip, port, name):
        self.name = name
        self.cli_connect.destroy()
        self.io_queue.put(f"[CLIENT] {ip} {port} {name}")
        self.chat_gui()
    
    def server(self, name):
        self.name = name
        self.name_window.destroy()
        self.io_queue.put(f"[SERVER] {name}")
        self.chat_gui()

        
    def chat_gui(self):
        self.master.deiconify()
        self.master.title("FinkChat")
        self.master.resizable(width = False,
                              height = False)
        self.master.configure(width = 470,
                              height = 550,)
        
        self.msgs = Text(self.master,
                             width = 20, 
                             height = 2,
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.msgs.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.master,
                                  height = 80)
          
        self.labelBottom.place(relwidth = 1,
                                rely = 0.825)
          
        self.msg_entry = Entry(self.labelBottom,
                              font = "Helvetica 13")
          
        self.msg_entry.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.msg_entry.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                command = lambda :self.send_msg(self.msg_entry.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        # Create a scroll bar
        scrollbar = Scrollbar(self.msgs)
        scrollbar.place(relheight = 1,
                        relx = 0.974)          
        scrollbar.config(command = self.msgs.yview)
        
        self.msgs.config(state = DISABLED)

        # self.master.update() 
        
    def send_msg(self, msg):
        self.msgs.config(state = DISABLED)
        self.msg_entry.delete(0, END)
        self.io_queue.put(msg)
        self.g_queue.put(self.name + ': ' + msg + '\n')
        
    def check_queue(self):
        while self.g_queue.qsize():
            try:
                msg = self.g_queue.get(0)
                # insert messages to text box
                self.msgs.config(state = NORMAL)
                self.msgs.insert(END, msg)
                self.msgs.config(state = DISABLED)
                self.msgs.see(END)
            except queue.Empty:
                pass
        
class Socket:
    def __init__(self, master):
        self.master = master
        
        #Create queue
        self.g_queue = queue.Queue()
        self.io_queue = queue.Queue()
        
        #Create GUI
        self.gui = GUI(self.master, self.g_queue, self.io_queue)

        self.running = True
        self.work_thread = threading.Thread(target=self.check_queue)
        self.work_thread.start()
        self.gui_work()
        
    def gui_work(self):
        self.gui.check_queue()
        self.master.after(250, self.gui_work)
        
    def check_queue(self):
        while self.running:
            while self.io_queue.qsize():
                try:
                    msg = self.io_queue.get(0)
                    self.parse_message(msg)
                except queue.Empty:
                    pass
                
    def parse_message(self, msg):
        if msg.startswith('[SERVER]'):
            self.isServer = True
            self.name = msg.split()[1]
            self.start_server()
        elif msg.startswith('[CLIENT]'):
            self.isServer = False
            tokenized = msg.split()
            self.name = tokenized[3]
            self.client_connect(tokenized[1], tokenized[2])
        else:
            # Server sends using socket object returned from accept()
            if self.isServer:
                self.send_thread = threading.Thread(target=self.send, args=(self.conn, msg))
                self.send_thread.start()
            # Client sends using socket object returned from socket.socket()
            else:
                self.send_thread = threading.Thread(target=self.send, args=(self.server, msg))
                self.send_thread.start()
            
    def start_server(self):
        # Create a new socket for the server and bind server addr to socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)
        
        # Print message to console and to user
        print('Server running on ' + str(ADDRESS[0]) + ':' + str(ADDRESS[1]))
        self.g_queue.put('Server running on ' + str(ADDRESS[0]) + ':' + str(ADDRESS[1]) + '\n')
        
        # Begin listening for client
        self.server.listen(1)
        self.conn, addr = self.server.accept()
        
        #Once client connects start a recieving thread
        self.recv_thread = threading.Thread(target=self.receive, args=[self.conn])
        self.recv_thread.start()
        self.g_queue.put('Client connected!\n')
        
    def client_connect(self, ip, port):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((ip, int(port)))
            self.g_queue.put('Connected to ' + str(ip) + ':' + str(port) + '\n')
            self.recv_thread = threading.Thread(target=self.receive, args=[self.server])
            self.recv_thread.start()
        except Exception:
            self.g_queue.put('Could not connect please try again later.\n')
            print('Could not connect please try again later.')
            
                
    def send(self, conn, message):
        conn.send((self.name + ': ' + message + '\n').encode("utf-8"))
    
    
    def receive(self, conn):
        while self.running:
            message = conn.recv(4096)
            self.g_queue.put(message)
            

root = Tk()
client = Socket(root)
root.mainloop()
        