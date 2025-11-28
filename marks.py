from customtkinter import *
from PIL import Image, ImageTk
from add_sgpa import sgpa
from tkinter import ttk 
import mysql.connector
from tkinter import messagebox


def validate_integer_input(new_value):
    
    if new_value == "" or new_value.isdigit():
        return True
    return False

class mark:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x560+80+220")
        #self.root.resizable(False, False)
        validate_command = root.register(validate_integer_input)

        self.new_win = None

        self.var_code=StringVar()
        self.var_Name=StringVar()
        self.var_mrks=StringVar()
        self.var_sem_search=StringVar()
        
        
    #----------------------------title---------------------------------------------------------
        
        title = CTkLabel(self.root, text="MARKS", font=("goudy old style", 25, "bold", "underline"),height=50, bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)
        
        
        #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
        
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=50)
        #----------------------------semester--------------------------------------------------------

        marks_btn=CTkButton(self.root,text="Marks",cursor="hand2",font=("goudy old style", 20, "bold"), height=35, width=140,command=self.add_mrks) 
        marks_btn.place(x=490, y=70)
       
        sgpa_btn=CTkButton(self.root,text="SGPA",cursor="hand2",font=("goudy old style", 20, "bold"), height=35, width=140,command=self.add_sgpa) 
        sgpa_btn.place(x=750, y=70)


        all_sem=["sem 1","sem 2","sem 3","sem 4","sem 5","sem 6","sem 7","sem 8"]
        self.semester=CTkComboBox(self.root,variable=self.var_sem_search,values=all_sem,height=30,width=250,state="readonly",font=("helvetica", 18))
        self.semester.place(x=200,y=150)
        self.semester.set("Enter Semester")

        #----------------------------enter data ---------------------------------------------------------
        frame1=CTkFrame(self.root, width=520, height=300, border_width=2,fg_color="azure")
        frame1.place(x=60, y=190)
        title1 = CTkLabel(frame1, text="Marks Entry", font=("goudy old style",22, "bold"),height=35, bg_color="black")
        title1.place(x=0, y=0, relwidth=1)
        
        sub_Lno=CTkLabel(frame1,text="Enter sub code:",text_color="black",font=("goudy old style", 22),fg_color="azure")
        sub_Lno.place(x=20, y=50)
        self.sub_code=CTkEntry(frame1,placeholder_text="enter sub code here...",textvariable=self.var_code,text_color="black",height=30,width=177,font=("arial",15),fg_color="azure")
        self.sub_code.place(x=170,y=50)
        
        sub_lbl=CTkLabel(frame1,text="Enter subject:",text_color="black",font=("goudy old style", 22))
        sub_lbl.place(x=20, y=100)
        self.sub_name=CTkEntry(frame1,placeholder_text="enter subject here...",textvariable=self.var_Name,text_color="black",height=30,width=200,font=("arial",15),fg_color="azure")
        self.sub_name.place(x=170,y=100)

        sub_mrks=CTkLabel(frame1,text="Enter marks:",text_color="black",font=("goudy old style", 22))
        sub_mrks.place(x=20, y=150)
        self.sub_m_entry=CTkEntry(frame1,validate="key",validatecommand=(validate_command, '%P'),textvariable=self.var_mrks,height=30,width=150,placeholder_text="123",text_color="black",font=("arial",15),fg_color="azure",bg_color="azure")
        self.sub_m_entry.place(x=170,y=150)
        
        #----------------------------buttons---------------------------------------------------------
        
        save_btn=CTkButton(frame1, text="SAVE",command=self.mrks_Add, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        save_btn.place(x=20, y=220)
        update_btn=CTkButton(frame1, text="UPDATE",command=self.update, cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        update_btn.place(x=150, y=220)
       
        reset_btn=CTkButton(frame1, text="RESET",command=self.reset, cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        reset_btn.place(x=280, y=220)

        self.root.bind("<Unmap>", self.minimize_child_window)
        self.root.bind("<Map>", self.restore_child_window)
        
        #----------------------------table frame---------------------------------------------------------

        tble_frm=CTkFrame(self.root,width=650,height=400,border_width=2,fg_color="azure")
        tble_frm.place(x=650,y=150)

        fdb_form_l=CTkFrame(tble_frm, width=600, height=40, border_width=2,fg_color="azure")
        fdb_form_l.place(x=20, y=10)

    
        #variables
        self.var_com_search=StringVar()

        skill_type=CTkLabel(fdb_form_l,text="Search By :",text_color="black",font=("goudy old style", 20),fg_color="azure")
        skill_type.place(x=5, y=5) 
        search_by=["sem","sub_code","sub_name"]
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


        tbl_frame=CTkFrame(tble_frm,width=610,height=330,border_width=2,fg_color="azure")
        tbl_frame.place(x=20,y=65)
        tbl_frame.pack_propagate(False)

        scr_x=CTkScrollbar(tbl_frame,orientation=HORIZONTAL)
        scr_y=CTkScrollbar(tbl_frame,orientation=VERTICAL)

        self.table=ttk.Treeview(tbl_frame,columns=("sem","code","name","mrk"),xscrollcommand=scr_x.set,yscrollcommand=scr_y.set)
        scr_x.pack(side=BOTTOM,fill="x")
        scr_y.pack(side=RIGHT,fill="y")

        scr_x.configure(command=self.table.xview)
        scr_y.configure(command=self.table.yview)

        
        self.table.column("sem", width=70, anchor='center')
        self.table.column("code", width=200, anchor='center')
        self.table.column("name", width=200, anchor='center')
        self.table.column("mrk", width=100, anchor='center')
        
        
        self.table.heading("sem",text="Sem")
        self.table.heading("code",text="Subject code")
        self.table.heading("name",text="sunject Name")
        self.table.heading("mrk",text="Marks",anchor="center")

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



#-----------------------------------add data---------------------------------------------------------------------
        
    def mrks_Add(self):

                if(self.var_sem_search.get()=="Enter Semester" or self.var_code.get()=="" or  self.var_mrks.get()=="" ):
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
                                        INSERT INTO marks (Sem, sub_code, sub_Name, marks)
                                        VALUES (%s, %s, %s, %s)
                                        ''',(self.var_sem_search.get(),self.var_code.get(),self.var_Name.get(),self.var_mrks.get()))
                        
                                        

                        
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
        cursor.execute("select * from marks")
        data=cursor.fetchall()

        
        for i in data:
            self.table.insert("",END,values=i)
        db.commit()
        
        db.close()

    #----------------------------reset----------------------------------------------------------------------

    def reset(self):
        self.sub_code.delete(0,END)
        self.sub_name.delete(0,END)
        self.sub_m_entry.delete(0,END)
        self.semester.set("sem 1")
        
        self.search_byy1.set("search by")
        self.search_entry.delete(0,END)
       
     #----------------------------select_data-------------------------------------------------------
    
    def select_data(self,event=""):
         cursor_row=self.table.focus()
         content=self.table.item(cursor_row)
         data=content["values"]
        
         self.var_sem_search.set(data[0])
         self.var_code.set(data[1])
         self.var_Name.set(data[2])
         self.var_mrks.set(data[3])

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
                    cursor.execute("select * from marks where "+str(self.var_com_search.get())+ "  = %s", (self.var_searchbox.get(),))
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
                   cursor.execute("update marks set marks=%s where sub_code=%s",(self.var_mrks.get(),self.var_code.get()))
                  

                   

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

    def close_current_window(self):
        if hasattr(self, 'new_win'):
            
            if self.new_win is not None and self.new_win.winfo_exists():
                self.new_win.destroy()
                self.new_win = None 

    def minimize_child_window(self, event=None):
        """Minimize the child window when the main window is minimized."""
        if self.new_win is not None:
            self.new_win.withdraw()  # Minimize the child window (hide it)

    def restore_child_window(self, event=None):
        """Restore the child window when the main window is restored."""
        if self.new_win is not None:
            self.new_win.deiconify()

    def close_current_window(self):
        if hasattr(self, 'new_win'):
            
            if self.new_win is not None and self.new_win.winfo_exists():
                self.new_win.destroy()
                self.new_win = None 

    def add_sgpa(self):
        self.close_current_window()
        self.new_win=CTkToplevel(self.root)
        
        self.new_obj=sgpa(self.new_win)
        self.new_win.attributes('-topmost',True)
        self.new_win.focus_force()
        self.new_win.overrideredirect(True)
        

    def add_mrks(self):
        if hasattr(self, 'new_win'):
            self.new_win.destroy()
        

if __name__ == "__main__":
    root = CTk()
    obj = mark(root)
    root.mainloop()
