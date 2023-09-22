from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
pdfmetrics.registerFont(TTFont('LucidaSansUnicode', 'l_10646.ttf'))
can.setFont("LucidaSansUnicode", 11)


# Write business/owner name
can.setFillColorRGB(255,255,255)
can.drawString(20, 691, "Hello world")
can.drawString(500, 691, "Hello world")

# Write date
can.setFillColorRGB(0,0,0)
can.drawString(520, 720, date.today().strftime("%m/%d/%Y"))

# Write offer option

can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open("offer1.pdf", "rb"))
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()
