from flask import *
from database import *
import uuid
admin=Blueprint('admin',__name__)
 

@admin.route('/adminhome',methods=['get','post'])
def adminhome():
	return render_template('adminhome.html')


@admin.route('/admin_manage_staff',methods=['get','post'])
def admin_manage_staff():
	data={}
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		if res:
			flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('admin.admin_manage_staff'))
		else:
			q="insert into login values('%s','%s','admin')"%(uname,password)
			insert(q)
		q="insert into staff values(NULL,'%s','%s','%s','%s','%s','%s')"%(uname,fname,lname,place,phone,email)
		insert(q)
		return redirect(url_for('admin.admin_manage_staff'))
	q="select * from staff inner join login using(username)"
	res=select(q)
	if res:
		data['staff']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update login set usertype='staff' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	if action=='inactive':
		q="update login set usertype='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	if action=='delete':
		q="delete from staff where staff_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_staff'))
	if action=='update':
		q="select * from staff where staff_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		q="update staff set firstname='%s',lastname='%s',place='%s',phone='%s',email='%s' where staff_id='%s'"%(fname,lname,place,phone,email,id)
		update(q)
		return redirect(url_for('admin.admin_manage_staff'))
	return render_template('admin_manage_staff.html',data=data)


@admin.route('/admin_view_user',methods=['get','post'])
def admin_view_user():
	data={}
	q="select * from customer inner join login using(username)"
	res=select(q)
	data['users']=res
	print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='active':
		q="update login set usertype='user' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_view_user'))
	if action=='inactive':
		q="update login set usertype='inactive' where username='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_view_user'))
	return render_template('admin_view_user.html',data=data)





@admin.route('/admin_view_bookings',methods=['get','post'])
def admin_view_bookings():
	data={}
	q="SELECT *,booking.status AS bstatus FROM booking INNER JOIN customer USING(customer_id) INNER JOIN timeslot USING(slot_id) INNER JOIN vehicle USING(vehicle_id) WHERE booking.status in('paid','extended and paid','pending','return-pending','inactive')"
	res=select(q)
	session['mains']=q
	print(res)
	data['orders']=res

	if 'action' in request.args:
		action=request.args['action']
		boid=request.args['boid']	
		vid=request.args['vid']	
	else:
		action=None

	if action=="confirm":
		q="update vehicle set vstatus='active' where vehicle_id='%s'"%(vid)
		update(q)
		q="update booking set status='inactive' where vehicle_id='%s'"%(vid)
		update(q)
		flash("CONFIRM SUCCESSFULLY")
		return redirect(url_for('admin.admin_view_bookings'))

	if 'submit' in request.form:
		nod=request.form['nod']
		print(nod)
		if nod=='':
			print("helo")

		print(nod)
		from_date=request.form['from_date']
		to_date=request.form['to_date']
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		if nod=='':
			if from_date:
				q="SELECT *,booking.status AS bstatus FROM booking INNER JOIN customer USING(customer_id) INNER JOIN timeslot USING(slot_id) INNER JOIN vehicle USING(vehicle_id) WHERE booking.status in('paid','extended and paid','pending','return-pending','inactive') AND ( bdate between '%s' and '%s')"%(from_date,to_date)
				print(q)
				res=select(q)
				if res:
					session['mains']=q
					res=select(q)
					data['orders']=res
					print(res)
				else:
					flash("NO MATCHING RESULTS")
					return redirect(url_for('admin.admin_view_bookings'))

		else:
			if from_date:
				q="SELECT *,booking.status AS bstatus FROM booking INNER JOIN customer USING(customer_id) INNER JOIN timeslot USING(slot_id) INNER JOIN vehicle USING(vehicle_id) WHERE booking.status in('paid','extended and paid','pending','return-pending','inactive') AND ( bdate between '%s' and '%s') and booking.duration='%s'"%(from_date,to_date,nod)
				print(q)

				res=select(q)
				if res:
					session['mains']=q
					res=select(q)
					data['orders']=res
					print(res)
				else:
					flash("NO MATCHING RESULTS")
					return redirect(url_for('admin.admin_view_bookings'))
			else:
				q="SELECT *,booking.status AS bstatus FROM booking INNER JOIN customer USING(customer_id) INNER JOIN timeslot USING(slot_id) INNER JOIN vehicle USING(vehicle_id) WHERE booking.status in('paid','extended and paid','pending','return-pending','inactive') and booking.duration='%s'"%(nod)
				print(q)
				if res:
					session['mains']=q
					res=select(q)
					data['orders']=res
					print(res)
				else:
					flash("NO MATCHING RESULTS")
					return redirect(url_for('admin.admin_view_bookings'))

	return render_template("admin_view_bookings.html",data=data)
	

@admin.route('/admin_print_bookings')
def admin_print_bookings():
	data={}
	from datetime import date,datetime 
	today=date.today()
	print(today)
	data['today']=today
	now=datetime.now()
	current_time=now.strftime("%H:%M:%S")
	print(current_time)
	data['current_time']=current_time	

	res=select(session['mains'])
	data['orders']=res
	
	return render_template('admin_print_booking.html',data=data)


@admin.route('/admin_view_feedback',methods=['get','post'])
def admin_view_feedback():
	data={}
	q="SELECT * FROM feedback INNER JOIN branches using(branch_id) inner join admins using(admin_id)"
	res=select(q)
	data['feedbacks']=res
	print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		if action=="update":
			q="select * from feedback inner join admins using(admin_id) where feedback_id='%s' "%(id)
			res=select(q)
			data['updater']=res
	if 'update' in request.form:
		reply=request.form['reply']
		q="update feedback set reply='%s' where feedback_id='%s'"%(reply,id)
		update(q)
		return redirect(url_for('admin.admin_view_feedback'))
	return render_template('admin_view_feedback.html',data=data)


@admin.route('/admin_change_password',methods=['get','post'])
def admin_change_password():
	data={}
	uname=session['username']
	q="select * from login where username='%s'"%(uname)
	res=select(q)
	print(res)
	data['updater']=res
	print(res)
	if 'update' in request.form:
		npass=request.form['npass']
		cpass=request.form['cpass']
		if cpass==npass:
			q="update login set password='%s' where username='%s'"%(npass,uname)
			update(q)
			flash("PASSWORD UPDATED")
		else:
			flash("PASSWORD DOES NOT MATCH")
	# q="select * from feedback inner join branches using(branch_id) where admin_id='%s'"%(cid)	
	# res=select(q)
	# data['fb']=res
	# print(res)
	return render_template('admin_change_password.html',data=data)

@admin.route('/admin_review_andrate',methods=['get','post'])
def admin_review_andrate():
	data={}
	q="select * from review_rating inner join branches using(branch_id) inner join customers using(customer_id)"
	res=select(q)
	print(res)
	data['rating']=res
	print(res)
	# q="select * from feedback inner join branches using(branch_id) where admin_id='%s'"%(cid)	
	# res=select(q)
	# data['fb']=res
	# print(res)
	return render_template('admin_review_andrate.html',data=data)


@admin.route('/admin_view_complaints',methods=['get','post'])
def admin_view_complaints():
	data={}
	q="SELECT * FROM user INNER JOIN complaint USING(user_id)"
	res=select(q)
	data['complaints']=res
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		if action=="update":
			q="select * from complaint inner join user using(user_id) where complaint_id='%s' "%(id)
			res=select(q)
			data['updater']=res
	if 'update' in request.form:
		reply=request.form['reply']
		q="update complaint set reply='%s' where complaint_id='%s'"%(reply,id)
		update(q)
		return redirect(url_for('admin.admin_view_complaints'))
	return render_template('admin_view_complaints.html',data=data)

@admin.route('/admin_manage_vehicle',methods=['get','post'])
def admin_manage_vehicle():
	data={}
	if 'submit' in request.form:
		vehicle=request.form['vehicle']
		f=request.files['img']
		amt=request.form['amt']
		vno=request.form['vno']
		path="static/"+str(uuid.uuid4())+f.filename
		f.save(path)
		q="select * from vehicle where vno='%s'"%(vno)
		res=select(q)
		if res:
			flash("ALREADY REGISTERED VEHICLE")
			return redirect(url_for('admin.admin_manage_vehicle'))
		else:
			q="insert into vehicle values(NULL,'%s','%s','%s','%s','active')"%(vehicle,path,vno,amt)
			lid=insert(q)
			flash("ADDED SUCESSFULLY")
			return redirect(url_for('admin.admin_manage_vehicle'))

	q="select * from vehicle"
	res=select(q)
	if res:
		data['vehicle']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='delete':
		q="delete from vehicle where vehicle_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.admin_manage_vehicle'))
	if action=='update':
		q="select * from vehicle where vehicle_id='%s'"%(id)
		data['updater']=select(q)
	if action=='inactive':
		
		q="update vehicle set vstatus='inactive' where vehicle_id='%s'"%(id)
		update(q)
		print(q)
		flash("UPDATED AS INACTIVE")
		return redirect(url_for('admin.admin_manage_vehicle'))
	if action=='active':
		q="update vehicle set vstatus='active' where vehicle_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_vehicle'))
	if 'update' in request.form:
		vehicle=request.form['vehicle']
		f=request.files['img']
		amt=request.form['amt']
		vno=request.form['vno']
		path="static/"+str(uuid.uuid4())+f.filename
		f.save(path)
		q="update vehicle set vehiclename='%s',image='%s',amt='%s',vno='%s' where vehicle_id='%s'"%(vehicle,path,amt,vno,id)
		update(q)
		return redirect(url_for('admin.admin_manage_vehicle'))
	return render_template('admin_manage_vehicle.html',data=data)

@admin.route('/admin_manage_slots',methods=['get','post'])
def admin_manage_slots():
	data={}
	if 'submit' in request.form:
		td=request.form['td']
		rate=request.form['rate']
		q="select * from timeslot where status='active' and duration='%s'"%(td)
		res=select(q)
		if res:
			flash("ALREADY A SLOT ACTIVE IN TIME DURATION"+td)
			return redirect(url_for('admin.admin_manage_slots'))
		else:
			q="insert into timeslot values(NULL,'%s','%s','active')"%(td,rate)
			lid=insert(q)
			flash("ADDED SUCESSFULLY")
			return redirect(url_for('admin.admin_manage_slots'))

	q="select * from timeslot"
	res=select(q)
	if res:
		data['timeslot']=res
		print(res)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='update':
		q="select * from timeslot where slot_id='%s'"%(id)
		data['updater']=select(q)
	if 'update' in request.form:
		td=request.form['td']
		rate=request.form['rate']
		q="select * from timeslot where status='active' and duration='%s'"%(td)
		res=select(q)
		if res:
			flash("ALREADY A SLOT ACTIVE IN TIME DURATION"+td)
			return redirect(url_for('admin.admin_manage_slots'))
		else:
			q="update timeslot set duration='%s',rate='%s' where slot_id='%s'"%(td,rate,id)
			update(q)
			print(q)
			print("55555555555555555555555")
			return redirect(url_for('admin.admin_manage_slots'))
	if action=='inactive':
		
		q="update timeslot set status='inactive' where slot_id='%s'"%(id)
		update(q)
		flash("UPDATED AS INACTIVE")
		return redirect(url_for('admin.admin_manage_slots'))
	if action=='active':
		q="update timeslot set status='active' where slot_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.admin_manage_slots'))
	
	return render_template('admin_manage_slots.html',data=data)

