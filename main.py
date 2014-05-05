#!/usr/bin/env python
#coding=utf-8


from smtplib import *
from Tkinter import *
import ttk
import tkMessageBox
import string
import os
import datas

FILEPATH=os.path.join(os.path.split(sys.argv[0])[0],'data')
FILENAME=os.path.join(FILEPATH,'invoice.db')

USER=os.path.join(FILEPATH,'user.txt')

GET_PROJECT_LIST=datas.getProject()

class loginPage(object):

	def __init__(self, master, info='Invoice Management'):
		self.master = master
		self.mainlabel = Label(master, text=info, justify=CENTER)
		self.mainlabel.grid(row=0, columnspan=3)


		self.user = Label(master, text='username', borderwidth=2)
		self.user.grid(row=1, sticky=W)


		self.pwd = Label(master, text='password', borderwidth=2)
		self.pwd.grid(row=2, sticky=W)

#		att=datas.getName()
		attn=[i['username'] for i in datas.getName()]
		self.userEntry=ttk.Combobox(master)
		self.userEntry['values']=tuple(attn)
		self.userEntry.grid(row=1,column=1,columnspan=2)
		self.userEntry.focus_set()

		self.pwdEntry = Entry(master,show='*')
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

		self.mas = Toplevel(master)

		self.sp=Frame(self.mas)

		Label(self.sp,text='USER').grid(row=0,column=0,sticky=W)
		Label(self.sp,text='S/N').grid(row=0,column=3,sticky=W)
		Label(self.sp,text='INVOICE NO').grid(row=1,column=0,sticky=W)
		Label(self.sp,text='REV').grid(row=1,column=3,sticky=W)
		Label(self.sp,text='DATE').grid(row=1,column=6,sticky=W)
		Label(self.sp,text='PROGRESS STATUS').grid(row=1,column=8,sticky=W)

		Label(self.sp,text='PROJECT CODE').grid(row=2,column=0,sticky=W)
		Label(self.sp,text='PROJECT TITLE').grid(row=3,column=0,sticky=W)
		Label(self.sp,text='CLIENT NAME').grid(row=6,column=0,sticky=W)
		Label(self.sp,text='CLIENT CTTN').grid(row=8,column=0,sticky=W)

		Label(self.sp,text='QUOTATION DATE').grid(row=2,column=3,sticky=W)
		Label(self.sp,text='QUOTATION REF').grid(row=3,column=3,sticky=W)
		Label(self.sp,text='CLIENT PO NO').grid(row=4,column=3,sticky=W)
		Label(self.sp,text='CREDIT NOTE NO').grid(row=5,column=3,sticky=W)
		Label(self.sp,text='REV').grid(row=6,column=3,sticky=W)

		Label(self.sp,text='INVOICE AMOUNT(EXCL GST)').grid(row=2,column=6,sticky=W)
		Label(self.sp,text='CN AMOUNT(EXCL GST)').grid(row=3,column=6,sticky=W)
		Label(self.sp,text='RETENTION(%)').grid(row=4,column=6,sticky=W)
		Label(self.sp,text='RETENTION($)').grid(row=5,column=6,sticky=W)

		Label(self.sp,text='GROSS AMOUNT').grid(row=2,column=8,sticky=W)
		Label(self.sp,text='GST($)').grid(row=3,column=8,sticky=W)
		Label(self.sp,text='NET INVOICE AMOUNT($)').grid(row=4,column=8,sticky=W)
		Label(self.sp,text='REMARKS').grid(row=5,column=8,sticky=W)

		#=====USER NAME=====
		self.username=StringVar()
		Label(self.sp,textvariable=self.username).grid(row=0,column=1,sticky=W)
		self.username.set(self.user)
		#=====SN NO.=====
		self.sn=StringVar()
		Label(self.sp,textvariable=self.sn).grid(row=0,column=4,sticky=W)
		self.sn.set('')
		#=====INVOICE NO=====
		a1=datas.getData()
		print a1
		if a1:
			invoice_list=[i['invoice_no'] for i in a1]
		else:
			invoice_list=[]
		self.invoicelist=ttk.Combobox(self.sp)
		self.invoicelist['values']=tuple(invoice_list)
		self.invoicelist['width']=12
		self.invoicelist.bind('<<ComboboxSelected>>',self.getInvoiceDetail)
		self.invoicelist.grid(row=1,column=1,sticky=W)
		#=====INVOICE REV=====
		self.invoiceRev=ttk.Combobox(self.sp)
		self.invoiceRev.bind('<<ComboboxSelected>>',self.getInvoiceInfo)
		self.invoiceRev['width']=8
		self.invoiceRev.grid(row=1,column=4,sticky=W)

#		self.invoiceRev=Entry(self.sp).grid(row=1,column=4,sticky=W)
		#=====INVOICE DATE=====
		self.invoiceDate=Entry(self.sp).grid(row=1,column=7,sticky=W)
		#=====INVOICE STATUS=====
		a=['FINAL']
		a.extend(range(1,15))
		
		self.invoiceStatus=ttk.Combobox(self.sp)
		self.invoiceStatus['values']=tuple(a)
		self.invoiceStatus.grid(row=1,column=9,sticky=W)
		#=====PROJECT CODE=====
		project_code_list=[i[1] for i in GET_PROJECT_LIST]
		self.projectlist=ttk.Combobox(self.sp)
		self.projectlist['values']=tuple(project_code_list)
		self.projectlist['width']=12
		self.projectlist.bind('<<ComboboxSelected>>',self.getProjectDetail)
		self.projectlist.bind('<Return>',self.getProjectDetail)
		self.projectlist.grid(row=2,column=1,sticky=W)
		#=====PROJECT TITLE=====
		f1=Frame(self.sp)
		bary1=Scrollbar(f1)
		bary1.pack(side=RIGHT,fill=Y)
		self.projecttitle=Text(f1,width=27,height=1)
		self.projecttitle.pack(side=LEFT,fill=BOTH)
		bary1.config(command=self.projecttitle.yview)
		self.projecttitle.config(yscrollcommand=bary1.set)
		f1.grid(row=4,column=0,rowspan=2,columnspan=3,sticky=W)
		#=====CLIENT COMPANY=====
		fc=Frame(self.sp)
		baryc=Scrollbar(fc)
		baryc.pack(side=RIGHT,fill=Y)
		self.clientCompany=Text(fc,width=17,height=0.5)
		self.clientCompany.pack(side=LEFT,fill=BOTH)
		baryc.config(command=self.clientCompany.yview)
		self.clientCompany.config(yscrollcommand=baryc.set)
		fc.grid(row=6,column=1,rowspan=2,columnspan=2,sticky=W)
		
#		self.client_company=StringVar()
#		self.clientCompany=Entry(self.sp,textvariable=self.client_company,width=25).grid(row=5,column=1,columnspan=2,sticky=W)
		#=====CLIENT ATTN=====
		self.client_attn=StringVar()
		self.clientAttn=Entry(self.sp,textvariable=self.client_attn,width=25).grid(row=8,column=1,columnspan=2,sticky=W)
		#=====QUOTATION DATE=====
		self.quotationDate=Entry(self.sp).grid(row=2,column=4,sticky=W)
		#=====QUOTATION NO.=====
		self.quotation=Entry(self.sp).grid(row=3,column=4,sticky=W)
		#=====CLIENT PO NO=====
		self.clientPo=Entry(self.sp).grid(row=4,column=4,sticky=W)
		#=====CREDIT NOTE NO.=====
		self.creditNote=Entry(self.sp).grid(row=5,column=4,sticky=W)
		#=====REV=====
		self.rev=Entry(self.sp).grid(row=6,column=4,sticky=W)

		self.invoiceAmount=Entry(self.sp).grid(row=2,column=7,sticky=W)
		self.cnAmount=Entry(self.sp).grid(row=3,column=7,sticky=W)
		self.retentionPercent=Entry(self.sp).grid(row=4,column=7,sticky=W)
		self.retentionAmount=Entry(self.sp).grid(row=5,column=7,sticky=W)

		self.grossAmount=Entry(self.sp).grid(row=2,column=9,sticky=W)
		self.gst=Entry(self.sp).grid(row=3,column=9,sticky=W)
		self.netInvoiceAmount=Entry(self.sp).grid(row=4,column=9,sticky=W)
#=======remarks========		
		f2=Frame(self.sp)
		bary2=Scrollbar(f2)
		bary2.pack(side=RIGHT,fill=Y)
		self.remarks=Text(f2,width=15,height=5)
		bary2.config(command=self.remarks.yview)
		self.remarks.config(yscrollcommand=bary2.set)
		f2.grid(row=5,column=9,rowspan=2,columnspan=2,sticky=W)


#=======search bar=======
		self.search_invoice=Button(self.sp,text='SEARCH',command=self.searchInvoice).grid(row=1,column=2,sticky=W)
		self.search_project=Button(self.sp,text='SEARCH',command=self.searchProject).grid(row=2,column=2,sticky=W)

		self.sp.pack(side=TOP,fill=X)


		f3=Frame(self.mas)
		self.add=Button(f3,text='ADD',command=self.addInvoice).grid(row=0,column=0,sticky=W)
		self.edit=Button(f3,text='EDIT',command=self.editInvoice).grid(row=0,column=1,sticky=W)
		self.delete=Button(f3,text='DELETE',command=self.delInvoice).grid(row=0,column=2,sticky=W)
		self.clear=Button(f3,text='CLEAR',command=self.clearInvoice).grid(row=0,column=3,sticky=W)
		f3.pack(side=TOP,fill=X)

#=============INVOICE LIST================
		invoice_list=['','','','','','','','','','','','','','','','','','',]
		listbar=Frame(self.mas)

		bary3=Scrollbar(listbar)
		bary3.pack(side=RIGHT,fill=Y)
		barx3=Scrollbar(listbar,orient=HORIZONTAL)
		barx3.pack(side=BOTTOM,fill=X)

		self.invoiceList=ttk.Treeview(listbar,columns=invoice_list)
		self.invoiceList.column(column='#0',width=0,stretch=False)
		for i in range(len(invoice_list)):
			self.invoiceList.heading(i,text=invoice_list[i])
			self.invoiceList.column(i,width=100)
		self.invoiceList.column(1,width=100)
		self.invoiceList.bind('<<TreeviewSelect>>',self.getInvoiceItem)
		self.invoiceList.pack(side=LEFT,fill=BOTH)

		barx3.config(command=self.invoiceList.xview)
		bary3.config(command=self.invoiceList.yview)
		
		self.invoiceList.config(xscrollcommand=barx3.set,yscrollcommand=bary3.set)

		listbar.pack(fill=X)

#==============PAGES MANAGEMENT================


#===============================================
	def getInvoiceDetail(self):
		'''
			get selected invoice information
		'''
		if self.invoicelist.get():
			a=((self.invoicelist.get()).strip('')).upper()
			m=datas.getData()
			invoice_summary=[]
			for i in m:
				if i['invoice_no']==a:
					invoice_summary.append(i)
			if not invoice_summary:
				tkMessageBox.showinfo('Notice','Please check the invoice again.')
				return
			else:
				clearData()
				if len(invoice_summary)==1:
					invoice_no=invoice_summary['invoice_no']
					invoice_rev=invoice_summary['invoice_rev']
					self.invoiceRev.set(invoice_rev)
					getInvoice(invoice_no,invoice_rev)
				else:
					x=[i['invoice_rev'] for i in invoice_summary]
					self.invoiceRev['values']=tuple(x)


	def getInvoiceInfo(self):
		if self.invoicelist.get() and self.invoiceRev.get():
			invoice_no=(self.invoicelist.get()).strip()
			invoice_rev=(self.invoiceRev.get()).strip()
			getInvoice(invoice_no,invoice_rev)

	def getInvoice(self,invoice_no,invoice_rev):
		if invoice_no and invoice_rev:
			m=datas.getDate()
			for i in m:
				if i['invoice_no']==invoice_no and i['invoice_rev']==invoice_rev:
					self.invoiceDate.insert(0,i[3])
					self.invoiceStatus.insert(0,i[21])
					self.projectlist.insert(0,i[4])
					self.projecttitle.insert(END,i[5])
					self.clientCompany.insert(END,i[6])
					self.clientAttn.insert(0,i[7])
					self.quotationDate.insert(0,i[8])
					self.quotation.insert(0,i[9])
					self.clientPo.insert(0,i[10])
					self.creditNote.insert(0,i[11])
					self.rev.insert(0,i[12])
					self.invoiceAmount.insert(0,i[13])
					self.cnAmount.insert(0,i[14])
					self.retentionPercent.insert(0,i[15])
					self.retentionAmount.insert(0,i[16])
					self.grossAmount.insert(0,i[17])
					self.gst.insert(0,i[18])
					self.netInvoiceAmount.insert(0,i[19])
					self.remarks.insert(END,i[20])
			

	def getProjectDetail(self,event):
		'''
			select the project code, and show all information for this code.
		'''
		if self.projectlist.get():
			a=GET_PROJECT_LIST
			m=(self.projectlist.get().strip()).upper()
			x=[]
			for i in a:
				if m == i[1]:
					x.extend(i)
			if x:
				self.projecttitle.delete(1.0,END)
				self.clientCompany.delete(1.0,END)
				self.client_attn.set('')

				self.projecttitle.insert(END,x[7])
				self.clientCompany.insert(END,x[5])
				self.client_attn.set(x[6])
		else:
			self.projecttitle.delete(1.0,END)
			self.clientCompany.delete(1.0,END)
			self.client_attn.set('')

	def searchInvoice(self):
		pass

	def searchProject(self):
		pass

	def addInvoice(self):
		pass

	def editInvoice(self):
		pass

	def delInvoice(self):
		pass

	def clearInvoice(self):
		try:
			clearData()
			self.invoiceRev.delete(0,END)
			self.invoicelist.delete(0,END)
			self.sn.set('')
			tkMessageBox.showinfo('Notice','Clear success.')
		except Exception as e:
			tkMessageBox.showinfo('Notice',e)


	def getInvoiceItem(self):
		pass

	def clearData(self):
		self.invoiceDate.delete(0,END)
		self.invoiceStatus.delete(0,END)
		self.projectlist.delete(0,END)
		self.projecttitle.delete(1.0,END)
		self.clientCompany.delete(1.0,END)
		self.clientAttn.delete(0,END)
		self.quotationDate.delete(0,END)
		self.quotation.delete(0,END)
		self.clientPo.delete(0,END)
		self.creditNote.delete(0,END)
		self.rev.delete(0,END)
		self.invoiceAmount.delete(0,END)
		self.cnAmount.delete(0,END)
		self.retentionPercent.delete(0,END)
		self.retentionAmount.delete(0,END)
		self.grossAmount.delete(0,END)
		self.gst.delete(0,END)
		self.netInvoiceAmount.delete(0,END)
		self.remarks.delete(0,END)
		

if __name__ == '__main__':


    root = Tk()
    root.title('')


    myLogin = loginPage(root)


    #root.wait_window(myLogin.mySendMail.sp)
    mainloop()
