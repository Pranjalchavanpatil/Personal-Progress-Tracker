from customtkinter import *
from PIL import Image, ImageTk
from tkinter import ttk 
import mysql.connector
from tkinter import messagebox


class skill:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x550+80+280")
        #self.root.resizable(False, False)

     #----------------------------title---------------------------------------------------------
        
        title = CTkLabel(self.root, text="SKILLS", font=("goudy old style", 25, "bold", "underline"),height=50, bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)

 #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
        
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=50)

 #----------------------------semester--------------------------------------------------------
        self.var_sem_search=StringVar()
        all_sem=["sem 1","sem 2","sem 3","sem 4","sem 5","sem 6","sem 7","sem 8"]
        self.semester=CTkComboBox(self.root,variable=self.var_sem_search,values=all_sem,height=30,width=250,text_color="black",state="readonly",font=("helvetica", 18),fg_color="cadetblue1",bg_color="cadetblue2")
        self.semester.place(x=250,y=80)
        self.semester.set("sem 1") 

#----------------------------variables ---------------------------------------------------------
        self.var_skill_type=StringVar()
        self.var_skill_Name=StringVar()
        self.var_progress=StringVar()
        self.var_sno=StringVar()

#----------------------------FRAME 2 ---------------------------------------------------------
        frame2=CTkFrame(self.root, width=430, height=360, border_width=2,fg_color="azure")
        frame2.place(x=130, y=130) 
        title3 = CTkLabel(frame2, text="Tasks Completed", font=("goudy old style",22, "bold"),height=35, bg_color="black")
        title3.place(x=0, y=0, relwidth=1) 
   
        
        
        skill_no=CTkLabel(frame2,text="Sno:",text_color="black",font=("goudy old style", 22),fg_color="azure")
        skill_no.place(x=20, y=60)  
        
        self.sno_entry=CTkEntry(frame2,textvariable=self.var_sno,text_color="black",height=30,width=50,font=("arial",15),fg_color="azure")
        self.sno_entry.place(x=70,y=60)
        


        skill_type1=CTkLabel(frame2,text="Skill Type:",text_color="black",font=("goudy old style", 22),fg_color="azure")
        skill_type1.place(x=20, y=100)  
        
        self.skill_type_entry_1=CTkEntry(frame2,placeholder_text="enter type of skill here...",textvariable=self.var_skill_type,text_color="black",height=30,width=177,font=("arial",15),fg_color="azure")
        self.skill_type_entry_1.place(x=120,y=100)
        
        skill_lbl1=CTkLabel(frame2,text="Enter Skill:",text_color="black",font=("goudy old style", 22))
        skill_lbl1.place(x=20, y=150)
        self.skill_entry1=CTkEntry(frame2,placeholder_text="enter Skill here...",textvariable=self.var_skill_Name,text_color="black",height=30,width=200,font=("arial",15),fg_color="azure")
        self.skill_entry1.place(x=130,y=150)

        prog_lbl1=CTkLabel(frame2,text="Your Progress:",text_color="black",font=("goudy old style", 22))
        prog_lbl1.place(x=20, y=200)

        progress=["In Progress","Completed","Incomplete"]
        self.prog=CTkComboBox(frame2,values=progress,height=30,width=250,variable=self.var_progress,text_color="black",state="readonly",font=("helvetica", 18),fg_color="azure")
        self.prog.place(x=150,y=200)
        self.prog.set("Incomplete") 
        


#----------------------------buttons---------------------------------------------------------
        
        save_btn=CTkButton(frame2, text="SAVE",command=self.Add_data, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        save_btn.place(x=20, y=270)
        update_btn=CTkButton(frame2, text="UPDATE",command=self.update, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        update_btn.place(x=150, y=270)
       
        reset_btn=CTkButton(frame2, text="RESET",command=self.reset, cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        reset_btn.place(x=280, y=270)

        #------------------------------------Table Form-----------------------------------------------------------------------

        tble_frm=CTkFrame(self.root,width=650,height=470,border_width=2,fg_color="azure")
        tble_frm.place(x=630,y=60)

        fdb_form_l=CTkFrame(tble_frm, width=600, height=40, border_width=2,fg_color="azure")
        fdb_form_l.place(x=20, y=10)

    
        #variables
        self.var_com_search=StringVar()

        skill_type=CTkLabel(fdb_form_l,text="Search By :",text_color="black",font=("goudy old style", 20),fg_color="azure")
        skill_type.place(x=5, y=5) 
        search_by=["Skill_Name","Progress"]
        self.search_byy1=CTkComboBox(fdb_form_l,values=search_by,height=30,width=140,variable=self.var_com_search,state="readonly",text_color="black",font=("goudy old style", 18),fg_color="azure")
        self.search_byy1.place(x=98,y=5)
        self.search_byy1.set("search by")
        
        self.var_searchbox=StringVar()
        self.search_entry=CTkEntry(fdb_form_l,textvariable=self.var_searchbox,placeholder_text="Search Here... ",text_color="black",height=30,width=130,font=("arial",15),fg_color="azure")
        self.search_entry.place(x=245,y=5)

        search_btn=CTkButton(fdb_form_l, text="SEARCH",command=self.search_data,cursor="hand2",font=("goudy old style", 18, "bold"), height=10, width=90)
        search_btn.place(x=380, y=6)
        
        showall_btn=CTkButton(fdb_form_l, text="SHOW ALL",command=self.fetch_data,cursor="hand2", font=("goudy old style", 18, "bold"), height=10, width=80)
        showall_btn.place(x=480, y=6)


        tbl_frame=CTkFrame(tble_frm,width=610,height=400,border_width=2,fg_color="azure")
        tbl_frame.place(x=20,y=65)
        tbl_frame.pack_propagate(False)

        scr_x=CTkScrollbar(tbl_frame,orientation=HORIZONTAL)
        scr_y=CTkScrollbar(tbl_frame,orientation=VERTICAL)

        self.table=ttk.Treeview(tbl_frame,columns=("sno","sem","skill type","skill name","progress"),xscrollcommand=scr_x.set,yscrollcommand=scr_y.set)
        scr_x.pack(side=BOTTOM,fill="x")
        scr_y.pack(side=RIGHT,fill="y")

        scr_x.configure(command=self.table.xview)
        scr_y.configure(command=self.table.yview)

        
        self.table.column("sno", width=50, anchor='center')
        self.table.column("sem", width=70, anchor='center')
        self.table.column("skill type", width=200, anchor='center')
        self.table.column("skill name", width=200, anchor='center')
        self.table.column("progress", width=200)
        
        self.table.heading("sno",text="Sno")
        self.table.heading("sem",text="Sem")
        self.table.heading("skill type",text="Skill Type")
        self.table.heading("skill name",text="Skill Name")
        self.table.heading("progress",text="Progress",anchor="center")

        self.table["show"]="headings"
        self.table.pack(fill="both",expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13), foreground="black", background="white")
        style.configure("Treeview.Heading", font=("Arial", 16), foreground="black", background="green")
        style.configure("Treeview", rowheight=30)
        
        

      
        separator = ttk.Separator(self.table, orient='horizontal')
        separator.place(x=0, y=25, relwidth=1, relheight=0)
        
        self.fetch_data()

        self.table.bind("<ButtonRelease>",self.select_data)

         #----------------------------ADD_data-------------------------------------------------------      

    def Add_data(self):

                if(self.var_skill_Name.get()=="" ):
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
                                        INSERT INTO skills (Sem, Skill_Type, Skill_Name, Progress)
                                        VALUES (%s, %s, %s, %s)
                                        ''',(self.var_sem_search.get(),self.var_skill_type.get(),self.var_skill_Name.get(),self.var_progress.get()))
                        
                                        

                        
                                db.commit()
                                self.fetch_data()
                                db.close()
                                messagebox.showinfo("Success","Data Added Succesfully..",parent=self.root)

                        except Exception as es:
                                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

   #----------------------------fetch_data-------------------------------------------------------      
                 
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
        cursor.execute("select * from skills")
        data=cursor.fetchall()

        
        for i in data:
            self.table.insert("",END,values=i)
        db.commit()
        
        db.close()

  #----------------------------reset----------------------------------------------------------------------

    def reset(self):
        self.skill_entry1.delete(0,END)
        self.skill_type_entry_1.delete(0,END)
        self.prog.set("Incomplete")
        self.semester.set("sem 1")
        self.search_byy1.set("search by")
        self.search_entry.delete(0,END)
        self.sno_entry.delete(0,END)
     #----------------------------select_data-------------------------------------------------------
    
    def select_data(self,event=""):
         cursor_row=self.table.focus()
         content=self.table.item(cursor_row)
         data=content["values"]
         self.var_sno.set(data[0])
         self.var_sem_search.set(data[1])
         self.var_skill_type.set(data[2])
         self.var_skill_Name.set(data[3])
         self.var_progress.set(data[4])

    #----------------------------search_data-------------------------------------------------------
    
    def search_data(self):
            if(self.var_com_search.get()=="" or self.var_searchbox.get()==""):
                messagebox.showerror("Error","please select option",parent=self.root)
            else:
                try:
                    db = mysql.connector.connect(
                    host="localhost",          
                    user="root",      
                    password="Satya@9632",  
                    database="my_project"  
                    )
                    cursor = db.cursor()
                    cursor.execute("select * from skills where "+str(self.var_com_search.get())+ "  = %s", (self.var_searchbox.get(),))
                    data=cursor.fetchall()
                    if len(data) != 0:
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert("",END,values=i)
                        db.commit()
                    db.close()
                except Exception as es:
                    messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

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
                   cursor.execute("update skills set Progress=%s where Sno=%s",(self.var_progress.get(),self.var_sno.get()))
                   print(self.var_progress.get(), self.var_sno.get())

                   db.commit()
                   self.fetch_data()
                   db.close()
                   messagebox.showinfo("Success","Data updated Succesfully..",parent=self.root)
                   
              
                                        
         except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)
        
        

    def hide(self):
        """Method to hide the Toplevel window."""
        self.root.withdraw()

    def show(self):
        """Method to show the Toplevel window."""
        self.root.deiconify() 

if __name__ == "__main__":
    root = CTk()
    obj = skill(root)
    root.mainloop()
