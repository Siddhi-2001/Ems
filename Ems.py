from tkinter import*
from tkinter.messagebox import*
from tkinter.scrolledtext import*
import matplotlib.pyplot as plt
import pandas as pd
import requests
from sqlite3 import*
import re
mw=Tk()
mw.title("E.M.S")
mw.geometry("800x680+200+100")
f=("Times New Roman",30,"bold")
mw.configure(bg="plum")

def f1():
	mw.withdraw()
	aw.deiconify()
def f2():
	aw.withdraw()
	mw.deiconify()
def f3():
	mw.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0,END)
	con=None
	try:
		con=connect("emp.db")
		cursor=con.cursor()
		sql="select *from employee order by id"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"ID="+str(d[0])+"  Name="+str(d[1])+"  Salary="+str(d[2])+"\n"
		vw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
def f4():
	vw.withdraw()
	mw.deiconify()
def f5():
	mw.withdraw()
	uw.deiconify()
def f6():
	uw.withdraw()
	mw.deiconify()
def f7():
	mw.withdraw()
	dw.deiconify()
def f8():
	dw.withdraw()
	mw.deiconify()

def add():
	con=None
	try:
		con=connect("emp.db")
		cursor=con.cursor()
		sql="insert into employee values('%s','%s','%s')"
		id=str(aw_ent_id.get())
		name=aw_ent_name.get()
		salary=str(aw_ent_sal.get())
		cursor.execute(sql%(id,name,salary))
		if len(id)==0:
			raise Exception("Enter Id")
		elif bool(re.match("^[A-z ]+$",id)):
			raise Exception("Enter Integers Only")

		else:
			id=int(aw_ent_id.get())
			
			if id<1:
				raise Exception("Id should be +ve")
			elif (len(name)==0)or (name.isspace()):
				raise Exception("Enter Name")
			elif (len(name)<2):
				raise Exception("Invalid name")
			elif not bool(re.match("^[A-z ]+$",name)):
				raise Exception("Name should contain only alphabets")
			elif len(salary)==0:
				raise Exception("Enter Salary")
			elif bool(re.match("^[A-z ]+$",salary)):
				raise Exception("Enter Integers Only")
			else:
				salary=int(aw_ent_sal.get())
				if(salary<0):
					raise Exception("Salary must be +ve")
				if(salary<8000):
					raise Exception("Salary must be greater than 8000")
				else:
					con.commit()
					showinfo("Success","emp info saved")
	except IntegrityError:
		showerror("issue","Id already exists")
	except Exception as e:
		con.rollback()
		showerror("issue:",e)
	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0,END)
		aw_ent_name.delete(0,END)
		aw_ent_sal.delete(0,END)
		aw_ent_id.focus()

def update():
	con=None
	try:
		con=connect("emp.db")
		cursor=con.cursor()
		sql="update employee set name='%s',salary='%s' where id='%s'"
		id=str(uw_ent_id.get())
		name=uw_ent_name.get()
		salary=str(uw_ent_sal.get())
		cursor.execute(sql%(name,salary,id))
		if(len(id)==0):
			raise Exception("Enter  Id")
		elif bool(re.match("^[A-Za-z ]+$",id)):
			raise Exception("Enter only Integer")
		else: 
			id=int(uw_ent_id.get())
			if(id<1):
				raise Exception("Id should be +ve")
			elif(len(name)==0) :
				raise Exception("Enter Name")
			elif (len(name)<2):
				raise Exception("Invalid name")
			elif not bool(re.match("^[A-Za-z ]+$",name)):
				raise Exception("Name should contain only alphabets")	
			elif(len(salary)==0):
				raise Exception("Enter Salary")	
			elif bool(re.match("^[A-Za-z ]+$",salary)):
				raise Exception("Enter only Integer")
			else:
				salary=int(uw_ent_sal.get())
				if(salary<0):
					raise Exception("Salary must be positive")
				if(salary<8000):
					raise Exception("Salary must be greater than 8000")
				else:
					if cursor.rowcount==1:
						con.commit()
						showinfo("Success","Record updated")
					else:
						showerror("Error","Id does not exists")
	except Exception as e:
		con.rollback()
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		uw_ent_id.delete(0,END)
		uw_ent_name.delete(0,END)
		uw_ent_sal.delete(0,END)
		uw_ent_id.focus()

def delete():
	con=None
	try:
		con=connect("emp.db")
		cursor=con.cursor()
		sql="delete from employee where id='%s'"
		id=str(dw_ent_id.get())
		cursor.execute(sql%(id))
		if(len(id)==0):
			raise Exception("Enter  Id")
		elif bool(re.match("^[A-Za-z ]+$",id)):
			raise Exception("Enter only Integer")
		else: 
			id=int(dw_ent_id.get())
			if(id<1):
				raise Exception("Id should be +ve")
			elif cursor.rowcount==1:
				con.commit()
				showinfo("Success","record deleted")
			else:
				showerror("Error","Record does not exists")
	except Exception as e:
		con.rollback()
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		dw_ent_id.delete(0,END)
		dw_ent_id.focus()
		

def graph():
	con=None
	try:
		con=connect("emp.db")
		cursor=con.cursor()
		sql="select name,salary from employee order by salary desc limit 5"
		cursor.execute(sql)
		data=cursor.fetchall()
		name=[]
		salary=[]
		for d in data:
			name.append(d[0])
			salary.append(d[1])
		plt.bar(name,salary,width=0.40,color="black")
		plt.xlabel("Name")
		plt.ylabel("Salary")
		plt.title("EMS")
		plt.show()
	except Exception as e:
		print("issue",e)
	finally:
		if con is not None:
			con.close()

def loc():
	try:
		wa="http://ip-api.com/json/49.36.111.29"
		res=requests.get(wa)
		data=res.json()
		city=data["city"]
		return city
	except Exception as e:
		showerror("issue",e)

def weather():
	try:
		city=loc()
		a1="https://api.openweathermap.org/data/2.5/weather?"
		a2="q="+ city
		a3="&appid="+"c6e315d09197cec231495138183954bd"
		a4="&units="+"metric"
		wa=a1+a2+a3+a4
		res=requests.get(wa)
		data=res.json()
		temp=data["main"]["temp"]
		t=str(temp)+str('\u00b0C')
		return t
	except Exception as e:
		showerror("issue",e)


	
btn_add=Button(mw,text=" ADD ",font=f,command=f1 ,bg="medium purple")
btn_view=Button(mw,text=" VIEW ",font=f,command=f3,bg="medium purple")
btn_up=Button(mw,text="UPDATE",font=f,command=f5,bg="medium purple")
btn_del=Button(mw,text="DELETE",font=f,command=f7,bg="medium purple")
btn_chart=Button(mw,text="CHARTS",font=f,command=graph,bg="medium purple")
btn_add.pack(pady=30)
btn_view.pack(pady=10)
btn_up.pack(pady=10)
btn_del.pack(pady=10)
btn_chart.pack(pady=10)

lab_loc=Label(mw,text="Location:",font=f,bg="plum")
lab_loc.place(x=110,y=600)
lab_city=Label(mw,text="",font=f,bg="plum")
lab_city.place(x=290,y=600)
city=loc()
lab_city.configure(text=city)
lab_temp=Label(mw,text="Temp:",font=f,bg="plum")
lab_temp.place(x=490,y=600)
lab_wea=Label(mw,text="",font=f,bg="plum")
lab_wea.place(x=610,y=600)
wea=weather()
lab_wea.configure(text=wea)


aw=Toplevel(mw)
aw.title("Add Emp")
aw.geometry("800x680+200+150")
f=("Times New Roman",30,"bold")
aw.configure(bg="plum")
aw_lab_id=Label(aw,text="enter id:",font=f,bg="plum")
aw_ent_id=Entry(aw,font=f)
aw_lab_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lab_name=Label(aw,text="enter name:",font=f,bg="plum")
aw_ent_name=Entry(aw,font=f)
aw_lab_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lab_sal=Label(aw,text="enter salary:",font=f,bg="plum")
aw_ent_sal=Entry(aw,font=f)
aw_lab_sal.pack(pady=10)
aw_ent_sal.pack(pady=10)

aw_btn_save=Button(aw,text="Save",font=f,command=add,bg="medium purple")
aw_btn_back=Button(aw,text="Back",font=f,command=f2,bg="medium purple")
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)
aw.withdraw()

vw=Toplevel(mw)
vw.title("View Emp")
vw.geometry("800x680+200+100")
vw.configure(bg="plum")
vw_st_data=ScrolledText(vw,width=40,height=12,font=f)
vw_btn_back=Button(vw,text="Back",font=f,command=f4,bg="medium purple")
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.withdraw()

uw=Toplevel(mw)
uw.title("Update Emp")
uw.geometry("800x680+200+100")
uw.configure(bg="plum")
uw_lab_id=Label(uw,text="enter id",font=f,bg="plum")
uw_ent_id=Entry(uw,font=f)
uw_lab_id.pack(pady=10)
uw_ent_id.pack(pady=10)
uw_lab_name=Label(uw,text="enter name",font=f,bg="plum")
uw_ent_name=Entry(uw,font=f)
uw_lab_name.pack(pady=10)
uw_ent_name.pack(pady=10)
uw_lab_sal=Label(uw,text="enter salary",font=f,bg="plum")
uw_ent_sal=Entry(uw,font=f)
uw_lab_sal.pack(pady=10)
uw_ent_sal.pack(pady=10)

uw_btn_save=Button(uw,text="Save",font=f,command=update,bg="medium purple")
uw_btn_back=Button(uw,text="Back",command=f6,font=f,bg="medium purple")
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)
uw.withdraw()

dw=Toplevel(aw)
dw.title("Delete Emp")
dw.geometry("800x680+200+100")
dw.configure(bg="plum")
dw_lab_id=Label(dw,text="enter id which u want to delete",font=f,bg="plum")
dw_ent_id=Entry(dw,font=f)
dw_lab_id.pack(pady=10)
dw_ent_id.pack(pady=10)

dw_btn_del=Button(dw,text="Delete",font=f,command=delete,bg="medium purple")
dw_btn_back=Button(dw,text="Back",font=f,command=f8,bg="medium purple")
dw_btn_del.pack(pady=10)
dw_btn_back.pack(pady=10)
dw.withdraw()



mw.mainloop()