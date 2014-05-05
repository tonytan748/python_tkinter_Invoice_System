#-*-coding=utf-8-*-
import os
import sqlite3
import datetime
import sys
import shutil

FILEPATH=os.path.join(os.path.split(sys.argv[0])[0],'data')
FILENAME=os.path.join(FILEPATH,'invoice.db')

USER=os.path.join(FILEPATH,'user.txt')

def mainprocess(content):
	try:
		db=sqlite3.connect(FILENAME)
		cursor=db.cursor()
		cursor.execute(content)
		db.commit()
	except Exception as e:
		db.rollback()
		print e
	except DatabaseError as e:
		db.rollback()
		raise e
	finally:
		db.close()

def createTable():
	content='''
		CREATE TABLE invoice(
			id INTEGER PRIMARY KEY NOT NULL,
			invoice_no TEXT NOT NULL,
			invoice_rev TEXT NOT NULL,
			invoice_date TEXT NOT NULL,
			project_code TEXT NOT NULL,
			project_title TEXT NOT NULL,
			client_company_name TEXT NOT NULL,
			client_name TEXT NOT NULL,
			quotation_date TEXT NOT NULL,
			quotation_ref TEXT NOT NULL,
			client_po_no TEXT NOT NULL,
			credit_note_no TEXT NOT NULL,
			credit_note_rev TEXT NOT NULL,
			invoice_amount TEXT NOT NULL,
			cn_amount TEXT NOT NULL,
			retention_persent TEXT NOT NULL,
			retention_acount TEXT NOT NULL,
			gross_amount TEXT NOT NULL,
			gst TEXT NOT NULL,
			net_invoice_amount TEXT NOT NULL,
			remarks TEXT NOT NULL,
			payment_status NOT NULL,
			create_by TEXT NOT NULL,
			create_date TEXT NOT NULL,
			is_delete TEXT NOT NULL,
			delete_by TEXT NOT NULL,
			delete_date TEXT NOT NULL
		)
	'''
	mainprocess(content)
	
def getData():
	try:
		db=sqlite3.connect(FILENAME)
		c=db.cursor()
		c.execute('SELECT * FROM invoice')
		x=[]
		for i in c:
			if not i[23]:
				m={'id':{0},'invoice_no':{1},'invoice_rev':{2},'invoice_date':{3},	'project_code':{4},'project_title':{5},'client_company_name':{6},'client_name':{7},'quotation_date':{8},'quotation_ref':{9},'client_po_no':{10},'credit_note_no':{11},'credit_note_rev':{12},'invoice_amount':{13},'cn_amount':{14},'retention_persent':{15},'retention_acount':{16},'gross_amount':{17},'gst':{18},'net_invoice_amount':{19},'remarks':{20},'payment_status':{21},'create_by':{22},'create_date':{23}}
				x.append(m)
		db.commit()
		return x
	except Exception as e:
		db.rollback()
		print e
	except DatabaseError as e:
		db.rollback()
		raise e
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

def add(inv_list):
	if inv_list:
		content='''
			INSERT INTO invoice(invoice_no,invoice_rev,invoice_date,project_code,project_title,client_company_name,client_name,quotation_date,quotation_ref,client_po_no,credit_note_no,credit_note_rev,invoice_amount,cn_amount,retention_persent,retention_acount,gross_amount,gst,net_invoice_amount,remarks,create_by,create_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
		''',(inv_list)
		mainprocess(content)
		return True

def update(inv_id,inv_list):
	if inv_id and inv_list:
		content='''
			UPDATE invoice SET invoice_no=?, invoice_rev=?, invoice_date=?, project_code=?, project_title=?, client_company_name=?, client_name=?, quotation_date=?, quotation_ref=?, client_po_no=?, credit_note_no=?, credit_note_rev=?, invoice_amount=?, cn_amount=?, retention_persent=?, retention_acount=?, gross_amount=?, gst=?, net_invoice_amount=?, remarks=?, create_by=?, create_date=? WHERE id=?
		''',(','.join(inv_list),inv_id)
		mainprocess(content)
		return True
		
def delete(inv_id,del_info):
	if inv_id and del_info:
		content='''
			UPDATE invoice SET is_delete=1, delete_by=?, delete_date=?
		''',(inv_id,','.join(del_info))
		mainprocess(content)
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


if __name__=='__main__':
	createTable()