
import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox
import pymysql as mq
import datetime
# import cryptography


mysql=mq.connect(host="localhost",user="root",password="12345678",database="pythonproject")
mycursor=mysql.cursor()

def insertData(full_name, age, gender, teacher_id, branch, dob,master) :

    # dob = datetime.datetime.strptime(dob, "%m-%d-%y").date()

    # dob_formatted = dob.strftime("%d/%m/%Y")

    mycursor.execute("Select teacher_id from teacher")

    result = mycursor.fetchall()

    flag = True

    for i in result:
        print(str(teacher_id) in i)
        if str(teacher_id) in i :
            flag = False 
            break
    
    
    if(flag):


    
        try:
            mycursor.execute("INSERT INTO teacher (name, age, gender, teacher_id, branch, dateOfBirth) VALUES (%s, %s, %s, %s, %s, %s)",(full_name, age, gender, teacher_id, branch, dob))
            mysql.commit()
            messagebox.showinfo("Successfull","Data entered successfully")
            master.switch_frame(StartPage)
        except mq.Error as e :
            print("Error",e)
            messagebox.showerror("Error","Invalid Input")
            master.switch_frame(StartPage)

    else:
        messagebox.showerror("Error","ID already exists")


def dataManipulate(id,master,self):

    mycursor.execute("SELECT * from teacher")
    result = mycursor.fetchall()

    print(result)

    flag = False
    for i in result :
        
        if (id in i):
            flag = True
            
            break

    if (flag):

        update = tk.Button(self, text="Update", width=10,font=("Arial", 15),command=lambda:master.switch_frame(UpdatePage,id))
        update.grid(row=3, column=1, padx=(10, 5), pady=10)

        delete = tk.Button(self, text="Delete",width=10,font=("Arial", 15),command=lambda:deleteData(id,master))
        delete.grid(row=3, column=2,  padx=(20, 5), pady=10)
    else :
        messagebox.showerror("Error","ID not available")
        master.switch_frame(StartPage)
    

def update(full_name, age, gender, branch, dob,updateId,master):
    try:
        mycursor.execute("UPDATE teacher SET name = %s, age = %s, gender = %s, branch = %s, dateOfBirth = %s  WHERE teacher_id = %s", (full_name, age, gender, branch, dob, updateId))

        # mycursor.execute("INSERT INTO teacher (name, age, gender, teacher_id, branch, dateOfBirth) VALUES (%s, %s, %s, %s, %s, %s)",(full_name, age, gender, teacher_id, branch, dob))
        mysql.commit()
        messagebox.showinfo("Successfull","Data Updated Successfully")
        master.switch_frame(StartPage)
        
    except mq.Error as e :
        print("Error",e)
        

def deleteData(id,master):
    
    try:
        query = "Delete from teacher where teacher_id = %s"
        mycursor.execute(query,id)
        mysql.commit()
        messagebox.showinfo("Successfull","Data Deleted Successfully")
        master.switch_frame(StartPage)

    except mq.Error as e :
            print("Error",e)
    

def getData(branch,gender):

    if branch == "All Branches" and gender == "All Teachers":
        mycursor.execute("SELECT * from teacher")

    elif branch == "All Branches":
        mycursor.execute("SELECT * from teacher Where gender=%s",(gender))
    elif branch == "All Teachers":
        mycursor.execute("SELECT * from teacher Where branch=%s",(branch))

    else:
        mycursor.execute("SELECT * from teacher Where branch=%s and gender = %s",(branch,gender))
    result = mycursor.fetchall()
    return result

def displayData(branch,gender,master,self):

    
    g=[]

    teacherList=getData(branch,gender)

    parameter = ("ID","Name","Age","Gender","Branch","Birth Date")
    
    

    

    for i in range(len(parameter)):
        e = Entry(self,width=20,fg='black',font=('Arial',16,'bold'),justify='center')
        e.grid(row=2,column=i)
        e.insert(tk.END,parameter[i])

    

    for i in range(len(teacherList)):
        f=[]
        for j in range(len(teacherList[i])):
            f.append(Entry(self,width=20,fg='blue',font=('Arial',16,'bold'),justify='center'))
            f[j].grid(row=i+3,column=j)
            f[j].insert(tk.END,teacherList[i][j])
            f[j].configure(state="disabled")

        g.append(f)

    # print(g)

    clearbtn = tk.Button(self,text="Clear" ,width=9,font=("Ariel",12),command=lambda: clear(g))
    clearbtn.grid (row=1, column=2,  padx=(10, 5), pady=10)


def clear(g):
    for i in range(len(g)):
        for j in range(len(g[i])):
            g[i][j].destroy()

    

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class,id=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self,id)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self.geometry("1500x750")
        

class StartPage(tk.Frame):
    def __init__(self, master,id=None):
        tk.Frame.__init__(self, master)
        self.config(width=500,height=500)
        

        button = tk.Button(self,text="Enter Teacher Data",height=5,width=37,font=("Ariel",15),command=lambda: master.switch_frame(PageOne))
        button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        button2 = tk.Button(self,text="View Teacher Data" ,height=5,width=37,font=("Ariel",15),command=lambda: master.switch_frame(PageTwo))
        button2.place (relx=0.5, rely=0.5, anchor=tk.CENTER)

        button3 = tk.Button(self,text="Delete/Update Teacher Data" ,height=5,width=37,font=("Ariel",15),command=lambda: master.switch_frame(PageThree))
        button3.place (relx=0.5, rely=0.8, anchor=tk.CENTER)
        
        

class PageOne(tk.Frame):
    def __init__(self, master,id=None):
        tk.Frame.__init__(self, master)

        branch_list = ["Computer Engineering", "Mechanical Engineering", "Electrical Engineering","Civil Engineering","Autombile Enginnering"]
        value_inside = tk.StringVar(self)
        value_inside.set("Select an option")

        label_name = tk.Label(self, text="Teacher Registration", font=("Arial", 18))
        label_name.grid(row=0, column=0, columnspan=2, pady=10)

        label_full_name = tk.Label(self, text="Full Name:", font=("Arial", 12))
        label_full_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_full_name = tk.Entry(self, font=("Arial", 12))
        entry_full_name.grid(row=1, column=1, padx=10, pady=5)

        label_age = tk.Label(self, text="Age:", font=("Arial", 12))
        label_age.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_age = tk.Entry(self, font=("Arial", 12))
        entry_age.grid(row=2, column=1, padx=10, pady=5)

        label_gender = tk.Label(self, text="Gender:", font=("Arial", 12))
        label_gender.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        x = tk.StringVar(self,"MALE")
        entry_gender_m = tk.Radiobutton(self, text="Male", font=("Arial", 12), variable=x, value="MALE")
        entry_gender_m.grid(row=3, column=1)
        entry_gender_f = tk.Radiobutton(self, text="Female", font=("Arial", 12), variable=x, value="FEMALE")
        entry_gender_f.grid(row=3, column=2)

        label_ID = tk.Label(self, text="Teacher ID:", font=("Arial", 12))
        label_ID.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_ID = tk.Entry(self, font=("Arial", 12))
        entry_ID.grid(row=4, column=1, padx=10, pady=5)

        label_branch = tk.Label(self, text="Branch:", font=("Arial", 12))
        label_branch.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        bm = tk.OptionMenu(self, value_inside, *branch_list)
        bm.grid(row=5, column=1, padx=10, pady=5)

        label_dob = tk.Label(self, text="D.O.B:", font=("Arial", 12))
        label_dob.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        entry_dob = Calendar(self, selectmode='day', year=2020, month=5, day=22)
        entry_dob.grid(row=6, column=1, padx=10, pady=5)

        button_back = tk.Button(self, text="Back", font=("Arial", 15), width=10,command=lambda: master.switch_frame(StartPage))
        button_back.grid(row=7, column=0, padx=(10, 5), pady=10)

        button_submit = tk.Button(self, width=10,text="Submit", font=("Arial", 15),command=lambda: insertData(entry_full_name.get(), entry_age.get(),
                                                             x.get(), entry_ID.get(), value_inside.get(),
                                                             entry_dob.get_date(),master))
        button_submit.grid(row=7, column=1, padx=(5, 10), pady=60)

    
class PageTwo(tk.Frame):
    def __init__(self, master,id=None):
        tk.Frame.__init__(self, master)

        filter = tk.Label(self, text="Select Filters : ", font=("Arial", 12))
        filter.grid(row=0, column=0, sticky="e", padx=10, pady=5)

        branch_list = ["Computer Engineering", "Mechanical Engineering", "Electrical Engineering","All Branches","Civil Engineering","Autombile Enginnering"]
        value_inside1 = tk.StringVar(self)
        value_inside1.set("All Branches")


        gender_list = ["Male","Female","All Teachers"]
        value_inside2 = tk.StringVar(self)
        value_inside2.set("All Teachers")

        bm = tk.OptionMenu(self, value_inside1, *branch_list)
        bm.grid(row=0, column=1, padx=10, pady=5)

        gm = tk.OptionMenu(self, value_inside2, *gender_list)
        gm.grid(row=0, column=2, padx=10, pady=5)

        button_back = tk.Button(self, text="Back", width=9,font=("Arial", 12), command=lambda: master.switch_frame(StartPage))
        button_back.grid(row=1, column=0, padx=(10, 5), pady=10)

        submit_button = tk.Button(self, text="Display Data",width=10,font=("Arial", 12),command=lambda:displayData(value_inside1.get(),value_inside2.get(),master,self))
        submit_button.grid(row=1, column=1,  padx=(20, 5), pady=10)

            
class PageThree(tk.Frame):
    def __init__(self, master,id=None):
        tk.Frame.__init__(self, master)

        

        title = tk.Label(self, text="Delete/Update Teacher Data", font=("Arial", 18))
        title.grid(row=0, column=1, columnspan=3, pady=10)

        label1 = tk.Label(self, text="Enter Teacher ID  : ", font=("Arial", 12))
        label1.grid(row=1, column=0, columnspan=2, pady=10,padx=10)

        deleteId = tk.Entry(self, font=("Arial", 12))
        deleteId.grid(row=1, column=2, padx=10, pady=5)

        button_back = tk.Button(self, text="Back", width=10,font=("Arial", 15), command=lambda: master.switch_frame(StartPage))
        button_back.grid(row=2, column=1, padx=(10, 5), pady=10)

        submit_button = tk.Button(self, text="Submit",width=10,font=("Arial", 15),command=lambda: dataManipulate(deleteId.get(),master,self))
        submit_button.grid(row=2, column=2,  padx=(20, 5), pady=10)

        
class UpdatePage(tk.Frame):
    def __init__(self, master,updateId=None):
        tk.Frame.__init__(self, master)

        mycursor.execute("SELECT * FROM teacher WHERE teacher_id = %s", (updateId))
        teacher_data = mycursor.fetchone()

        branch_list = ["Computer Engineering", "Mechanical Engineering", "Electrical Engineering","Civil Engineering","Autombile Enginnering"]
        value_inside = tk.StringVar(self)
        value_inside.set("Select an option")

        label_name = tk.Label(self, text="Teacher Registration", font=("Arial", 18))
        label_name.grid(row=0, column=0, columnspan=2, pady=10)

        label_full_name = tk.Label(self, text="Full Name:", font=("Arial", 12))
        label_full_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_full_name = tk.Entry(self, font=("Arial", 12))
        entry_full_name.insert(0, teacher_data[1])
        entry_full_name.grid(row=1, column=1, padx=10, pady=5)

        label_age = tk.Label(self, text="Age:", font=("Arial", 12))
        label_age.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_age = tk.Entry(self, font=("Arial", 12))
        entry_age.insert(0, teacher_data[2])
        entry_age.grid(row=2, column=1, padx=10, pady=5)

        label_gender = tk.Label(self, text="Gender:", font=("Arial", 12))
        label_gender.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        # x = tk.StringVar(self,"MALE")

        x = tk.StringVar(self)
        x.set(teacher_data[3]) 
        
        entry_gender_m = tk.Radiobutton(self, text="Male", font=("Arial", 12), variable=x, value="MALE")
        entry_gender_m.grid(row=3, column=1)
        entry_gender_f = tk.Radiobutton(self, text="Female", font=("Arial", 12), variable=x, value="FEMALE")
        entry_gender_f.grid(row=3, column=2)

        label_branch = tk.Label(self, text="Branch:", font=("Arial", 12))
        label_branch.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        bm = tk.OptionMenu(self, value_inside, *branch_list)
        bm.grid(row=5, column=1, padx=10, pady=5)

        label_dob = tk.Label(self, text="D.O.B:", font=("Arial", 12))
        label_dob.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        entry_dob = Calendar(self, selectmode='day', year=2020, month=5, day=22)
        entry_dob.grid(row=6, column=1, padx=10, pady=5)

        button_back = tk.Button(self, text="Back", font=("Arial", 15), width=10,command=lambda: master.switch_frame(StartPage))
        button_back.grid(row=7, column=0, padx=(10, 5), pady=10)

        button_submit = tk.Button(self, width=10,text="Update", font=("Arial", 15),command=lambda: update(entry_full_name.get(), entry_age.get(),
                                                             x.get(),  value_inside.get(),
                                                             entry_dob.get_date(),updateId,master))
        button_submit.grid(row=7, column=1, padx=(5, 10), pady=60)

    




if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
