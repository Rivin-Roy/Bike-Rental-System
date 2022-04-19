from flask import *
from database import *
import uuid
from datetime import date

customer=Blueprint('customer',__name__)
 

@customer.route('/customerhome',methods=['get','post'])
def customerhome():
	cname=session['cname']
	cid=session['cid']
	print(cname)
	return render_template('customerhome.html',cname=cname)


@customer.route('/customer_view_ts',methods=['get','post'])
def customer_view_ts():
	data={}
	cname=session['cname']
	cid=session['cid']
	q="select * from timeslot where status='active'"
	res=select(q)
	print(res)
	data['timeslot']=res
	return render_template('customer_view_ts.html',data=data)




@customer.route('/customer_viewbikes',methods=['get','post'])
def customer_viewbikes():
	data={}
	cname=session['cname']
	
	id=request.args['id']
	data['id']=id
	from datetime import date
	data['today']=date.today()
	duration=request.args['duration']
	data['duration']=duration
	cid=session['cid']
	q="select * from vehicle where vstatus='active'"
	res=select(q)
	if res:
		data['vehicle']=res
		print(res)
	if 'action' in request.args:
		vid=request.args['vid']
		data['vid']=vid
	if 'submit' in request.form:
		date=request.form['date']
		q="select * from booking where customer_id='%s' and vehicle_id='%s' and slot_id='%s' and bdate='%s' and status='pending'"%(cid,vid,id,date)
		res=select(q)
		print("***************")
		print(res)
		if res:
			flash("YOUR REQUIRED BOOKING ALREADY IN YOUR BOOKING LIST")
			return redirect(url_for('customer.customer_view_bookings'))
		else:
			q="insert into booking values(NULL,'%s','%s','%s','%s','%s','%s','no')"%(cid,vid,id,duration,date,'pending')
			insert(q)
			print(q)
			flash("ADDED TO BOOKG LIST")
			return redirect(url_for('customer.customer_view_bookings',duration=duration,id=id,vid=vid))
	return render_template('customer_viewbikes.html',data=data)


@customer.route('/customer_view_bookings',methods=['get','post'])
def customer_view_bookings():
	data={}
	cid=session['cid']
	data={}
	# vid=request.args['vid']
	
	q="SELECT *,booking.status AS bstatus FROM booking  INNER JOIN timeslot USING(slot_id) INNER JOIN vehicle USING(vehicle_id) WHERE customer_id='%s'"%(cid)
	res=select(q)
	if res:
		# vid=res[0]['vehicle_id']
		# print(vid)
		data['bookings']=res
		print(res)
	if 'action' in request.args:
		vid=request.args['vid']
		action=request.args['action']
		boid=request.args['boid']	
		amt=request.args['amt']

		data['amt']=amt
		print(amt)
	else:
		action=None

	if action=="return":
		q="update booking set status='return-pending' where booking_id='%s'"%(boid)
		update(q)
		flash("RETURN SUCCESSFULLY")
		return redirect(url_for('customer.customer_view_bookings',vid=vid))
	
	if 'pay' in request.form:
		amt=request.args['amt']

		q="insert into payment values(NULL,'%s',NOW(),'paid')"%(boid)
		insert(q)
		q="update booking set status='paid' where booking_id='%s'"%(boid)
		update(q)
		q="update vehicle set vstatus='inactive' where vehicle_id='%s'"%(vid)
		update(q)
		flash("PAYMENT SUCCESS")

		return redirect(url_for('customer.customer_view_bookings',vid=vid))

	
	return render_template('customer_view_bookings.html',data=data)


@customer.route('/customer_timeextend',methods=['get','post'])
def customer_timeextend():
	data={}
	boid=request.args['boid']
	vid=request.args['vid']
	
	if 'submit' in request.form:
		data['amt']=request.form['amt']
		day=request.form['day']
		session['day']=day

	if 'pay' in request.form:
		
		
		q="update booking set extend='%s',status='extended and paid' where booking_id='%s'"%(session['day'],boid)
		update(q)
		return redirect(url_for('customer.customer_view_bookings',vid=vid))
		flash("EXETENTED")


	return render_template('customer_timeextend.html',data=data)


@customer.route('/customer_view_profile',methods=['get','post'])
def customer_view_profile():
	data={}
	username=session['username']
	print(username)
	q="select * from customer inner join login using(username) where username='%s'"%(username)
	res=select(q)
	print(res)
	data['customer']=res
	if 'submit' in request.form:
		ph=request.form['ph']
		email=request.form['email']
		street=request.form['street']
		district=request.form['district']
		uname=request.form['uname']
		password=request.form['password']
		q="update login set username='%s',password='%s' where username='%s'"%(uname,password,username)
		update(q)
		q="update customer set phone='%s',email='%s',street='%s',district='%s',username='%s' where username='%s' "%(ph,email,street,district,uname,username)
		update(q)
		session['username']=uname
		flash("PROFILE UPDATED")
		return redirect(url_for('customer.customer_view_profile'))
	if 'action' in request.args:
		q="delete login,customer from customer inner join login using(username) where username='%s'"%(username)
		delete(q)
		flash("ACCOUNT DELETED SUCESSFULLY")
		return redirect(url_for('public.home'))
	return render_template('customer_view_profile.html',data=data)