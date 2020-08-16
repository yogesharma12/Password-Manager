from tkinter import *
import sqlite3
from tkinter import messagebox
import random
import pyperclip

root = Tk()
root.title("Password Manager")
root.geometry("900x400")

frame = Frame(root, bg="#80c1ff", bd=5)
frame.place(relx=0.50, rely=0.50, relwidth=0.98, relheight=0.45, anchor = "n")

conn = sqlite3.connect("passmanager.db")
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS 
					manager(app_name text,
							url text,
							email_id text,
							password text)
				""")
conn.commit()
conn.close()

def submit():
	conn = sqlite3.connect("passmanager.db")
	cursor = conn.cursor()

	if app_name.get()!="" and url.get()!="" and email_id.get()!="" and password!="":
		cursor.execute(""" INSERT INTO manager 
						VALUES(:app_name, :url, :email_id, :password)"""
						, {
							'app_name': app_name.get(),
							'url': url.get(),
							'email_id': email_id.get(),
							'password': password.get()
						}
						)
		conn.commit()
		conn.close()

		messagebox.showinfo("Information", "Record Added in Database!")

		# clear the text boxes
		app_name.delete(0, END)
		url.delete(0, END)
		email_id.delete(0, END)
		password.delete(0, END)
	else:
		messagebox.showinfo("Alert", "Please fill all details!")
		conn.close()

def query():
	conn = sqlite3.connect("passmanager.db")
	cursor = conn.cursor()

	cursor.execute("SELECT *, oid FROM manager")
	records = cursor.fetchall()

	p_records = ""
	for record in records:
		p_records += str(record[4])+ " " +str(record[0])+ " " +str(record[1])+ " " +str(record[2])+ " " +str(record[3])+ "\n"

	query_label['text'] = p_records
	conn.commit()
	conn.close()

def delete():
	conn = sqlite3.connect("passmanager.db")
	cursor = conn.cursor()

	t = delete_id.get()
	if(t!=""):
		cursor.execute("DELETE FROM MANAGER WHERE oid = "+ delete_id.get())
		delete_id.delete(0, END)
		messagebox.showinfo("Alert","Record %s Delete" %t)
	else:
		messagebox.showinfo("Alert", "Please enter record id to delete!")

	conn.commit()
	conn.close()

def Random():

	password.delete(0,END)

	p = passlen.get()
	n = int(p)
	alphanum = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()"
	random_pass = ""

	for i in range(0, n):
		random_pass = random_pass + random.choice(alphanum)

	password.insert(10,random_pass)
	pyperclip.copy(random_pass)


#create Text Boxes
app_name = Entry(root, width=30)
app_name.grid(row=0, column=1, padx=20)
url = Entry(root, width=30)
url.grid(row=1, column=1, padx=20)
email_id = Entry(root, width=30)
email_id.grid(row=2, column=1, padx=20)
password = Entry(root, width=30)
password.grid(row=3, column=1, padx=20)
passlen = Entry(root, width=5)
passlen.grid(row=3, column=5, padx=20)

delete_id = Entry(root, width=30)
delete_id.grid(row=6, column=1, padx=20)

#create Text Box Labels
app_name_label = Label(root, text = "Application Name:")
app_name_label.grid(row=0, column=0)
url_label = Label(root, text="URL:")
url_label.grid(row=1, column=0)
email_id_label = Label(root, text="Email Id:")
email_id_label.grid(row=2, column=0)
password_label = Label(root, text="Password:")
password_label.grid(row=3,column=0)
passlen_label = Label(root, text="Password length:")
passlen_label.grid(row=3,column=4)

#create Submit Button
submit_btn = Button(root, text = "Add Record", command = submit)
submit_btn.grid(row=5, column=0, pady=5, padx=15, ipadx=35)

#create Query Button
query_btn = Button(root, text = "Show Records", command = query)
query_btn.grid(row=5, column=1, pady=5, padx=5, ipadx=35)

#create Generate Button
gen_btn = Button(root, text = "Generate Password", command = Random)
gen_btn.grid(row=3, column=2, pady = 5, padx=10, ipadx=15)

#create Delete Button
delete_btn = Button(root, text = "Delete Record", command = delete)
delete_btn.grid(row=6, column=0, ipadx=30)

#create a label to show responses

global query_label
query_label = Label(frame, anchor="nw", justify="left")
query_label.place(relwidth=1, relheight=1)

def main():
	root.mainloop()

if __name__ == '__main__':
	main()
