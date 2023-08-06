from github import Github
from github.GithubException import *
import tkinter as tk
from tkinter import messagebox
import requests
from EntryWithPlaceholder import EntryWithPlaceholder as EntryPlace
import sys
from PIL import ImageTk, Image

class FailedRetrievalException(Exception):
	pass

try:
	# g = Github(sys.argv[1])
	g = Github("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")
	g.get_user("rackodo") # If you fork or modify this repo, please keep this line the same to provide credit to me. -@rackodo
except IndexError:
	print("Please run this script again with your GitHub Access Token after the package name. Like this:")
	print("$ python py_github_gui ghp_ACCESSKEYHERE1234")
	exit()
except BadCredentialsException:
	print("Invalid GitHub Access Token")
	exit()

user = None
userAvatar = None

def updateName():
	result = user.name if user.name != None else ("@" + user.login.lower())

	profileRealName.configure(text=result)
	

def updateAvatar():
	avatarRaw = Image.open(requests.get(user.avatar_url, stream=True).raw).resize((150, 150), Image.LANCZOS)
	avatar = ImageTk.PhotoImage(avatarRaw)
	profilePicWrapper.configure(image = avatar)
	profilePicWrapper.image = avatar

def receiveUser():
	global user
	try:
		user = g.get_user(usernameEntry.get())
	except UnknownObjectException:
		messagebox.showerror("Error", "Not a GitHub Profile")

	updateName()
	updateAvatar()


win = tk.Tk()
win.title("Py Github GUI")
win.geometry('520x320')

main = tk.Frame(width=500, height=300)
main.pack(padx=10, pady=10)

# Left Column
left = tk.Frame(main)
left.place(x=0, y=0, anchor="nw", width=150, height=300)

profilePic = ImageTk.PhotoImage(Image.open("py_github_gui/placeholder.png").resize((150, 150), Image.LANCZOS))
profilePicWrapper = tk.Label(left, image = profilePic, width=150, height=150)
profileRealName = tk.Label(left, font=("Arial", 16), text="Waiting...")
infoButton = tk.Button(left, width=150, text="Get Information", command=receiveUser)
usernameEntry = EntryPlace(left, placeholder="GitHub Username")
usernameEntry.configure(width=150, justify=tk.CENTER)

profilePicWrapper.pack()
profileRealName.pack()
infoButton.pack(side=tk.BOTTOM)
usernameEntry.pack(side=tk.BOTTOM)

win.resizable(width=False, height=False)
win.mainloop()