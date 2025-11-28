from fpdf import FPDF
import mysql.connector

def save_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add a title
    pdf.cell(200, 10, txt="Student Progress Report", ln=True, align='C')
    
    # Fetch data from database
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT name, semester, marks FROM students")
        
        data = cursor.fetchall()
        
        # Add data to the PDF
        for row in data:
            pdf.cell(0, 10, f"Name: {row[0]}, Semester: {row[1]}, Marks: {row[2]}", ln=True)
        
        # Save the PDF to a file
        pdf.output("student_report.pdf")
        print("PDF saved successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

