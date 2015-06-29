import sys
import socket
import Tkinter
from Tkconstants import *
from threading import Thread

port = 25565
sock = [None] * 2

if sys.platform.startswith('win'):
    import winsound
    play = lambda: winsound.Beep(10000, 200)
else:
    play = lambda: None


def stop():
    if sock[0]:
        sock[0].send('Bye bye!')
        sock[0].close()
    else:
        pass
    root.destroy()
    sys.exit()

def wait():
    while True:
        input = sock[0].recv(4096)
        if not input:
            continue
        print " IN: ", input
        input = input.decode('utf8')
        chatlog.insert(END, '\nIN: ' + input)
        chatlog.see(END)
        play()


def send(event):
    text = entry.get()
    sock[0].send(text.encode('utf8'))
    play()
    chatlog.insert(END, u'\nMe: ' + text)
    chatlog.see(END)
    entry.delete(0, END)


def start():
    ip = ipdata.get()
    print ip
    print type(ip)
    if len(ip) == 0:
    # if True:
        listener = socket.socket()
        listener.bind(('', port))
        listener.listen(5)
        chatlog.insert(END, '\n' + 'Waiting for input connection...')
        sock[0], sock[1] = listener.accept()
        chatlog.insert(END, '\n' + 'Successfully connected: ' + 
                        str(sock[1]) + '\n')
        play()
        print sock[1]
    else:
        sock[0] = socket.socket()
        print sock[0]
        chatlog.insert(END, '\n' + 'Connecting to: ' + 
                        ip + ':' + str(port))
        sock[0].connect_ex((ip, port))
        chatlog.insert(END, '\n' + 'Successfully connected!' + '\n')
        play()
    M = Thread(target=wait)
    M.start()
    startbutton.config(state=DISABLED)


root = Tkinter.Tk()
upperframe = Tkinter.Frame(root)
upperframe.pack()
chatlog = Tkinter.Text(upperframe, font='Arial 13')
chatlog.pack(side=LEFT, fill=Y)
scrollbar = Tkinter.Scrollbar(upperframe)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=chatlog.yview)
chatlog.config(yscrollcommand=scrollbar.set)
lowerframe = Tkinter.Frame(root)
lowerframe.pack()
Tkinter.Label(lowerframe, text='IP:').pack(side=LEFT)
starter = lambda e=None: Thread(target=start).start()
ipdata = Tkinter.Entry(lowerframe)
ipdata.pack(side=LEFT)
ipdata.insert(END, 'vort3.ddns.net')
ipdata.bind('<Return>', starter)
startbutton  =  Tkinter.Button(lowerframe, text='Start', command=starter)
startbutton.pack(side=LEFT)
Tkinter.Label(lowerframe, text='MSG:').pack(side=LEFT)
entry = Tkinter.Entry(lowerframe, width=80)
entry.pack(side=LEFT)
entry.bind('<Return>', send)

root.protocol('WM_DELETE_WINDOW', stop)
root.title('Direct Chatting')
root.resizable(0, 0)
root.mainloop()
