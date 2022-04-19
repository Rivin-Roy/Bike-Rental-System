from flask import *
from database import *
import uuid
staff=Blueprint('staff',__name__)


@staff.route('/staffhome',methods=['get','post'])
def staffhome():
	sname=session['sname']
	sid=session['sid']

	return render_template('staffhome.html',sname=sname)


@staff.route('/staff_view_profile',methods=['get','post'])
def staff_view_profile():
	data={}
	sid=session['sid']
	uname=session['username']
	q="SELECT * FROM staff INNER JOIN login USING(username) where username='%s'"%(uname)
	print(q)
	res=select(q)
	data['updater']=res
	print(res)

	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		username=request.form['uname']
		print(username)
		pwd=request.form['password']
		q="update staff set username='%s',firstname='%s',lastname='%s',place='%s',phone='%s',email='%s' where staff_id='%s'"%(username,fname,lname,place,phone,email,sid)
		print(q)
		update(q)
		
		q="update login set username='%s',password='%s' where username='%s'"%(username,pwd,uname)
		update(q)
		session['username']=username
		uname=session['username']
		print(uname)
		flash("updated successfully")
		return redirect(url_for('staff.staff_view_profile'))
	return render_template('staff_view_profile.html',data=data)





@staff.route('/staff_manage_vehicle',methods=['get','post'])
def staff_manage_vehicle():
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
			return redirect(url_for('staff.staff_manage_vehicle'))

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
		return redirect(url_for('staff.staff_manage_vehicle'))
	if action=='update':
		q="select * from vehicle where vehicle_id='%s'"%(id)
		data['updater']=select(q)
	if action=='inactive':
		
		q="update vehicle set vstatus='inactive' where vehicle_id='%s'"%(id)
		update(q)
		print(q)
		flash("UPDATED AS INACTIVE")
		return redirect(url_for('staff.staff_manage_vehicle'))
	if action=='active':
		q="update vehicle set vstatus='active' where vehicle_id='%s'"%(id)
		update(q)
		return redirect(url_for('staff.staff_manage_vehicle'))
	if 'update' in request.form:
		vehicle=request.form['vehicle']
		f=request.files['img']
		amt=request.form['amt']
		vno=request.form['vno']
		path="static/"+str(uuid.uuid4())+f.filename
		f.save(path)
		q="update vehicle set vehiclename='%s',image='%s',amt='%s',vno='%s' where vehicle_id='%s'"%(vehicle,path,amt,vno,id)
		update(q)
		return redirect(url_for('staff.staff_manage_vehicle'))
	return render_template('staff_manage_vehicle.html',data=data)

@staff.route('/staff_manage_slots',methods=['get','post'])
def staff_manage_slots():
	data={}
	if 'submit' in request.form:
		td=request.form['td']
		rate=request.form['rate']
		q="select * from timeslot where status='active' and duration='%s'"%(td)
		res=select(q)
		if res:
			flash("ALREADY A SLOT ACTIVE IN TIME DURATION"+td)
			return redirect(url_for('staff.staff_manage_slots'))
		else:
			q="insert into timeslot values(NULL,'%s','%s','active')"%(td,rate)
			lid=insert(q)
			flash("ADDED SUCESSFULLY")
			return redirect(url_for('staff.staff_manage_slots'))

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
			return redirect(url_for('staff.staff_manage_slots'))
		else:
			q="update timeslot set duration='%s',rate='%s' where slot_id='%s'"%(td,rate,id)
			update(q)
			print(q)
			print("55555555555555555555555")
			return redirect(url_for('staff.staff_manage_slots'))
	if action=='inactive':
		
		q="update timeslot set status='inactive' where slot_id='%s'"%(id)
		update(q)
		flash("UPDATED AS INACTIVE")
		return redirect(url_for('staff.staff_manage_slots'))
	if action=='active':
		q="update timeslot set status='active' where slot_id='%s'"%(id)
		update(q)
		return redirect(url_for('staff.staff_manage_slots'))
	
	return render_template('staff_manage_slots.html',data=data)



@staff.route('/staff_view_bookings',methods=['get','post'])
def staff_view_bookings():
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
		return redirect(url_for('staff.staff_view_bookings'))

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
					return redirect(url_for('staff.staff_view_bookings'))

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
					return redirect(url_for('staff.staff_view_bookings'))
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
					return redirect(url_for('staff.staff_view_bookings'))
	return render_template("staff_view_bookings.html",data=data)


@staff.route('/staff_print_bookings')
def staff_print_bookings():
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