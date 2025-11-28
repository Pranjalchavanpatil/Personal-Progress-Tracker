from customtkinter import *
from PIL import Image, ImageTk
import mysql.connector
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk




class fdb:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x550+80+280")
        self.root.resizable(False, False)


        
        
         #----------------------------title---------------------------------------------------------
        
        title = CTkLabel(self.root, text="FEEDBACKS", font=("goudy old style", 25, "bold", "underline"),height=50, bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)

    #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
            
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=50)
    #----------------------------LABEL FRAME---------------------------------------------------------
        fdb_form_l=CTkFrame(self.root, width=1280, height=48, border_width=2,fg_color="azure")
        fdb_form_l.place(x=55, y=60)

    
        #variables
        self.var_com_search=StringVar()

        skill_type=CTkLabel(fdb_form_l,text="Search By  :",text_color="black",font=("goudy old style", 22),fg_color="azure")
        skill_type.place(x=300, y=10) 
        search_by=["email","profession"]    
        search_byy=CTkComboBox(fdb_form_l,values=search_by,height=30,width=150,variable=self.var_com_search,state="readonly",text_color="black",font=("goudy old style", 18),fg_color="azure")
        search_byy.place(x=400,y=10)
        search_byy.set("search by")
        
        self.var_searchbox=StringVar()
        select_entry=CTkEntry(fdb_form_l,textvariable=self.var_searchbox,placeholder_text="Search Here... ",text_color="black",height=30,width=250,font=("arial",15),fg_color="azure")
        select_entry.place(x=570,y=10)

        search_btn=CTkButton(fdb_form_l, text="SEARCH",command=self.search_data,cursor="hand2",font=("goudy old style", 18, "bold"), height=15, width=100)
        search_btn.place(x=840, y=10)
        
        showall_btn=CTkButton(fdb_form_l, text="SHOW ALL",command=self.fetch_data,cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        showall_btn.place(x=970, y=10)

        refresh_btn=CTkButton(fdb_form_l, text="REFRESH",command=self.refresh,cursor="hand2", font=("goudy old style", 18, "bold"), height=15, width=100)
        refresh_btn.place(x=1100, y=10)
    #----------------------------MAIN FRAME---------------------------------------------------------

        fdb_form=CTkFrame(self.root, width=1280, height=433, border_width=2,fg_color="azure")
        fdb_form.place(x=55, y=110)

        

    #----------------------------table FRAME and scroll bar ---------------------------------------------------------------------
        ''' right_frame=CTkFrame(fdb_form,width=710,height=400,border_width=2,fg_color="azure")
        tbl_frame.place(x=555,y=15)'''
        
        tbl_frame=CTkFrame(fdb_form,width=1100,height=400,border_width=2,fg_color="azure")
        tbl_frame.place(x=100,y=15)
        tbl_frame.pack_propagate(False)

        scr_x=CTkScrollbar(tbl_frame,orientation=HORIZONTAL)
        scr_y=CTkScrollbar(tbl_frame,orientation=VERTICAL)

        self.table=ttk.Treeview(tbl_frame,columns=("id","time","email","prof","feedback"),xscrollcommand=scr_x.set,yscrollcommand=scr_y.set)
        scr_x.pack(side=BOTTOM,fill="x")
        scr_y.pack(side=RIGHT,fill="y")

        scr_x.configure(command=self.table.xview)
        scr_y.configure(command=self.table.yview)

        #self.table.heading("id",text="ID")
        self.table.column("id", width=80, anchor='center')
        self.table.column("time", width=250, anchor='center')
        self.table.column("email", width=300, anchor='center')
        self.table.column("prof", width=300, anchor='center')
        self.table.column("feedback", width=800)
        
        self.table.heading("id",text="ID")
        self.table.heading("time",text="Time")
        self.table.heading("email",text="Email")
        self.table.heading("prof",text="Profession")
        self.table.heading("feedback",text="Feedback",anchor="w")

        self.table["show"]="headings"

        self.table.pack(fill="both",expand=True)
        self.fetch_data()

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13), foreground="black", background="white")
        style.configure("Treeview.Heading", font=("Arial", 16), foreground="black", background="green")
        style.configure("Treeview", rowheight=30)
        
        

        
        separator = ttk.Separator(self.table, orient='horizontal')
        separator.place(x=0, y=25, relwidth=1, relheight=0)
       
       
        # Google Sheets API Setup
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SERVICE_ACCOUNT_FILE = 'personal-progress-tracker-d6190e11682e.json'  # Replace with your JSON key file path

        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        # Google Sheets details
        SPREADSHEET_ID = '1K_ZFXK_k8daftnUN1WBFQXGdOOiCnYQNfdl9z_EvsOk' 
                          
        RANGE_NAME = 'Form Responses 1!A2:D'  # Adjust based on your sheet's structure

        # Fetch the data from Google Sheets
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        rows = result.get('values', [])

        # MySQL database connection
        db = mysql.connector.connect(
            host="localhost",          
            user="root",      
            password="Satya@9632",  
            database="my_project"  
        )
        cursor = db.cursor()

        # Create feedback table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                email VARCHAR(255),
                profession VARCHAR(255),
                feedback TEXT
            )
        ''')

        # Insert new rows into MySQL database if they don't already exist
        for row in rows:
            if len(row) >= 4:
                # Convert the timestamp to the correct format for MySQL (YYYY-MM-DD HH:MM:SS)
                timestamp_str = row[0]
                try:
                    # Convert the timestamp from 'MM/DD/YYYY HH:MM:SS' to 'YYYY-MM-DD HH:MM:SS'
                    timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print(f"Error parsing timestamp: {timestamp_str}")
                    continue

                email, profession, feedback = row[1], row[2], row[3]

                # Check if the row already exists in the database
                cursor.execute('''
                    SELECT COUNT(*) FROM feedback WHERE timestamp = %s AND email = %s
                ''', (timestamp, email))
                count = cursor.fetchone()[0]

                if count == 0:  # If not found, insert the new row
                    cursor.execute('''
                        INSERT INTO feedback (timestamp, email, profession, feedback)
                        VALUES (%s, %s, %s, %s)
                    ''', (timestamp, email, profession, feedback))
                    db.commit()

    def fetch_data(self):
        db = mysql.connector.connect(
            host="localhost",          
            user="root",      
            password="Satya@9632",  
            database="my_project"  
        )
        cursor = db.cursor()
        cursor.execute("select * from feedback")
        my_data=cursor.fetchall()
        if len(my_data)!=0:
            self.table.delete(*self.table.get_children())
            for i in my_data:
                self.table.insert("",END,values=i)
            db.commit()
            db.close()
        cursor.close()
        db.close()   

    def get_cursor(self, event=""):
        cursor_row = self.table.focus()  # Get the currently focused row
        content = self.table.item(cursor_row)  # Retrieve the item data from the row
        data = content["values"]  # Extract the values list from the item

        # Check if the data contains the expected number of elements to avoid IndexError
        if data and len(data) >= 5:  # Ensure that there are at least 5 items in the row
            self.var_id.set(data[0])
            self.var_ts.set(data[1])
            self.var_email.set(data[2])
            self.var_prof.set(data[3])
            self.var_fdb.set(data[4])
        else:
            # Handle the case where the data is missing or incomplete
            print("Row data is incomplete or not available.")

    

    #----------------------------search data---------------------------------------------------------------------
    def search_data(self):
        if(self.var_com_search.get()=="" or self.var_searchbox.get()==""):
            messagebox.showerror("Error","please select option")
        else:
            try:
                db = mysql.connector.connect(
                host="localhost",          
                user="root",      
                password="Satya@9632",  
                database="my_project"  
                )
                cursor = db.cursor()
                cursor.execute("select * from feedback where "+str(self.var_com_search.get())+" LIKE '%"+str(self.var_searchbox.get())+"%'")
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

    
    def refresh(self):
        '''for item in self.table.delete(*self.table.get_children()):
            self.table.delete(item)'''

        self.fetch_data()

        
    



if __name__ == "__main__":
    root = CTk()
    obj = fdb(root)
    root.mainloop()
