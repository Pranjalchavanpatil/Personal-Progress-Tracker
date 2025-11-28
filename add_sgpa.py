from customtkinter import *
from PIL import Image, ImageTk
from tkinter import ttk 
import mysql.connector
from tkinter import messagebox
from math import e


def validate_integer_input(new_value):
    
    if new_value == "" or new_value.isdigit():
        return True
    return False

class sgpa:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x460+80+400")
        self.root.resizable(False, False)
        #self.root.grab_set()
        
        validate_command = root.register(validate_integer_input)

        self.var_sem=StringVar()
        self.var_sgpa=StringVar()
        self.var_cgpa=StringVar()
        
        
    #----------------------------title---------------------------------------------------------
        
       # title = CTkLabel(self.root, text="MARKS", font=("goudy old style", 25, "bold", "underline"),height=50, bg_color="white", fg_color="dodgerblue")
        #title.place(x=0, y=0, relwidth=1)
        
        
        #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
        
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0)
       
        #---------------------------- sgpa frame--------------------------------------------------------

        frame1=CTkFrame(self.root, width=1080, height=430, border_width=2,fg_color="azure")
        frame1.place(x=150, y=20)

        frame2=CTkFrame(frame1, width=500, height=360, border_width=2,fg_color="azure")
        frame2.place(x=40, y=50)
        title1 = CTkLabel(frame2, text="SGPA Entry", font=("goudy old style",22, "bold"),height=35, bg_color="black")
        title1.place(x=0, y=0, relwidth=1)

        sem_lbl=CTkLabel(frame2,text="Enter Sem:",text_color="black",font=("goudy old style", 22),fg_color="azure")
        sem_lbl.place(x=20, y=80)
        all_sem=["sem 1","sem 2","sem 3","sem 4","sem 5","sem 6","sem 7","sem 8"]
        self.semester=CTkComboBox(frame2,variable=self.var_sem,values=all_sem,height=30,width=250,text_color="black",state="readonly",font=("helvetica", 18),fg_color="azure")
        self.semester.place(x=200,y=55)
        self.semester.set("sem 1") 
        self.semester.place(x=170,y=80)
        
        sgpa_lbl=CTkLabel(frame2,text="Enter SGPA:",text_color="black",font=("goudy old style", 22))
        sgpa_lbl.place(x=20, y=130)
        self.sgpa=CTkEntry(frame2,placeholder_text="enter SGPA here...",textvariable=self.var_sgpa,text_color="black",height=30,width=200,font=("arial",15),fg_color="azure")
        self.sgpa.place(x=170,y=130)

    
#---------------------------- btn frame--------------------------------------------------------

        save_btn=CTkButton(frame2, text="SAVE",command=self.mrks_Add, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        save_btn.place(x=40, y=190)
        update_btn=CTkButton(frame2, text="UPDATE",command=self.update, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        update_btn.place(x=180, y=190)
       
        reset_btn=CTkButton(frame2, text="RESET",command=self.reset, cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        reset_btn.place(x=310, y=190)

        
        cgpa_lbl=CTkLabel(frame2,text="CGPA :",text_color="black",font=("goudy old style", 22),fg_color="azure")
        cgpa_lbl.place(x=140,y=260)
        cgpa_entry=CTkEntry(frame2,placeholder_text="Enter SGPA",textvariable=self.var_cgpa,text_color="black",font=("goudy old style", 22),fg_color="azure")
        cgpa_entry.place(x=220,y=260)

        cgpa_calc_btn=CTkButton(frame2, text="CALCULATE",cursor="hand2", font=("goudy old style", 18, "bold"),command=self.calculate_cgpa)
        cgpa_calc_btn.place(x=170, y=310)

#---------------------------- table frame--------------------------------------------------------


        tble_frm=CTkFrame(frame1,width=480,height=390,border_width=2,fg_color="azure")
        tble_frm.place(x=570,y=20)

        #fdb_form_l=CTkFrame(tble_frm, width=600, height=40, border_width=2,fg_color="azure")
       # fdb_form_l.place(x=20, y=10)

    



        tbl_frame=CTkFrame(tble_frm,width=460,height=370,border_width=2,fg_color="azure")
        tbl_frame.place(x=10,y=10)
        tbl_frame.pack_propagate(False)

        scr_x=CTkScrollbar(tbl_frame,orientation=HORIZONTAL)
        scr_y=CTkScrollbar(tbl_frame,orientation=VERTICAL)

        self.table=ttk.Treeview(tbl_frame,columns=("sem","sgpa"),xscrollcommand=scr_x.set,yscrollcommand=scr_y.set)
        scr_x.pack(side=BOTTOM,fill="x")
        scr_y.pack(side=RIGHT,fill="y")

        scr_x.configure(command=self.table.xview)
        scr_y.configure(command=self.table.yview)

        
        self.table.column("sem", width=70, anchor='center')
        self.table.column("sgpa", width=200, anchor='center')
       
        
        
        self.table.heading("sem",text="Sem")
        self.table.heading("sgpa",text="SGPA")
       

        self.table["show"]="headings"
        self.table.pack(fill="both",expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13), foreground="black", background="white")
        style.configure("Treeview.Heading", font=("Arial", 16), foreground="black", background="green")
        style.configure("Treeview", rowheight=30)
        
        

        separator = ttk.Separator(self.table, orient='vertical')
        separator.place(x=250, y=0, relwidth=0, relheight=1)
        
        
        separator = ttk.Separator(self.table, orient='horizontal')
        separator.place(x=0, y=25, relwidth=1, relheight=0)
        
        self.fetch_data()
        self.table.bind("<ButtonRelease>",self.select_data)


    
#-----------------------------------add data---------------------------------------------------------------------
        
    def mrks_Add(self):

                if(self.var_sem.get()=="" or  self.var_sgpa.get()=="" ):
                        messagebox.showerror("Error","please enter data",parent=self.root)
                else:
                        try:
                                db = mysql.connector.connect(
                                host="localhost",          
                                user="root",      
                                password="Satya@9632",  
                                database="my_project"  
                                )
                                cursor = db.cursor()

                                # Create  table if it doesn't exist
                                
                                
                                cursor.execute('''
                                        INSERT INTO sgpa (Sem, sgpa)
                                        VALUES (%s, %s)
                                        ''',(self.var_sem.get(),self.var_sgpa.get()))
                        
                                        

                        
                                db.commit()
                                self.fetch_data()
                                db.close()
                                messagebox.showinfo("Success","Data Added Succesfully..",parent=self.root)

                        except Exception as es:
                                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

#-----------------------------------fetch data---------------------------------------------------------------------


    def fetch_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        db = mysql.connector.connect(
                    host="localhost",          
                    user="root",      
                    password="Satya@9632",  
                    database="my_project"  
                )
        cursor = db.cursor()
        cursor.execute("select * from sgpa")
        data=cursor.fetchall()

        
        for i in data:
            self.table.insert("",END,values=i)
        db.commit()
        
        db.close()

    #----------------------------reset----------------------------------------------------------------------

    def reset(self):
        self.sem_entry.delete(0,END)
        self.sgpa.delete(0,END)
        
       
     #----------------------------select_data-------------------------------------------------------
    
    def select_data(self,event=""):
         cursor_row=self.table.focus()
         content=self.table.item(cursor_row)
         data=content["values"]
        
         self.var_sem.set(data[0])
         self.var_sgpa.set(data[1])
         

   

    #----------------------------update_data------------------------------------------------------- 

    def update(self):
         try:
                 update=messagebox.askyesno("update", "Are you sure you want to Update this Data",parent=self.root)
                 if update==1:
                   db=mysql.connector.connect(host="localhost",
                                                user="root",
                                                password="Satya@9632",
                                                database="my_project")
                   cursor = db.cursor()
                   cursor.execute("update sgpa set sgpa=%s where sem=%s",(self.var_sgpa.get(),self.var_sem.get()))
                  

                   

                   db.commit()
                   self.fetch_data()
                   db.close()
                   messagebox.showinfo("Success","Data updated Succesfully..",parent=self.root)
                   
              
                                        
         except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def calculate_cgpa(self):
        db = mysql.connector.connect(host="localhost",
                                            user="root",
                                            password="Satya@9632",
                                            database="my_project")
        cursor = db.cursor()
        
        
        cursor = db.cursor()
        cursor.execute("SELECT sgpa FROM sgpa")
        data = cursor.fetchall()
        db.close()
        
        sgpas = [float(row[0]) for row in data]
        cgpa = sum(sgpas) / len(sgpas)
        self.var_cgpa.set(round(cgpa, 2))
                   

    def hide(self):
        """Method to hide the Toplevel window."""
        self.root.withdraw()

    def show(self):
        """Method to show the Toplevel window."""
        self.root.deiconify() 
        

if __name__ == "__main__":
    root = CTk()
    obj = sgpa(root)
    root.mainloop()
