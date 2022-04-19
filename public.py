from flask import *
from database import *
import random
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
	session.clear()
	
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(uname,password)
		res=select(q)
		if res:
			session['username']=res[0]['username']
			if res[0]['usertype']=='inactive':
				flash("You are blocked by admin")
				return redirect(url_for('public.login'))
			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.adminhome'))
			if res[0]['usertype']=='inactive':
				flash("YOUR BLOCKED BY ADMIN")
				return redirect(url_for('public.login'))

			if res[0]['usertype']=='staff':
				q="select * from staff where username='%s'"%(uname)
				res=select(q)
				print(res)
				session['sid']=res[0]['staff_id']
				session['sname']=res[0]['firstname']+" "+res[0]['lastname']
				return redirect(url_for('staff.staffhome'))
			
			if res[0]['usertype']=='user':
				q="select * from customer where username='%s'"%(uname)
				res=select(q)
				print(res)
				session['cid']=res[0]['customer_id']
				session['cname']=res[0]['firstname']+" "+res[0]['lastname']
				return redirect(url_for('customer.customerhome'))
		else:
			flash("COMPLETE REGISTRATION BEFORE LOGIN")
	return render_template('login.html')


@public.route('/userreg',methods=['get','post'])
def userreg():
	data={}
	if 'submit' in request.form:
		print("^^^^^^^^^^^^^^^^^^^^^^^^")
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		ph=request.form['phone']
		email=request.form['email']
		dis=request.form['dis']
		street=request.form['street']
		gen=request.form['gen']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		if res:
			flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('public.userreg'))
		else:
			q="insert into login values('%s','%s','user')"%(uname,password)
			insert(q)
			q="insert into customer values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(uname,fname,lname,place,ph,email,dis,street,gen)
			insert(q)
			return redirect(url_for('public.userreg'))
	return render_template('userreg.html',data=data)


# @public.route('/customerreg',methods=['get','post'])
# def customerreg():
# 	data={}
# 	if 'submit' in request.form:
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		ph=request.form['phone']
# 		email=request.form['email']
# 		lat=request.form['lat']
# 		lon=request.form['lon']
# 		uname=request.form['uname']
# 		password=request.form['password']
# 		q="select * from login where username='%s' and password='%s'"%(uname,password)
# 		res=select(q)
# 		if res:
# 			flash('THIS USER NAME AND PASSWORD ALREADY TAKEN BY ANOTHER USER')
# 			return redirect(url_for('public.customerreg'))
# 		else:
# 			q="insert into login values('%s','%s','customer')"%(uname,password)
# 			lid=insert(q)
# 			q="select * from customers order by customer_id desc limit 1"
# 			res=select(q)
# 			if res:
# 				s="c__"
# 				precid=res[0]['customer_id'].split("__")
# 				print(precid)
# 				cid=int(precid[1])+1
# 				cid="c__"+str(cid)
# 				print(cid)
# 			else:
# 				cid="c__1"
# 			q="insert into customers values('%s','%s','%s','%s','%s','%s','%s','%s')"%(cid,uname,fname,lname,ph,email,lat,lon)
# 			insert(q)
# 			return redirect(url_for('public.customerreg'))
# 	return render_template('customerreg.html',data=data)



@public.route('/public_changepassword',methods=['get','post'])
def public_changepassword():
	data={}
	if 'submit' in request.form:	
		npass=request.form['uname']
		ph=request.form['ph']
		q="select email,username from login inner join customer using(username) where username='%s' and phone='%s' union select email,username from login inner join staff using(username) where username='%s' and phone='%s'"%(npass,ph,npass,ph)
		print(q)
		res=select(q)
		if res:
			session['uname']=res[0]['username']
			email=res[0]['email']
			print(email)
			rd=random.randrange(1000,9999,4)
			msg=str(rd)
			data['rd']=rd
			print(rd)
			try:
				gmail = smtplib.SMTP('smtp.gmail.com', 587)
				gmail.ehlo()
				gmail.starttls()
				gmail.login('jomonml24@gmail.com','jomon240998#')
			except Exception as e:
				print("Couldn't setup email!!"+str(e))

			msg = MIMEText(msg)

			msg['Subject'] = 'OTP FOR PASSWORD RECOVRY'

			msg['To'] = email

			msg['From'] = 'jomonml24@gmail.com'

			try:
				gmail.send_message(msg)
				print(msg)
				flash("EMAIL SENED SUCCESFULLY")
				session['rd']=rd
				return redirect(url_for('public.setotp'))


			except Exception as e:
				print("COULDN'T SEND EMAIL", str(e))
				return redirect(url_for('public.public_changepassword'))
		


			
		else:
			flash("INVALID DETAILS")
			return redirect(url_for('public.public_changepassword'))
			
	
		
	return render_template('public_changepassword.html',data=data)


@public.route('/setotp',methods=['get','post'])
def setotp():
	rd=session['rd']
	uname=session['uname']
	data={}
	if "otp" in request.form:
		otp=request.form['otp']
		if int(otp)==int(rd):
			data['chp']=uname
		else:
			flash("invalid otp")
			return redirect(url_for('public.setotp'))

	if 'update' in request.form:
		uname=request.form['uname']
		p=request.form['p']
		cp=request.form['cp']
		if p==cp:
			print("+++++++++++")
			q="update login set password='%s' where username='%s'"%(p,uname)
			update(q)
			flash("UPDATED SUCCESSFULLY")
			return redirect(url_for('public.login'))
		else:
			flash("PASSWORD MISMATCH")
			data['chp']=uname


	return render_template('setotp.html',data=data)
