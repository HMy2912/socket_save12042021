# import all the required modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"

# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
		
# GUI class for the chat
class GUI:
	def signup(self):
		# signup window
		self.signup = Toplevel()
		# set the title
		self.signup.title("Sign up")
		self.signup.resizable(width = False, height = False)
		self.signup.configure(width = 400, height = 300)
			# create a Label
		self.pls = Label(self.signup, text = "Please sign up to continue", justify = CENTER, font = "Helvetica 14 bold")
		self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)
			# create a Label
		self.labelUsername = Label(self.signup, text = "Username: ", font = "Helvetica 12")
		self.labelUsername.place(relheight = 0.2, relx = 0.15, rely = 0.2)
		self.labelPassword = Label(self.signup, text = "Password: ", font = "Helvetica 12")
		self.labelPassword.place(relheight = 0.2, relx = 0.15, rely = 0.4)

			# create a entry box for # typing the message
		self.entryUsername = Entry(self.signup, font = "Helvetica 14")
		self.entryUsername.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.2)
		self.entryPassword = Entry(self.signup, font = "Helvetica 14", show = "*")
		self.entryPassword.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.4)
			
			# set the focus of the cursor
		self.entryUsername.focus()
		self.entryPassword.focus()
			
			# create a Continue Button # along with action
		self.continueBtn = Button(self.signup, text = "CONTINUE", font = "Helvetica 14 bold", 
			command = self.login)
		self.continueBtn.place(relx = 0.5, rely = 0.7, anchor = CENTER)

	def login(self):
		# login window
		self.login = Toplevel()
		# set the title
		self.login.title("Sign in")
		self.login.resizable(width = False, height = False)
		self.login.configure(width = 400, height = 300)
			# create a Label
		self.pls = Label(self.login, text = "Please login to continue", justify = CENTER, font = "Helvetica 14 bold")
		self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07)
			# create a Label
		self.labelUsername = Label(self.login, text = "Username: ", font = "Helvetica 12")
		self.labelUsername.place(relheight = 0.2, relx = 0.15, rely = 0.2)
		self.labelPassword = Label(self.login, text = "Password: ", font = "Helvetica 12")
		self.labelPassword.place(relheight = 0.2, relx = 0.15, rely = 0.4)

		global entryUsername
		global entryPassword
			# create a entry box for # typing the message
		self.entryUsername = Entry(self.login, font = "Helvetica 14")
		self.entryUsername.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.2)
		self.entryPassword = Entry(self.login, font = "Helvetica 14", show = "*")
		self.entryPassword.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.4)
			
			# set the focus of the cursor
		self.entryUsername.focus()
		self.entryPassword.focus()
			
			# create a Continue Button # along with action
		self.continueBtn = Button(self.login, text = "CONTINUE", font = "Helvetica 14 bold", 
			command = lambda : self.goAhead(self.entryUsername.get(), self.entryPassword.get()))
		self.continueBtn.place(relx = 0.5, rely = 0.7, anchor = CENTER)

	# constructor method
	def __init__(self):
		# chat window which is currently hidden
		self.Window = Tk()
		self.Window.withdraw()
		
		global accountWindow
		# login window
		self.accountWindow = Toplevel()
		# set the title
		self.accountWindow.title("Account")
		self.accountWindow.resizable(width = False, height = False)
		self.accountWindow.configure(width = 400, height = 300)

		# create a Label
		self.pls = Label(self.accountWindow, text = "Select your choice", justify = CENTER, font = "Helvetica 14 bold")
		self.pls.place(relx = 0.5, rely = 0.2, anchor = CENTER)
		
		# create a Continue Button # along with action
		self.signInBtn = Button(self.accountWindow, text = "SIGN IN", font = "Helvetica 14 bold", command = self.login)
		self.signInBtn.place(relx = 0.5, rely = 0.4, anchor = CENTER)

		self.signUpBtn = Button(self.accountWindow, text = "SIGN UP", font = "Helvetica 14 bold", command = self.signup)
		self.signUpBtn.place(relx = 0.5, rely = 0.6, anchor = CENTER)
		self.Window.mainloop()

	def goAhead(self, name, password):
		self.login.destroy()
		self.layout(name, password)

		# the thread to receive messages
		rcv = threading.Thread(target=self.receive)
		rcv.start()
		# client.send(name.encode(FORMAT))
		# client.send(password.encode(FORMAT))

	# The main layout of the chat
	def layout(self, name, password):
		self.name = name
		self.password = password

		# to show chat window
		self.Window.deiconify()
		self.Window.title("LIVE SCORE")
		self.Window.resizable(width = False, height = False)
		self.Window.configure(width = 870, height = 750, bg = "#17202A")
		self.labelHead = Label(self.Window, bg = "#17202A", fg = "#EAECEE", text = self.name, font = "Helvetica 13 bold", pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window, width = 450, bg = "#ABB2B9")
		
		self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
		
		self.textCons = Text(self.Window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5)
		
		self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)
		
		self.labelBottom = Label(self.Window, bg = "#ABB2B9", height = 50)
		
		self.labelBottom.place(relwidth = 1, rely = 0.825)
		
		self.entryMsg = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.00001, relx = 0.011)
		
		self.entryMsg.focus()
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,text = "SEND",font = "Helvetica 10 bold",width = 20,bg = "#ABB2B9",command = lambda : self.sendButton(self.entryMsg.get()))
		self.buttonMsg.place(relx = 0.77,rely = 0.00001,relheight = 0.06,relwidth = 0.22)
		self.textCons.config(cursor = "arrow")
		#
		self.quitBtn = Button(self.Window,text = "LIST ALL",font = "Helvetica 10 bold",width = 20,bg = "#ABB2B9",command = self.sendListAll)
		self.quitBtn.place(relx = 0.5, rely = 0.92, anchor = CENTER, relwidth=0.97)
		#
		self.listallBtn = Button(self.Window, text = "DISCONNECT", font = "Helvetica 10 bold",width = 20,bg = "#ABB2B9",command = self.Window.quit)
		self.listallBtn.place(relx = 0.5,rely = 0.97, anchor = CENTER, relwidth=0.97)
		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)
		
		# place the scroll bar	# into the gui window
		scrollbar.place(relheight = 1, relx = 0.974)
		scrollbar.config(command = self.textCons.yview)
		self.textCons.config(state = DISABLED)

	def sendListAll(self):
		client.send("LIST ALL".encode(FORMAT))
	# function to basically start the thread for sending messages
	def sendButton(self, msg):
		self.textCons.config(state = DISABLED)
		self.msg=msg
		# print(f"BTN {self.msg}")
		self.entryMsg.delete(0, END)
		snd= threading.Thread(target = self.sendMessage)
		snd.start()

	# function to receive messages
	def receive(self):
		while True:
			try:
				message = client.recv(1024).decode(FORMAT)
				
				if message == "USERNAME":
				 	client.send(self.name.encode(FORMAT))
				elif message == "PASSWORD":
				 	client.send(self.password.encode(FORMAT))
				else:
					# self.layout(name, password)
					self.textCons.config(state = NORMAL)
					self.textCons.insert(END, message + "\n")
						
					self.textCons.config(state = DISABLED)
					self.textCons.see(END)
			except:
				# an error will be printed on the command line or console if there's an error
				print(f"{DISCONNECT_MESSAGE}")
				client.send(DISCONNECT_MESSAGE.encode(FORMAT))
				client.close()
				break
		
	# function to send messages
	def sendMessage(self):
		self.textCons.config(state=DISABLED)
		try:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(FORMAT))	
			# print(message)
		except:
			print("UNABLE TO SEND\n")

# create a GUI class object
g = GUI()
client.send(DISCONNECT_MESSAGE.encode(FORMAT))