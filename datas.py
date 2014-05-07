#-*-coding=utf-8-*-
import os
import sqlite3
import datetime
import sys
import shutil

FILEPATH=os.path.join(os.path.split(sys.argv[0])[0],'data')
FILENAME=os.path.join(FILEPATH,'invoice.db')

USER=os.path.join(FILEPATH,'user.txt')

def mainprocess(*args):
	m=args
	try:
		db=sqlite3.connect(FILENAME)
		db.text_factory=str
		cursor=db.cursor()
		if len(m)==1:
			cursor.execute(m[0])
		else:
			cursor.execute(m[0],m[1])
		db.commit()
	except Exception as e:
		db.rollback()
		print e
	finally:
		db.close()

def createTable():
	content='''
		CREATE TABLE invoice(
			id INTEGER PRIMARY KEY NOT NULL,
			invoice_no TEXT NOT NULL,
			invoice_rev TEXT NOT NULL,
			invoice_date TEXT,
			project_code TEXT NOT NULL,
			project_title TEXT,
			client_company_name TEXT,
			client_name TEXT,
			quotation_date TEXT,
			quotation_ref TEXT,
			client_po_no TEXT,
			credit_note_no TEXT,
			credit_note_rev TEXT,
			invoice_amount TEXT,
			cn_amount TEXT,
			retention_percent TEXT,
			retention_amount TEXT,
			gross_amount TEXT,
			gst TEXT,
			net_invoice_amount TEXT,
			remarks TEXT,
			payment_status TEXT,
			create_by TEXT,
			create_date TEXT,
			is_delete TEXT,
			delete_by TEXT,
			delete_date TEXT
		)
	'''
	mainprocess(content)
	
def getData():
	try:
		db=sqlite3.connect(FILENAME)
		c=db.cursor()
		c.execute('SELECT * FROM invoice')
		x=[]
		for i in c.fetchall():
			if not i[24]:
				m={'id':i[0],'invoice_no':i[1],'invoice_rev':i[2],'invoice_date':i[3],	'project_code':i[4],'project_title':i[5],'client_company_name':i[6],'client_name':i[7],'quotation_date':i[8],'quotation_ref':i[9],'client_po_no':i[10],'credit_note_no':i[11],'credit_note_rev':i[12],'invoice_amount':i[13],'cn_amount':i[14],'retention_percent':i[15],'retention_amount':i[16],'gross_amount':i[17],'gst':i[18],'net_invoice_amount':i[19],'remarks':i[20],'payment_status':i[21],'create_by':i[22],'create_date':i[23],'is_delete':i[24],'delete_by':i[25],'delete_date':i[26]}
				x.append(m)
		db.commit()
		return x
	except Exception as e:
		db.rollback()
		print e
	finally:
		db.close()

def searchInv(inv_no):
	if inv_no:
		m=getData()
		x=(i for i in m if inv_no in i['invoice_no'])
		if x:
			return list(x)
		else:
			return

def searchProject(pro_code):
	if inv_no:
		m=getData()
		x=(i for i in m if pro_code in i['project_code'])
		if x:
			return list(x)
		else:
			return

def newInvoiceRev(inv_no):
	if inv_no:
		m=getData()
		x=list(i for i in m if inv_no == i['invoice_no'])
		try:
			a1=[int(i['invoice_rev'][1:]) for i in x]
			mx=a1.index(max(a1))+1
			n='R'+str(mx)
			return n
		except Exception as e:
			print e
			return 
			
def newInvoiceNo():
	m=getData()
	if m:
		try:
			x=[int(i['invoice_no'][1:]) for i in m]
			if len(x)>1:
				mx=max(x)+1
			else:
				mx=2
			print mx
			n='I' + ((4-len(str(mx)))*'0') + str(mx)
			print n
			return n
		except Exception as e:
			print e
			return
	else:
		return u'I0001'
			
def add(inv_list):
	if inv_list:
		prnt=tuple(inv_list)
		content='''INSERT INTO invoice(invoice_no,invoice_rev,invoice_date,project_code,project_title,client_company_name,client_name,quotation_date,quotation_ref,client_po_no,credit_note_no,credit_note_rev,invoice_amount,cn_amount,retention_percent,retention_amount,gross_amount,gst,net_invoice_amount,remarks,payment_status,create_by,create_date,is_delete,delete_by,delete_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
		values=tuple(inv_list)
		mainprocess(content,values)
		return True

def update(inv_id,inv_list):
	if inv_id and inv_list:
		content='''UPDATE invoice SET invoice_no=?, invoice_rev=?, invoice_date=?, project_code=?, project_title=?, client_company_name=?, client_name=?, quotation_date=?, quotation_ref=?, client_po_no=?, credit_note_no=?, credit_note_rev=?, invoice_amount=?, cn_amount=?, retention_percent=?, retention_amount=?, gross_amount=?, gst=?, net_invoice_amount=?, remarks=?, payment_status=?, create_by=?, create_date=?, is_delete=?, delete_by=?, delete_date=? WHERE id=?'''
		m=inv_list.append(inv_id)
		values=tuple(inv_list)
		#values=(','.join(inv_list),int(inv_id))
		mainprocess(content,values)
		return True
		
def delete(inv_id,del_info):
	if inv_id and del_info:
		content='''UPDATE invoice SET is_delete=1, delete_by=?, delete_date=? WHERE id=?'''
		values=(','.join(del_info),inv_id)
		mainprocess(content,values)
		return True


#==========LOGIN IN===========
def getName():
	a=[]
	with open(USER,'r') as f:
		for i in f.readlines():
			m={}
			x=i.split(',')
			m['username']=x[0]
			m['password']=x[1]
			a.append(m)
	return a
	
#==========project code===========
def getProject():
	m=r'\\KMSVR\Company Data\Common\2. KM Software\backup'
	project_file=os.path.join(m,'probackup.txt')
	pl=os.path.join(os.path.split(sys.argv[0])[0],'data')
	project_list=os.path.join(pl,'paobackup.txt')
	print os.path.split(sys.argv[0])[0]
	try:
		shutil.copy(project_file,project_list)
	except Exception as e:
		print e
	#print project_list
	x=[]
	with open(project_list,'r') as f:
		for i in f.readlines():
			n=i.strip('')
			x.append(n.split(','))
	#print x
	return x[8:]
	
def insertTest():
	content='''INSERT INTO invoice(invoice_no,invoice_rev,invoice_date,project_code,project_title,client_company_name,client_name,quotation_date,quotation_ref,client_po_no,credit_note_no,credit_note_rev,invoice_amount,cn_amount,retention_percent,retention_amount,gross_amount,gst,net_invoice_amount,remarks,payment_status,create_by,create_date,is_delete,delete_by,delete_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
	values=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26')
	mainprocess(content,values)
	return True

if __name__=='__main__':
	createTable()
	insertTest()
	m=getData()
	print m