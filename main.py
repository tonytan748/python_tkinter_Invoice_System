#!/usr/bin/env python
#coding=utf-8


from smtplib import *
from Tkinter import *
import tkMessageBox
import string

import datas

FILEPATH=os.path.join(os.path.split(sys.argv[0])[0],'data')
FILENAME=os.path.join(FILEPATH,'invoice.db')

USER=os.path.join(FILEPATH,'user.txt')


class loginPage(object):

    def __init__(self, master, info='Invoice Management'):
        self.master = master
        self.mainlabel = Label(master, text=info, justify=CENTER)
        self.mainlabel.grid(row=0, columnspan=3)


        self.user = Label(master, text='username', borderwidth=2)
        self.user.grid(row=1, sticky=W)


        self.pwd = Label(master, text='password', borderwidth=2)
        self.pwd.grid(row=2, sticky=W)
		
		att=datas.getName()
		attn=[i['username'] for i in att]
		self.userEntry=ttk.Combobox(master)
		self.userEntry['values']=tuple(attn)
		self.userEntry.grid(row=1,column=1,columnspan=2)
		self.userEntry.focus_set()
		

        self.pwdEntry = Entry(master, show='*')
        self.pwdEntry.grid(row=2, column=1, columnspan=2)


        self.loginButton = Button(master, text='Login', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)


        self.clearButton = Button(master, text='Clear', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)


    def login(self):
        self.username = (self.userEntry.get().strip()).upper()
        self.passwd = self.pwdEntry.get().strip()
		a=datas.getName()
		attn=[i['username'] for i in a]
		if len(self.username) == 0 or len(self.passwd) == 0 or not self.username in attn:
			tkMessageBox.showwarning('please check your username')
			self.clear()
			self.userEntry.focus_set()
            return
		else:
			pw=[i['password'] for i in a if i['username'] == self.username]
			if not self.passwd == pw[0]:
				tkMessageBox.showwarning('please check your username')
				self.clear()
				self.userEntry.focus_set()
				return
				
        self.connect()


    def connect(self):
		self.username = (self.userEntry.get().strip()).upper()
        self.invoice = invoice(self.master,self.username)


    def clear(self):
        self.userEntry.delete(0, END)
        self.pwdEntry.delete(0, END)

class invoice(object):

    def __init__(self, master, user=''):
        self.user = user

        self.sp = Toplevel(master)

		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='').grid(row=0,column=0,sticky=W)
		

        self.sendToLabel = Label(self.sp, text='send to:')
        self.sendToLabel.grid()
        self.sendToEntry = Entry(self.sp)
        self.sendToEntry.grid(row=0, column=1)


        self.subjectLabel = Label(self.sp, text='subject:')
        self.subjectLabel.grid(row=1, column=0)
        self.subjectEntry = Entry(self.sp)
        self.subjectEntry.grid(row=1, column=1)


        self.fromToLabel = Label(self.sp, text='from to:')
        self.fromToLabel.grid(row=2, column=0)
        self.formToAdd = Label(self.sp, text=self.sender)
        self.formToAdd.grid(row=2, column=1)


        self.sendText = Text(self.sp)
        self.sendText.grid(row=3, column=0, columnspan=2)


        self.sendButton = Button(self.sp, text='send', command=self.sendMail)
        self.sendButton.grid(row=4, column=0)


        self.newButton = Button(self.sp, text='new mail', command=self.newMail)
        self.newButton.grid(row=4, column=1)


    def getMailInfo(self):
        self.sendToAdd = self.sendToEntry.get().strip()
        self.subjectInfo = self.subjectEntry.get().strip()
        self.sendTextInfo = self.sendText.get(1.0, END)


    def sendMail(self):
        self.getMailInfo()
        body = string.join(("From: %s" % self.sender, "To: %s" % self.sendToAdd, "Subject: %s" % self.subjectInfo, "", self.sendTextInfo), "\r\n")
        try:
            self.smtp.sendmail(self.sender, [self.sendToAdd], body)
        except Exception, e:
            tkMessageBox.showerr('发送失败', "%s" % e)
            return
        tkMessageBox.showinfo('提示', '邮件已发送成功！')


    def newMail(self):
        self.sendToEntry.delete(0, END)
        self.subjectEntry.delete(0, END)
        self.sendText.delete(1.0, END)


if __name__ == '__main__':


    root = Tk()
    root.title('简易发送邮件程序')


    myLogin = loginPage(root)


    #root.wait_window(myLogin.mySendMail.sp)
    mainloop()
