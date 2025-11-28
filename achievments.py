from customtkinter import *
from PIL import Image, ImageTk
from tkinter import ttk 
import mysql.connector
from tkinter import messagebox




class achiev:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x550+80+280")
        #self.root.resizable(False, False)

        #variables
        self.var_special=StringVar()
        self.var_reward=StringVar()
        self.var_disc=StringVar()
        self.var_sem=StringVar()

 #----------------------------title---------------------------------------------------------
        
        title = CTkLabel(self.root, text="ACHIEVEMENTS", font=("goudy old style", 25, "bold", "underline"),height=50, bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)
        
 #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
        
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=50)



        

#----------------------------frame 1--------------------------------------------------------

        frame2=CTkFrame(self.root, width=530, height=400, border_width=2,fg_color="azure")
        frame2.place(x=80, y=100) 
        title3 = CTkLabel(frame2, text="Achievements", font=("goudy old style",22, "bold"),height=35, bg_color="black")
        title3.place(x=0, y=0, relwidth=1)   
 #----------------------------data--------------------------------------------------------       
        '''sno_type=CTkLabel(frame2,text="Enter S.no     :",text_color="black",font=("goudy old style", 22),fg_color="azure")
        sno_type.place(x=40, y=45)
        select_entry=CTkEntry(frame2,placeholder_text="enter S.no here...",textvariable=self.var_id,text_color="black",height=30,width=200,font=("arial",15),fg_color="azure")
        select_entry.place(x=200,y=45)'''

        sem_type=CTkLabel(frame2,text_color="black",text="Enter  semester  : ",font=("goudy old style", 22),fg_color="azure")
        sem_type.place(x=40, y=55)
        all_sem=["sem 1","sem 2","sem 3","sem 4","sem 5","sem 6","sem 7","sem 8"]
        self.semester=CTkComboBox(frame2,variable=self.var_sem,values=all_sem,height=30,width=250,text_color="black",state="readonly",font=("helvetica", 18),fg_color="azure")
        self.semester.place(x=200,y=55)
        self.semester.set("Enter Semester") 

        reward_type=CTkLabel(frame2,text="Reward Type     :",text_color="black",font=("goudy old style", 22),fg_color="azure")
        reward_type.place(x=40, y=150)  
        
        search_by=["Certificate","Rank","Prize"]
        self.search_byy=CTkComboBox(frame2,variable=self.var_reward,values=search_by,height=30,width=150,state="readonly",text_color="black",font=("goudy old style", 18),fg_color="azure")
        self.search_byy.place(x=200,y=150)
        self.search_byy.set("Select")
       
        
        select_lbl1=CTkLabel(frame2,text="Speciality Name :",text_color="black",font=("goudy old style", 22))
        select_lbl1.place(x=40, y=100)
        self.select_entry1=CTkEntry(frame2,placeholder_text="enter name here...",textvariable=self.var_special,text_color="black",height=30,width=200,font=("arial",15),fg_color="azure")
        self.select_entry1.place(x=200,y=100)

        self.select_lbl2=CTkLabel(frame2,text="Discription   :",text_color="black",font=("goudy old style", 22))
        self.select_lbl2.place(x=40, y=185)
        self.select_entry2=CTkEntry(frame2,text_color="black",textvariable=self.var_disc,placeholder_text="Discription",height=100,width=450,font=("arial",15),fg_color="white",border_width=3,border_color="black")
        self.select_entry2.place(x=40,y=220)


       #----------------------------buttons--------------------------------------------------------

        save_btn=CTkButton(frame2, text="SAVE",command=self.add_data, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        save_btn.place(x=130, y=340)
        reset_btn=CTkButton(frame2, text="RESET", cursor="hand2",command=self.reset ,font=("goudy old style", 18, "bold"), height=15, width=100)
        reset_btn.place(x=290, y=340)
        '''update_btn=CTkButton(frame2, text="UPDATE", cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        update_btn.place(x=270, y=340)
        delete_btn=CTkButton(frame2, text="DELETE", cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        delete_btn.place(x=390, y=340)'''

        #----------------------------table frame 1--------------------------------------------------------
        tble_frm=CTkFrame(self.root,width=650,height=470,border_width=2,fg_color="azure")
        tble_frm.place(x=680,y=60)

        fdb_form_l=CTkFrame(tble_frm, width=600, height=40, border_width=2,fg_color="azure")
        fdb_form_l.place(x=20, y=10)

    
        #variables
        self.var_com_search=StringVar()

        skill_type=CTkLabel(fdb_form_l,text="Search By :",text_color="black",font=("goudy old style", 20),fg_color="azure")
        skill_type.place(x=5, y=5) 
        search_by=["sem","speciality","reward_type"]
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

        self.table=ttk.Treeview(tbl_frame,columns=("id","sem","speciality","reward","discription"),xscrollcommand=scr_x.set,yscrollcommand=scr_y.set)
        scr_x.pack(side=BOTTOM,fill="x")
        scr_y.pack(side=RIGHT,fill="y")

        scr_x.configure(command=self.table.xview)
        scr_y.configure(command=self.table.yview)

        #self.table.heading("id",text="ID")
        self.table.column("id", width=50, anchor='center')
        self.table.column("sem", width=100, anchor='center')
        self.table.column("speciality", width=200, anchor='center')
        self.table.column("reward", width=250, anchor='center')
        self.table.column("discription", width=700)
        
        self.table.heading("id",text="SID")
        self.table.heading("sem",text="Sem")
        self.table.heading("speciality",text="Speciality Name")
        self.table.heading("reward",text="Reward Type")
        self.table.heading("discription",text="Discription",anchor="w")

        self.table["show"]="headings"
        self.table.pack(fill="both",expand=True)
        
        self.fetch_data()

        self.table.bind("<ButtonRelease>",self.select_data)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13), foreground="black", background="white")
        style.configure("Treeview.Heading", font=("Arial", 16), foreground="black", background="green")
        style.configure("Treeview", rowheight=30)
        
        

        
        separator = ttk.Separator(self.table, orient='horizontal')
        separator.place(x=0, y=25, relwidth=1, relheight=0)


#----------------------------add_data-------------------------------------------------------

    def add_data(self):
        if(self.var_sem.get()=="Enter Semester" or self.var_special.get()=="" or self.var_disc.get()=="" or self.var_reward.get()=="Select"):
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
                            INSERT INTO archiev (sem, speciality, reward_type, description)
                            VALUES (%s, %s, %s, %s)
                        ''',(self.var_sem.get(),self.var_special.get(),self.var_reward.get(),self.var_disc.get()))
                


                
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
        cursor.execute("select * from archiev")
        data=cursor.fetchall()

        
        for i in data:
            self.table.insert("",END,values=i)
        db.commit()
        db.close()
    
     #----------------------------select_data-------------------------------------------------------
    
    def select_data(self,event=""):
         cursor_row=self.table.focus()
         content=self.table.item(cursor_row)
         data=content["values"]

         self.var_sem.set(data[1])
         self.var_special.set(data[2])
         self.var_reward.set(data[3])
         self.var_disc.set(data[4])


    
  #----------------------------reset_data-------------------------------------------------------
    def reset(self):
     self.select_entry1.delete(0,END)
     self.select_entry2.delete(0,END)
     self.search_byy.set("Select")
     self.semester.set("Enter Semester")
     self.search_byy1.set("search by")
     self.search_entry.delete(0,END)

    
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
                    cursor.execute("select * from archiev where "+str(self.var_com_search.get())+" LIKE '%"+str(self.var_searchbox.get())+"%'")
                    data=cursor.fetchall()
                    if len(data) != 0:
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert("",END,values=i)
                        db.commit()
                    db.close()
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
    obj = achiev(root)
    root.mainloop()
