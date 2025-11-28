from customtkinter import *
import mysql.connector
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Scrollbar, Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class grp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Progress Tracker")
        self.root.geometry("1400x550+80+280")

        title = CTkLabel(self.root, text="GRAPHS", font=("goudy old style", 25, "bold", "underline"), height=50,
                         bg_color="white", fg_color="dodgerblue")
        title.place(x=0, y=0, relwidth=1)

        # Ensure that background comes before the graphs
        self.bg_img = Image.open("images/bg2.jpg")
        self.bg_img = self.bg_img.resize((1920, 1060), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        bg_label = CTkLabel(self.root, image=self.bg_img)
        bg_label.place(x=0, y=50)

        # ------------------------------Scrollable frame for graphs------------------------------
        frame_width = 1200  # Increase width to fit more graphs horizontally
        frame_height = 490
        frame = CTkFrame(self.root, bg_color="azure", height=frame_height, width=frame_width)

        # Centering the frame in the middle
        frame.place(relx=0.5, rely=0.5, anchor="center", y=25)  # Adjust 'y' for title offset

        frame.pack_propagate(False)

        # Create a canvas inside the frame
        self.canvas = Canvas(frame, bg="azure")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Add a horizontal scrollbar to the canvas
        self.scrollbar = Scrollbar(frame, orient="horizontal", command=self.canvas.xview)  # Changed to horizontal
        self.scrollbar.pack(side="bottom", fill="x")

        # Configure canvas with the horizontal scrollbar
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create another frame inside the canvas to hold the graphs (this is where graphs are placed)
        self.cert_frame = CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cert_frame, anchor="nw")  # 'anchor' remains "nw" (northwest)

        # Bind canvas to resize event and ensure proper scroll region
        self.canvas.bind("<Configure>", self.update_scroll_region)

        # Create the graphs after the background is set
        self.create_graph1()
        self.create_graph2()
        self.create_graph3()

    # ------------------------------Graph 1: Achievements------------------------------
    def fetch_data1(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Satya@9632",
            database="my_project")

        cursor = db.cursor()
        cursor.execute("SELECT * FROM archiev")
        data = cursor.fetchall()
        db.close()
        return data

    def create_graph1(self):
        data = self.fetch_data1()
        sem_data = [i[1] for i in data]
        counts = [sem_data.count(i) for i in set(sem_data)]
        labels = list(set(sem_data))

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(counts, labels=labels, autopct='%1.1f%%')
        ax.set_title('Achievements during each semester')

        # Place the graph inside a frame in cert_frame
        self.graph_frame1 = CTkFrame(self.cert_frame)
        self.graph_frame1.pack(side="left", padx=10, pady=10)  # Place side by side for horizontal scroll

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ------------------------------Graph 2: SGPA Analysis------------------------------
    def fetch_data2(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Satya@9632",
            database="my_project"
        )
        cursor = db.cursor()
        cursor.execute("SELECT Sem, sgpa FROM sgpa")
        data = cursor.fetchall()
        db.close()
        return data

    def create_graph2(self):
        data = self.fetch_data2()
        data.sort(key=lambda x: x[0])  # Sort data by semester
        semesters = [row[0] for row in data]
        sgpas = [float(row[1]) for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(semesters, sgpas, marker='o')
        ax.set_title('SGPA Analysis For Each Sem')
        ax.set_xlabel('Semester')
        ax.set_ylabel('SGPA')
        ax.set_xticks(semesters)

        # Place the graph inside a frame in cert_frame
        self.graph_frame2 = CTkFrame(self.cert_frame)
        self.graph_frame2.pack(side="left", padx=10, pady=10)  # Place side by side for horizontal scroll

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ------------------------------Graph 3: Skill Progress------------------------------
    def fetch_data3(self):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Satya@9632",
            database="my_project")

        cursor = db.cursor()
        cursor.execute("SELECT Progress FROM skills")
        data = cursor.fetchall()
        db.close()
        return data

    def create_graph3(self):
        data = self.fetch_data3()
        incomplete, inprogress, complete = 0, 0, 0
        for row in data:
            if row[0] == "Incomplete":
                incomplete += 1
            elif row[0] == "In Progress":
                inprogress += 1
            elif row[0] == "Completed":
                complete += 1

        labels = ['Incomplete', 'In Progress', 'Completed']
        sizes = [incomplete, inprogress, complete]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Skill Progress Status')

        # Place the graph inside a frame in cert_frame
        self.graph_frame3 = CTkFrame(self.cert_frame)
        self.graph_frame3.pack(side="left", padx=10, pady=10)  # Place side by side for horizontal scroll

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame3)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Update the scroll region when the content changes
    def update_scroll_region(self, event=None):
        self.cert_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = CTk()
    obj = grp(root)
    
    root.mainloop()
