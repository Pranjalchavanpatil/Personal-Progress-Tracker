from customtkinter import * 
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, Canvas, Scrollbar
import os
import mysql.connector

class certify:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x550+80+280")
        
        # Title
        title = CTkLabel(self.root, text="CERTIFICATES", font=("goudy old style", 25, "bold", "underline"), height=50, bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)

        # Frame for the canvas (to allow scrolling)
        frame = CTkFrame(self.root, bg_color="azure", height=400, width=1300)
        frame.place(x=40, y=60)
        frame.pack_propagate(False)

        # Upload button
        upload_button = CTkButton(self.root, text="Upload Certificates", command=self.upload_certificate)
        upload_button.place(x=630, y=500)

        # Create a canvas inside the frame
        self.canvas = Canvas(frame, bg="azure")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar to the canvas
        self.scrollbar = Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure canvas with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create another frame inside the canvas to hold the certificates
        self.cert_frame = CTkFrame(self.canvas)  
        self.canvas.create_window((0, 0), window=self.cert_frame, anchor="nw")

        # Bind canvas to resize event and ensure proper scroll region
        self.canvas.bind("<Configure>", self.update_scroll_region)

        # To store uploaded image objects (to avoid garbage collection)
        self.uploaded_images = []

        
        self.load_certificates_from_db()

    # Save certificate to the database
    def save_certificate_to_db(self, file_name, file_path):
        db = mysql.connector.connect(
            host="localhost",          
            user="root",      
            password="Satya@9632",  
            database="my_project"   
        )
        cursor = db.cursor()
        cursor.execute("INSERT INTO certificates (file_name, file_path) VALUES (%s, %s)", (file_name, file_path))
        db.commit()
        cursor.close()
        db.close()

    # Function to upload and save certificates to the database
    def upload_certificate(self):
        filetypes = [("Image files", "*.jpg;*.jpeg;*.png")]
        files = filedialog.askopenfilenames(title="Select Certificates", filetypes=filetypes,parent=self.root)
        
        
        if files:
            for file in files:
                file_name = os.path.basename(file)
                file_path = file

                # Save certificate to database
                self.save_certificate_to_db(file_name, file_path)

                # Display the thumbnail
                self.display_certificate_thumbnail(file_path)

            messagebox.showinfo("Success", f"{len(files)} certificate(s) uploaded and saved successfully!",parent=self.root)
        else:
            messagebox.showwarning("No file selected", "Please select at least one certificate to upload.",parent=self.root)

    # Function to display certificate thumbnails
    def display_certificate_thumbnail(self, file_path):
        img = Image.open(file_path)
        img.thumbnail((375, 310))  
        img_tk = ImageTk.PhotoImage(img)
        self.uploaded_images.append(img_tk)  

       
        row, col = divmod(len(self.uploaded_images) - 1, 4)  

        # Create a label to display the thumbnail at the right grid position
        img_label = CTkLabel(self.cert_frame, image=img_tk)
        img_label.grid(row=row, column=col, padx=10, pady=10)  # Spacing between thumbnails

        
        self.update_scroll_region()

    
    def update_scroll_region(self, event=None):
        self.cert_frame.update_idletasks() 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Load certificates from the database
    def load_certificates_from_db(self):
        db = mysql.connector.connect(
            host="localhost",          
            user="root",      
            password="Satya@9632",  
            database="my_project"   
        )
        cursor = db.cursor()
        cursor.execute("SELECT file_path FROM certificates")
        certificates = cursor.fetchall()
        cursor.close()
        db.close()

        for cert in certificates:
            file_path = cert[0]
            self.display_certificate_thumbnail(file_path)

    def hide(self):
        """Method to hide the Toplevel window."""
        self.root.withdraw()

    def show(self):
        """Method to show the Toplevel window."""
        self.root.deiconify() 
        
            
if __name__ == "__main__":
    root = CTk()
    obj = certify(root)
    root.mainloop()
