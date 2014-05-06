#!/usr/bin/env python
#coding=utf-8


from smtplib import *
from Tkinter import *
import ttk
import tkMessageBox
import string
import os
import datas
import datetime

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
		self.DATALIST=[]

		self.mas = Toplevel(master)

		menubar=Menu(self.mas)
		filemenu=Menu(menubar,tearoff=0)
		filemenu.add_command(label='Add Invoice')
		filemenu.add_command(label='Delete Invoice')
		filemenu.add_separator()
		filemenu.add_command(label='Exit',command=master.quit)
		menubar.add_cascade(label='File',menu=filemenu)

		projmenu=Menu(menubar,tearoff=0)
		projmenu.add_command(label='Update Project List')
		menubar.add_cascade(label='Project',menu=projmenu)

		aboutmenu=Menu(menubar,tearoff=0)
		aboutmenu.add_command(label='About Me')
		menubar.add_cascade(label='About',menu=aboutmenu)

		self.mas['menu']=menubar


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
		print len(a1)
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
		self.invoice_date=StringVar()
		self.invoiceDate=Entry(self.sp,textvariable=self.invoice_date).grid(row=1,column=7,sticky=W)
		self.invoice_date.set('')
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
		#=====CLIENT ATTN=====
		self.client_attn=StringVar()
		self.clientAttn=Entry(self.sp,textvariable=self.client_attn,width=25).grid(row=8,column=1,columnspan=2,sticky=W)
		#=====QUOTATION DATE=====
		self.quotation_date=StringVar()
		self.quotationDate=Entry(self.sp,textvariable=self.quotation_date).grid(row=2,column=4,sticky=W)
		self.quotation_date.set('')
		#=====QUOTATION NO.=====
		self.quotation_no=StringVar()
		self.quotation=Entry(self.sp,textvariable=self.quotation_no).grid(row=3,column=4,sticky=W)
		self.quotation_no.set('')
		#=====CLIENT PO NO=====
		self.client_po=StringVar()
		self.clientPo=Entry(self.sp,textvariable=self.client_po).grid(row=4,column=4,sticky=W)
		self.client_po.set('')
		#=====CREDIT NOTE NO.=====
		self.credit_note=StringVar()
		self.creditNote=Entry(self.sp,textvariable=self.credit_note).grid(row=5,column=4,sticky=W)
		self.credit_note.set('')
		#=====REV=====
		self.q_rev=StringVar()
		self.rev=Entry(self.sp,textvariable=self.q_rev).grid(row=6,column=4,sticky=W)
		self.q_rev.set('')
		#=====INVOICE AMOUNT=====
		self.invoice_amount=StringVar()
		self.invoiceAmount=Entry(self.sp,textvariable=self.invoice_amount).grid(row=2,column=7,sticky=W)
		self.invoice_amount.set('')
		#=====CN AMOUNT=====
		self.cn_amount=StringVar()
		self.cnAmount=Entry(self.sp,textvariable=self.cn_amount).grid(row=3,column=7,sticky=W)
		self.cn_amount.set('')
		#=====RETENTION PERCENT=====
		self.retention_percent=StringVar()
		self.retentionPercent=Entry(self.sp,textvariable=self.retention_percent).grid(row=4,column=7,sticky=W)
		self.retention_percent.set('')
		#=====RETENTION AMOUNT=====
		self.retention_amount=StringVar()
		self.retentionAmount=Entry(self.sp,textvariable=self.retention_amount).grid(row=5,column=7,sticky=W)
		self.retention_amount.set('')
		#=====GROSS AMOUNT=====
		self.gross_amount=StringVar()
		self.grossAmount=Entry(self.sp,textvariable=self.gross_amount).grid(row=2,column=9,sticky=W)
		self.gross_amount.set('')
		#=====GST=====
		self.invoice_gst=StringVar()
		self.gst=Entry(self.sp,textvariable=self.invoice_gst).grid(row=3,column=9,sticky=W)
		self.invoice_gst.set('')
		#=====NET INVOICE AMOUNT=====
		self.net_invoice_amount=StringVar()
		self.netInvoiceAmount=Entry(self.sp,textvariable=self.net_invoice_amount).grid(row=4,column=9,sticky=W)
		self.net_invoice_amount.set('')

#=======remarks========		
		f2=Frame(self.sp)
		bary2=Scrollbar(f2)
		bary2.pack(side=RIGHT,fill=Y)
		self.remarks=Text(f2,width=15,height=5)
		self.remarks.pack(side=LEFT,fill=BOTH)
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
		pagebar=Frame(self.mas)
		self.providebtn=Button(pagebar,text='PROVIDER',command=self.providepage).pack(side=LEFT,padx=5)
		self.pages=StringVar()
		self.page_pages=Label(pagebar,textvariable=self.pages).pack(side=LEFT,padx=5)
		self.pages.set('1/1')
		self.nextbtn=Button(pagebar,text='NEXT',command=self.nextpage).pack(side=LEFT,padx=5)

		pagebar.pack(fill=X)
#===============================================
	def getInvoiceDetail(self,event):
		'''
			get selected invoice information
		'''
		if self.invoicelist.get():
			a=((self.invoicelist.get()).strip('')).upper()
			print a

			m=datas.getData()
			invoice_summary=[]
			for i in m:
				if i['invoice_no']==a:
					invoice_summary.append(i)
			if not invoice_summary:
				tkMessageBox.showinfo('Notice','Please check the invoice again.')
				return
			else:
				self.clearData()
				if len(invoice_summary)==1:
					invoice_no=invoice_summary[0]['invoice_no']
					invoice_rev=invoice_summary[0]['invoice_rev']
					self.invoiceRev.set(invoice_rev)
					self.getInvoice(invoice_no,invoice_rev)
				else:
					x=[i['invoice_rev'] for i in invoice_summary]
					self.invoiceRev['values']=tuple(x)


	def getInvoiceInfo(self):
		if self.invoicelist.get() and self.invoiceRev.get():
			invoice_no=(self.invoicelist.get()).strip()
			invoice_rev=(self.invoiceRev.get()).strip()
			self.getInvoice(invoice_no,invoice_rev)

	def getInvoice(self,invoice_no,invoice_rev):
		if invoice_no and invoice_rev:
			m=datas.getData()
			for i in m:
				if i['invoice_no']==invoice_no and i['invoice_rev']==invoice_rev:
					self.invoice_date.set(i['invoice_date'])
					if i['payment_status']:
						self.invoiceStatus.set(i['payment_status'])
					if i['project_code']:	
						self.projectlist.set(i['project_code'])
					if i['project_title']:
						self.projecttitle.insert(END,i['project_title'])
					if i['client_company_name']:
						self.clientCompany.insert(END,i['client_company_name'])
					if i['client_name']:	
						self.client_attn.set(i['client_name'])
					if i['quotation_date']:
						self.quotation_date.set(i['quotation_date'])
					self.quotation_no.set(i['quotation_ref'])
					self.client_po.set(i['client_po_no'])
					self.credit_note.set(i['credit_note_no'])
					self.q_rev.set(i['credit_note_rev'])
					self.invoice_amount.set(i['invoice_amount'])
					self.cn_amount.set(i['cn_amount'])
					self.retention_percent.set(i['retention_percent'])
					self.retention_amount.set(i['retention_amount'])
					self.gross_amount.set(i['gross_amount'])
					self.invoice_gst.set(i['gst'])
					self.net_invoice_amount.set(i['net_invoice_amount'])
					self.remarks.insert(END,i['remarks'])
			

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
		whichitem='invoice_no'
		keywords=(self.invoicelist.get()).strip()
		self.searchit(whichitem,keywords)

	def searchProject(self):
		whichitem='project_code'
		keywords=(self.projectlist.get()).strip()
		self.searchit(whichitem,keywords)

	def searchit(self,whichitem,keywords):
		self.DATALIST=[]
		m=[]
		n=self.invoiceList.get_children()
		if n:
			for i in n:
				self.invoiceList.delete(i)
		s=datas.getData()
		if keywords:
			w=keywords.strip()
			for i in s:
				if w in i[whichitem]:
					m.append(i)
		else:
			for i in s:
				m.append(i)
		self.DATALIST.extend(m)
		if len(m)>25:
			if len(m)%25==0:
				pages=len(m)/25
			else:
				pages=len(m)/25+1
			page=1
			p=str(page)+'/'+str(pages)
			self.pages.set(p)
			for i in m[:25]:
				self.invoiceList.insert('','end',values=i)
		else:
			self.pages.set('1/1')
			for i in m:
				self.invoiceList.insert('','end',values=i)
		self.clearInvoice()

	def addInvoice(self):
		if self.projectlist.get() and self.net_invoice_amount.get():
			invoice_date=self.fillItems(self.invoice_date.get())
			project_code=self.fillItems(self.projectlist.get())
			project_title=self.fillItems(self.projecttitle.get(1.0,END))
			client_company_name=self.fillItems(self.clientCompany.get(1.0,END))
			client_name=self.fillItems(self.client_attn.get())
			quotation_date=self.fillItems(self.quotation_date.get())
			quotation_ref=self.fillItems(self.quotation_no.get())
			client_po_no=self.fillItems(self.client_po.get())
			credit_note_no=self.fillItems(self.credit_note.get())
			credit_note_rev=self.fillItems(self.q_rev.get())
			invoice_amount=self.fillItems(self.invoice_amount.get())
			cn_amount=self.fillItems(self.cn_amount.get())
			retention_percent=self.fillItems(self.retention_percent.get())
			retention_amount=self.fillItems(self.retention_amount.get())
			gross_amount=self.fillItems(self.gross_amount.get())
			gst=self.fillItems(self.invoice_gst.get())
			net_invoice_amount=self.fillItems(self.net_invoice_amount.get())
			remarks=self.fillItems(self.remarks.get(1.0,END))
			print remarks
			if not len(remarks):
				remarks=None
			payment_status=self.fillItems(self.invoiceStatus.get())
			create_by=self.fillItems(self.username.get())
			create_date=(datetime.datetime.now().strftime('%Y%m%d-%H%M'))

			if self.invoicelist.get():
				invoice_no=self.fillItems(self.invoicelist.get())
				invoice_rev=datas.newInvoiceRev(invoice_no)
			else:
				invoice_no=datas.newInvoiceNo()
				invoice_rev='R0'
				
			is_delete=None
			delete_by=None
			delete_date=None

			inv_list=[invoice_no,invoice_rev,invoice_date,project_code,project_title,client_company_name,client_name,quotation_date,quotation_ref,client_po_no,credit_note_no,credit_note_rev,invoice_amount,cn_amount,retention_percent,retention_amount,gross_amount,gst,net_invoice_amount,remarks,payment_status,create_by,create_date,is_delete,delete_by,delete_date]
			print inv_list
			print len(inv_list)
#			try:
			if len(inv_list):
				datas.add(inv_list)
				self.invoicelist.set(invoice_no)
				self.invoiceRev.set(invoice_rev)
				tkMessageBox.showinfo('Notice','the Invoice %s %s create success.' % (invoice_no,invoice_rev))
				self.clearData()
#			except Exception as e:
#				tkMessageBox.showinfo('Notice','Please check your data. ')
#				print e

	def fillItems(self,words):
		if words:
			words=words.replace(',','.')
			return words.strip()
		else:
			return None

	def editInvoice(self):
		pass

	def delInvoice(self):
		pass

	def clearInvoice(self):
		try:
			self.clearData()
			self.invoiceRev.delete(0,END)
			self.invoicelist.delete(0,END)
			self.sn.set('')
#			tkMessageBox.showinfo('Notice','Clear success.')
		except Exception as e:
			tkMessageBox.showinfo('Notice',e)

	def getInvoiceItem(self):
		self.clearData()
		self.invoicelist.set('')
		self.invoiceRev.set('')

		m=self.invoiceList.selection()
		if m:
			x=self.invoiceList.item(m)['values']
			self.sn.set(x[0])
			self.invoicelist.set(x[1])
			self.invoiceRev.set(x[2])
			self.invoice_date.set(x[3])
			self.invoiceStatus.set(x[21])

			self.projectlist.insert(END,x[4])
			self.projecttitle.insert(END,x[5])
			self.clientCompany.insert(END,x[6])
			self.client_attn.set(x[7])
			self.quotation_date.set(x[8])
			self.quotation_no.set(x[9])
			self.client_po.set(x[10])
			self.credit_note.set(x[11])
			self.q_rev.set(x[12])
			self.invoice_amount.set(x[13])
			self.cn_amount.set(x[14])
			self.retention_percent.set(x[15])
			self.retention_amount.set(x[16])
			self.gross_amount.set(x[17])
			self.invoice_gst.set(x[18])
			self.net_invoice_amount.set(x[19])
			self.remarks.insert(END,x[20])
		

	def clearData(self):
		self.sn.set('')
		self.invoice_date.set('')
		self.invoiceStatus.set('')
		self.projectlist.set('')

		self.projecttitle.delete(1.0,END)
		self.clientCompany.delete(1.0,END)
		self.client_attn.set('')
		self.quotation_date.set('')
		self.quotation_no.set('')
		self.client_po.set('')
		self.credit_note.set('')
		self.q_rev.set('')
		self.invoice_amount.set('')
		self.cn_amount.set('')
		self.retention_percent.set('')
		self.retention_amount.set('')
		self.gross_amount.set('')
		self.invoice_gst.set('')
		self.net_invoice_amount.set('')
		self.remarks.delete(1.0,END)
		

#===========PAGE MANAGEMENT============
	def providepage(self):
		m=self.pages.get()
		p=m.split('/')
		if int(p[0])>1:
			n=int(p[0])-1
			new_page=str(n)+'/'+p[1]
			self.pages.set(new_page)
			new_items=self.DATALIST[((n-1)*25):(n*25-1)]
			for i in self.invoiceList.get_children():
				self.invoiceList.delete(i)
			for i in new_items:
				self.invoiceList.insert('','end',values=i)

	def nextpage(self):
		m=self.pages.get()
		p=m.split('/')
		if int(p[0])>=int(p[1]):
			return
		n=int(p[0])
		new_page=str(n+1)+'/'+p[1]
		self.pages.set(new_pages)
		new_items=self.DATALIST[(n*25):((n+1)*25-1)]
		for i in self.invoiceList.get_children():
			self.invoiceList.delete(i)
		for i in new_items:
			self.invoiceList.insert('','end',values=i)


if __name__ == '__main__':


    root = Tk()
    root.title('')


    myLogin = loginPage(root)


    #root.wait_window(myLogin.mySendMail.sp)
    mainloop()
