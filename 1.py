from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def share_btn(self, file_path):
    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    # Styles for the text
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    # Add a clickable link (HTML-style hyperlink)
    link_text = '<link href="https://forms.gle/mNkKDV1NrMFa63kBA">Click here to provide feedback</link>'
    paragraph = Paragraph(link_text, normal_style)

    # Build the PDF
    doc.build([paragraph])

    print("PDF saved successfully!")
