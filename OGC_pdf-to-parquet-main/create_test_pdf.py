from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_simple_pdf():
    filename = "Test_Simple/simple_test.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Page 1
    c.drawString(100, 750, "Test Document - Page 1")
    c.drawString(100, 700, "This is a technical diagram showing system architecture.")
    c.drawString(100, 650, "Key components:")
    c.drawString(120, 620, "- Database layer")
    c.drawString(120, 590, "- API gateway")
    c.drawString(120, 560, "- Frontend interface")
    c.showPage()
    
    # Page 2
    c.drawString(100, 750, "Test Document - Page 2")
    c.drawString(100, 700, "Performance metrics and analysis:")
    c.drawString(100, 650, "Response time: 150ms")
    c.drawString(100, 620, "Throughput: 1000 requests/sec")
    c.drawString(100, 590, "Error rate: 0.1%")
    c.showPage()
    
    c.save()
    print(f"Created simple test PDF: {filename}")

if __name__ == "__main__":
    create_simple_pdf()