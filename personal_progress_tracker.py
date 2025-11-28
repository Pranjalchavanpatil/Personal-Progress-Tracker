from customtkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import warnings
from tkinter import messagebox
import mysql.connector
warnings.filterwarnings("ignore")


class register():
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1525x784+0+0")
        self.root.resizable(False, False)
        set_appearance_mode("dark")
        
        #self.root.attributes("-topmost",True)
        #self.root.focus_force()

     #----------------------------logo---------------------------------------------------------
         
        icon = Image.open("6.ico")
        icon = ImageTk.PhotoImage(icon)

        self.root.wm_iconbitmap("6.ico") 

 #----------------------------BACKGROUNG IMAGE---------------------------------------------------------
        
        self.bg_img = Image.open("images/13.jpg")
        self.bg_img = self.bg_img.resize((1920,1080 ), Image.LANCZOS)
        self.bg_img= ImageTk.PhotoImage(self.bg_img)
        bg_label=tk.Label(self.root, image=self.bg_img)
        bg_label.place(x=-2, y=-2)
        
#----------------------------variables--------------------------------------------------------
        self.var_username=StringVar()
        self.var_password=StringVar()
        self.var_que = StringVar()
        self.var_ans=StringVar()
        self.var_new_pass=StringVar()

     #----------------------------title--------------------------------------------------------

        self.frame = CTkFrame(self.root ,fg_color='slateblue3',border_color="blue",width=475,height=435,border_width=4,corner_radius=30)
        self.frame.place(x=550,y=150)

        hding_lbl=CTkLabel(self.frame,text="Welcome Back..!",font=("goudy old style", 28, "bold"),height=30)
        hding_lbl.place(x=150,y=30)

        hding_lbl=CTkLabel(self.frame,text="Please Login..",font=("goudy old style", 28, "bold"),height=30)
        hding_lbl.place(x=170,y=80)


     #----------------------------user name---------------------------------------------------------

        user_label=CTkLabel(self.frame,text="Username",font=("goudy old style", 18, "bold"),height=5)
        user_label.place(x=110,y=140)

        self.user_entry=CTkEntry(self.frame,border_color="blue",textvariable=self.var_username,font=("goudy old style", 18, "bold"),border_width=2,width=250,height=5)
        self.user_entry.place(x=110,y=165)
    
     #----------------------------password and eye btns---------------------------------------------------------

        passward_label=CTkLabel(self.frame,text="Password",font=("goudy old style", 18, "bold"),height=5)
        passward_label.place(x=110,y=220)
        
        self.password_entry=CTkEntry(self.frame,border_color="blue",textvariable=self.var_password,show="*",font=("goudy old style", 18, "bold"),border_width=2,width=250,height=5)
        self.password_entry.place(x=110,y=245)

        self.close_eye = Image.open("images/closeye1.png")
        self.close_eye = self.close_eye.resize((20,20 ), Image.LANCZOS)

        self.open_eye = Image.open("images/openeye.png")
        self.open_eye = self.open_eye.resize((20,20 ), Image.LANCZOS)

        self.close_eye= ImageTk.PhotoImage(self.close_eye)
        self.open_eye= ImageTk.PhotoImage(self.open_eye)

        self.eye_btn=CTkButton(self.frame,text="",image=self.open_eye,width=18,height=10,cursor="hand2",corner_radius=50,bg_color="transparent" ,fg_color='transparent',hover="transparent")
        self.eye_btn.configure(command=self.toggle_eye_btn)
        self.eye_btn.place(x=329, y=247)


     #----------------------------forget password---------------------------------------------------------

        self.fgt_btn=CTkButton(self.frame,text="forget password ?",command=self.forgot_pass_btn,cursor="hand2",bg_color="transparent",fg_color='transparent',hover="transparent")
        self.fgt_btn.place(x=220,y=275)

        self.login_btn=CTkButton(self.frame,text="LOGIN",cursor="hand2",border_width=1.5,border_color="blue",command=self.open_dash,fg_color="slateblue4")
        self.login_btn.place(x=160,y=320)
    
        root.bind('<Return>', self.enter_key)
        
    def toggle_eye_btn(self):
        if self.eye_btn.cget('image')== (self.open_eye):
            self.eye_btn.configure(image=self.close_eye)
            self.password_entry.configure(show="")
            
        else:
            self.eye_btn.configure(image=self.open_eye)
            self.password_entry.configure(show="*")

    def reset(self):
     self.ans_entry.delete(0,END)
     self.new_pass_entry.delete(0,END)
     self.question.set("select question..")
     self.password_entry.delete(0,END)
     self.user_entry.delete(0,END)

    def forget_password(self):
        if  self.var_ans.get()=="" or self.var_new_pass.get()=="":
            messagebox.showerror("Error:", "All fields are required..", parent=self.root2)
        else:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Satya@9632",
                    database="my_project",
                    use_pure=True
                )
                cursor = db.cursor()

                cursor.execute("SELECT * FROM login WHERE username = %s and question= %s and ans= %s", (self.var_username.get(),self.var_que.get(),self.var_ans.get()))
                data = cursor.fetchone()
                
                
                if data == None:
                    messagebox.showerror("Error:", "Please Select correct Question / Enter correct Answer", parent=self.root2)
                else:
                    cursor.execute("update login set pass= %s WHERE username = %s", (self.var_new_pass.get(),self.var_username.get(),))
                    
                    db.commit()
                    db.close()
                    messagebox.showinfo("success","your password has been reset,Please login with new password",parent=self.root2)
                    self.reset()
                    self.root2.destroy()
                   
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root2)
                
                

    def forgot_pass_btn(self):
        if self.var_username.get() == "":
            messagebox.showerror("Error:", "Please enter the Username to reset your password", parent=self.root)
        else:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Satya@9632",
                    database="my_project",
                    use_pure=True
                )
                cursor = db.cursor()

               
                cursor.execute("SELECT * FROM login WHERE username = %s", (self.var_username.get(),))
                
                
                data = cursor.fetchone()
                
               
                if data == None:
                    messagebox.showerror("Error:", "Invalid Username", parent=self.root)
                else:
                      
                    self.root2 = CTkToplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("400x400+750+250")
                    self.root2.focus_force()
                    self.root2.config(bg="white")
                    self.root2.attributes('-topmost', True)

                    

                    self.root2.wm_iconbitmap("6.ico")

                    self.l1 = CTkLabel(self.root2, text="FORGOT PASSWORD", font=("times new roman", 20, "bold"),
                                    bg_color="white", text_color="red")
                    self.l1.place(x=100, y=30)

                    

                    self.que_l1 = CTkLabel(self.root2, text="Your question:", font=("times new roman", 18, "bold"),
                                        bg_color="white", text_color="black")
                    self.que_l1.place(x=50, y=80)

                    all_que = [ "What is your favorite fruit ?","What is your pet name ?", "What is your favorite food ?"]
                    self.question = CTkComboBox(self.root2, variable=self.var_que, values=all_que, height=30, width=300,
                                                text_color="black", state="readonly", font=("helvetica", 15),
                                                fg_color="azure")
                    self.question.place(x=50, y=110)
                    self.question.set("select question..")

                    self.ans_l1 = CTkLabel(self.root2, text="Enter Answer:", font=("times new roman", 18, "bold"),
                                        bg_color="white", text_color="black")
                    self.ans_l1.place(x=50, y=170)

                    self.ans_entry = CTkEntry(self.root2, width=300,textvariable=self.var_ans, font=("times new roman", 18,), bg_color="white",
                                            fg_color="white", text_color="black")
                    self.ans_entry.place(x=50, y=200)

                    self.pass_l1 = CTkLabel(self.root2, text="New Password:",font=("times new roman", 18, "bold"),
                                            bg_color="white", text_color="black")
                    self.pass_l1.place(x=50, y=240)

                    
                    self.new_pass_entry = CTkEntry(self.root2, width=300,textvariable=self.var_new_pass ,font=("times new roman", 18,), bg_color="white",
                                                fg_color="white", text_color="black")
                    self.new_pass_entry.place(x=50, y=270)

                    self.change_btn = CTkButton(self.root2, text="Change Password",command=self.forget_password, cursor="hand2",
                                                font=("goudy old style", 18, "bold"))
                    self.change_btn.place(x=130, y=340)
                

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)



    def enter_key(self,event):
        self.open_dash()


    def open_dash(self):
        if self.var_username.get() == "" or self.var_password.get() == "":
            messagebox.showerror("Error:", "Please enter the Username and password", parent=self.root)
        else:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Satya@9632",
                    database="my_project",
                    use_pure=True
                )
                cursor = db.cursor()

                cursor.execute("SELECT * FROM login WHERE username = %s and pass= %s", 
                            (self.var_username.get(), self.var_password.get(),))
                data = cursor.fetchone()

                if data is None:
                    messagebox.showerror("Error:", "Invalid Username or password", parent=self.root)
                else:
                    
                    self.root.withdraw()

                    
                    new_root = CTkToplevel() 
                    new_root.title("Dashboard")
                    
                    # Load the dashboard
                    import AB_dashboard  
                    AB_dashboard.PPT(new_root) 
                    new_root.mainloop()  

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)



        

   
        

if __name__ == "__main__":
    root = CTk()
    
    obj = register(root)
    root.mainloop()
