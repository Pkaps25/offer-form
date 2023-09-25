from tkinter import * 
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import locale

base = Tk()  
locale.setlocale( locale.LC_ALL, '' )
base.geometry("1000x1000")  
base.title("registration form")  

business_name_var = StringVar()
owner_name_var = StringVar()


general_choices = {
    "Business name": business_name_var, 
    "Owner name": owner_name_var, 
    }
y_vals = iter(range(10,2000,30))
for label, var in general_choices.items():
    y_val = next(y_vals)
    label = Label(base, text=label, width=25, font=("arial", 12))  
    label.place(x=19, y=y_val)  
    entry = Entry(base, textvariable=var)  
    entry.place(x=200,y=y_val)

offer_items = ["Frequency", "Term", "Amount", "Payback", "Payments", "Payments before refinance", "Payment"]
offers = {}
for i in range(1,4):
    offers[i] = {
        k: StringVar() for k in offer_items
    }
    for labelstr, var in offers[i].items():
        y_val = next(y_vals)
        label = Label(base, text=f"{labelstr} {i}", width=25, font=("arial", 12))
        label.place(x=19, y=y_val)
        if labelstr == "Frequency":
            entry = OptionMenu(base, var, "Bi-Weekly", "Weekly", "Monthly")
            var.set("Select")
            entry.pack()
        else:
            entry = Entry(base, textvariable=var)
        entry.place(x=200,y=y_val)


def format_currency(num):
    cur = locale.currency(num, grouping=True)
    return cur[:-3]


def submit():
    business_name = business_name_var.get()
    owner_name = owner_name_var.get()

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('LucidaSansUnicode', 'l_10646.ttf'))
    can.setFont("LucidaSansUnicode", 10)


    # Write business/owner name
    can.setFillColorRGB(255,255,255)
    can.drawString(20, 691, business_name)
    can.drawString(500, 691, owner_name)

    # Write date
    can.setFillColorRGB(0,0,0)
    can.drawString(520, 720, date.today().strftime("%m/%d/%Y"))

    # Write offer options
    offer2_filled = offers[2]["Term"].get() != ""
    offer3_filled = offers[3]["Term"].get() != ""
    template_pdf = "offer1.pdf"
    if offer2_filled:
        template_pdf = "offer2.pdf"
    if offer3_filled:
        template_pdf = "offer3.pdf"

    # only 1 offer
    if not offer2_filled and not offer3_filled:
        can.drawString(62, 484, offers[1]["Frequency"].get())
        can.drawString(128, 484, offers[1]["Term"].get()) 
        can.drawString(260, 484, format_currency(int(offers[1]["Payback"].get())))
        can.drawString(345, 484, offers[1]["Payments"].get())
        can.drawString(460, 484, format_currency(int(offers[1]["Payment"].get())))
        can.drawString(360, 470, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 484, format_currency(int(offers[1]["Amount"].get())))
        can.drawString(345, 470, offers[1]["Payments before refinance"].get())

    # 2 offers
    elif offer2_filled and not offer3_filled:
        # first offer
        can.setFillColorRGB(0,0,0)
        can.drawString(62, 490, offers[1]["Frequency"].get())
        can.drawString(128, 490, offers[1]["Term"].get()) 
        can.drawString(260, 490, format_currency(int(offers[1]["Payback"].get())))
        can.drawString(345, 490, offers[1]["Payments"].get())
        can.drawString(460, 490, format_currency(int(offers[1]["Payment"].get())))
        can.drawString(360, 476, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 490, format_currency(int(offers[1]["Amount"].get())))
        can.drawString(345, 476, offers[1]["Payments before refinance"].get())

        # second offer
        can.setFillColorRGB(0,0,0)
        can.drawString(62, 440, offers[2]["Frequency"].get())
        can.drawString(128, 440, offers[2]["Term"].get()) 
        can.drawString(260, 440, format_currency(int(offers[2]["Payback"].get())))
        can.drawString(345, 440, offers[2]["Payments"].get())
        can.drawString(460, 440, format_currency(int(offers[2]["Payment"].get())))
        can.drawString(360, 426, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 440, format_currency(int(offers[2]["Amount"].get())))
        can.drawString(345, 426, offers[2]["Payments before refinance"].get())

    # 3 offers
    elif offer2_filled and offer3_filled:
        # first offer
        can.setFillColorRGB(0,0,0)
        can.drawString(62, 495, offers[1]["Frequency"].get())
        can.drawString(128, 495, offers[1]["Term"].get()) 
        can.drawString(260, 495, format_currency(int(offers[1]["Payback"].get())))
        can.drawString(345, 495, offers[1]["Payments"].get())
        can.drawString(460, 495, format_currency(int(offers[1]["Payment"].get())))
        can.drawString(360, 481, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 495, format_currency(int(offers[1]["Amount"].get())))
        can.drawString(345, 481, offers[1]["Payments before refinance"].get())

        # second offer
        can.setFillColorRGB(0,0,0)
        can.drawString(62, 452, offers[2]["Frequency"].get())
        can.drawString(128, 452, offers[2]["Term"].get()) 
        can.drawString(260, 452, format_currency(int(offers[2]["Payback"].get())))
        can.drawString(345, 452, offers[2]["Payments"].get())
        can.drawString(460, 452, format_currency(int(offers[2]["Payment"].get())))
        can.drawString(360, 438, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 452, format_currency(int(offers[2]["Amount"].get())))
        can.drawString(345, 438, offers[2]["Payments before refinance"].get())

        # third offer
        can.setFillColorRGB(0,0,0)
        can.drawString(62, 412, offers[2]["Frequency"].get())
        can.drawString(128, 412, offers[2]["Term"].get()) 
        can.drawString(260, 412, format_currency(int(offers[2]["Payback"].get())))
        can.drawString(345, 412, offers[2]["Payments"].get())
        can.drawString(460, 412, format_currency(int(offers[2]["Payment"].get())))
        can.drawString(360, 398, "before refinance")

        can.setFillColorRGB(51/256, 153/256, 255/256)
        can.drawString(194, 412, format_currency(int(offers[2]["Amount"].get())))
        can.drawString(345, 398, offers[2]["Payments before refinance"].get())

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open(template_pdf, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    outputStream = open(f"Approval - {business_name}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    # close the form
    base.destroy()

  
Button(base, text="Register", width=10, command=submit).place(x=20,y=900)  
base.mainloop()