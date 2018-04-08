from sys import exit
from tkinter import *
from tkinter.colorchooser import *
from threading import Thread
from socket import *
import base64

color = "#000000"
bgColor = "#4dffff"
dataLen = 1000000

serverIP = ''
serverPort = ''
clientSocket = socket(AF_INET, SOCK_DGRAM)

#listens for messages
def listener():
	while(True):
		rawData, address = clientSocket.recvfrom(dataLen)
		#data=rawData.decode()
		data = base64.b64decode(rawData).decode('utf-8')
		message = data[:-7]
		textColor = data[-7:]
		listBox.insert(END, message)
		listBox.itemconfig(END, {'fg': textColor})
		listBox.see(END)
		
#sends messages
def chatter():
	print("world")

def connect(event = None):
	if username.get().strip():
		messageProtocol = "1:" + username.get()
		print(serverIP)
		clientSocket.sendto(base64.b64encode(messageProtocol.encode('utf-8')), (serverIP, serverPort))
		print(serverIP)
		signIn.destroy()
		
def close():
	exit(0)
	
def send(event=None):
	global color
	if message.get().strip():
		messageProtocol = "2:" + username.get() + ": " + message.get() + color
		clientSocket.sendto(base64.b64encode(messageProtocol.encode('utf-8')), (serverIP, serverPort))
		message.set("")
		messageEntry.focus()
		
        
def changeColor(event=None):
	global color
	color = askcolor()
	color = color[1]
	colorButton.config(bg = color)
	messageEntry.config(foreground = color)
	userLabel.config(foreground = color)
	messageEntry.focus()
	
def changeBackground(event=None):
	global bgColor
	bgColor = askcolor()
	bgColor = bgColor[1]
	chatBox.config(bg = bgColor)
	botFrame.config(bg = bgColor)
	userLabel.config(bg = bgColor)

if __name__ == "__main__":
	#login
	signIn = Tk()
	signIn.title("RWC Login")
	signIn.protocol("WM_DELETE_WINDOW", close)
	
	userLabel = Label(signIn, text = "Enter your username:  ")
	serveripLabel = Label(signIn, text = "Server IP Address: ") #prompts the user to enter the ip address of the communication server along with their nickname
	portLabel = Label(signin, text = "Server Port Number: ") #prompts user to enter port of server
	userLabel.grid(row=0, column=0)
	serveripLabel.grid(row=1,column=0)
	portLabel.grid(row=2, column=0)
	
	username = StringVar()
	serverip = StringVar()
	portnumber = StringVar()
	
	userEntry = Entry(signIn, textvariable=username)
	serverIPEntry = Entry(signIn, textvariable=serverip)
	portEntry = Entry(int(signIn, textvariable=portnumber))
	serverIPEntry.grid(row=0, column=1)
	userEntry.grid(row=0,column=1)
        #portEntry.grid(row=0,column=2)

	userEntry.bind("<Return>")
	serverIPEntry.bind("<Return>", connect)
        portEntry.bind("<Return>", connect)
	
	enterButton = Button(signIn, text="Sign In", command=connect)
	enterButton.grid(row=3, column=1)
	
	userEntry.focus()
	signIn.mainloop()
	
	#create chat box
	
	#start multi-thread
	threadListener = Thread(target = listener)
	threadChatter = Thread(target = chatter)
	
	chatBox = Tk()
	chatBox["bg"] = bgColor
	chatBox.title("RWC Chat")
	chatBox.protocol("WM_DELETE_WINDOW", close)

	#menubar
	menubar = Menu(chatBox)

	fileMenu = Menu(menubar, tearoff=0)
	fileMenu.add_command(label="Exit", command=close)
	menubar.add_cascade(label="File", menu=fileMenu)
        
	editMenu = Menu(menubar, tearoff=0)
	editMenu.add_command(label="Change Background Color", command=changeBackground)
	menubar.add_cascade(label="Edit", menu=editMenu)

	chatBox.config(menu=menubar)

	message = StringVar()
        #top frame
	topFrame = Frame(chatBox)
	topFrame.pack(fill=BOTH, expand=True, padx = 20, pady = 20)
	scrollBar = Scrollbar(topFrame, orient=VERTICAL)
	scrollBar.pack(side=RIGHT, fill=Y)
	listBox = Listbox(topFrame, yscrollcommand=scrollBar.set)
	listBox.pack(side=LEFT, expand=True, fill=BOTH)
	scrollBar.config(command=listBox.yview)
        #bot frame
	botFrame = Frame(chatBox, height = 1, bg = bgColor)
	botFrame.pack(fill=X, padx = 20)
	userLabel = Label(botFrame, text = "%s: " % username.get(), foreground=color, bg = bgColor)
	userLabel.pack(side=LEFT)
	
	messageEntry = Entry(botFrame, textvariable=message, foreground=color)
	messageEntry.bind("<Return>", send)

	sendButton = Button(botFrame, text="Send", command=send)
	sendButton.pack(side=RIGHT)

	colorButton = Button(botFrame, text=" ", command=changeColor, bg=color, width = 3)
	colorButton.pack(side=RIGHT, padx = 10)
	messageEntry.pack(expand=True, fill=BOTH)
		#spacer
	spacerFrame = Frame(chatBox)
	spacerFrame.pack(pady = 10)

	#chatBox.iconbitmap(r'C:\Users\ps592\ChatApp\ChatAppinProgress')
	
	threadListener.start()
	threadChatter.start()
	
	chatBox.mainloop()
