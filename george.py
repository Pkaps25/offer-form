import enum
import io
import locale
from collections import OrderedDict
from datetime import date
from tkinter import Button, Entry, Label, OptionMenu, StringVar, Tk

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FORM_FONT_SIZE = 13
BLUE_COLOR_RGB = (51 / 256, 153 / 256, 255 / 256)


base = Tk()
locale.setlocale(locale.LC_ALL, "")
base.geometry("1000x1000")
base.title("registration form")

additional_notes_var = StringVar()


class OfferItem(enum.Enum):
    FREQUENCY = "Frequency of Payment"
    TERM = "Term in Months"
    AMOUNT = "Funding Amount"
    PAYBACK = "Payback Amount"
    PAYMENTS = "Number of Payments"
    PAYMENT = "Payment Amount"


class RequiredItem(enum.Enum):
    BUSINESS_NAME = "Business name"
    OWNER_NAME = "Owner name"


label_map = {}
required_vars = {}
y_vals = iter(range(10, 2000, 33))
for required_item in RequiredItem:
    required_vars[required_item] = StringVar()
    y_val = next(y_vals)
    label = Label(base, text=required_item.value, width=25, font=("arial", FORM_FONT_SIZE))
    label.place(x=19, y=y_val)
    entry = Entry(base, textvariable=required_vars[required_item])
    entry.place(x=200, y=y_val)
    label_map[required_item] = label


offers = OrderedDict()
for i in range(1, 4):
    offers[i] = {k.value: StringVar() for k in OfferItem}
    for labelstr, var in offers[i].items():
        y_val = next(y_vals)
        label_text = f"{labelstr} {i}"
        label = Label(base, text=f"{labelstr} {i}", width=25, font=("arial", FORM_FONT_SIZE))
        label_map[label_text] = label
        label.place(x=19, y=y_val)
        if labelstr == OfferItem.FREQUENCY.value:
            entry = OptionMenu(base, var, "Daily", "Bi-Weekly", "Weekly", "Monthly")
            var.set("Select")
            entry.pack()
        else:
            entry = Entry(base, textvariable=var)
        entry.place(x=200, y=y_val)

# add additional info entry
y_val = next(y_vals)
Label(base, text="Additional notes", width=25, font=("arial", FORM_FONT_SIZE)).place(x=19, y=y_val)
Entry(base, textvariable=additional_notes_var).place(x=200, y=y_val)


def format_currency(num):
    cur = locale.currency(num, grouping=True)
    return cur[:-3]


def validate_form():
    for label in label_map.values():
        label.config(foreground="black")
    valid = True

    for required_item in RequiredItem:
        if not required_vars[required_item].get():
            label_map[required_item].config(foreground="red")
            valid = False

    for i, offer_map in offers.items():
        # ensure for each offer, either no fields are filled or all fields are filled
        filled = []
        not_filled = []
        for offer_item in OfferItem:
            selected = (
                offer_item == OfferItem.FREQUENCY
                and offer_map[OfferItem.FREQUENCY.value].get() != "Select"
            ) or (offer_item != OfferItem.FREQUENCY and offer_map[offer_item.value].get() != "")
            blank = (
                offer_item == OfferItem.FREQUENCY
                and offer_map[OfferItem.FREQUENCY.value].get() == "Select"
            ) or (offer_item != OfferItem.FREQUENCY and offer_map[offer_item.value].get() == "")

            filled.append(selected)
            not_filled.append(blank)

        valid = all(filled) if i == 1 else (all(filled) or all(not_filled))
        if not valid:
            for offer_item, value in offer_map.items():
                if (offer_item == OfferItem.FREQUENCY.value and value.get() == "Select") or (
                    offer_item != OfferItem.FREQUENCY.value and value.get() == ""
                ):
                    label_map[f"{offer_item} {i}"].config(foreground="red")
            return valid

    return valid


def submit():
    if not validate_form():
        return

    business_name = required_vars[RequiredItem.BUSINESS_NAME].get()
    owner_name = required_vars[RequiredItem.OWNER_NAME].get()

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont("LucidaSansUnicode", "static/l_10646.ttf"))
    can.setFont("LucidaSansUnicode", 10)

    # Write business/owner name
    can.setFillColorRGB(255, 255, 255)
    can.drawString(20, 691, business_name)
    can.drawString(500, 691, owner_name)

    # Write date
    can.setFillColorRGB(0, 0, 0)
    can.drawString(520, 720, date.today().strftime("%m/%d/%Y"))

    # Write offer options
    offer2_filled = offers[2][OfferItem.TERM.value].get() != ""
    offer3_filled = offers[3][OfferItem.TERM.value].get() != ""
    template_pdf = "static/offer1.pdf"
    if offer2_filled:
        template_pdf = "static/offer2.pdf"
    if offer3_filled:
        template_pdf = "static/offer3.pdf"

    # only 1 offer
    if not offer2_filled and not offer3_filled:
        can.drawString(62, 484, offers[1][OfferItem.FREQUENCY.value].get())

        num_payments = offers[1][OfferItem.PAYMENTS.value].get()
        term = offers[1][OfferItem.TERM.value].get()
        can.drawString(128, 484, term)
        can.drawString(138 if int(term) < 10 else 143, 484, "Month(s)")
        can.drawString(260, 484, format_currency(int(offers[1][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 484, num_payments)
        can.drawString(460, 484, format_currency(int(offers[1][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 470, "before refinance")
        can.drawString(25, 380, "Additional notes:")
        can.drawString(112, 380, additional_notes_var.get())

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 484, format_currency(int(offers[1][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 470, str(int(num_payments) // 2))

    # 2 offers
    elif offer2_filled and not offer3_filled:
        # first offer
        can.setFillColorRGB(0, 0, 0)
        can.drawString(25, 380, "Additional notes:")
        can.drawString(112, 380, additional_notes_var.get())

        can.drawString(62, 490, offers[1][OfferItem.FREQUENCY.value].get())

        num_payments = offers[1][OfferItem.PAYMENTS.value].get()
        term = offers[1][OfferItem.TERM.value].get()
        can.drawString(128, 490, term)
        can.drawString(138 if int(term) < 10 else 143, 490, "Month(s)")
        can.drawString(260, 490, format_currency(int(offers[1][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 490, num_payments)
        can.drawString(460, 490, format_currency(int(offers[1][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 476, "before refinance")

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 490, format_currency(int(offers[1][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 476, str(int(num_payments) // 2))

        # second offer
        can.setFillColorRGB(0, 0, 0)
        can.drawString(62, 440, offers[2][OfferItem.FREQUENCY.value].get())

        num_payments = offers[2][OfferItem.PAYMENTS.value].get()
        term = offers[2][OfferItem.TERM.value].get()
        can.drawString(128, 440, term)
        can.drawString(138 if int(term) < 10 else 143, 440, "Month(s)")
        can.drawString(260, 440, format_currency(int(offers[2][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 440, num_payments)
        can.drawString(460, 440, format_currency(int(offers[2][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 426, "before refinance")

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 440, format_currency(int(offers[2][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 426, str(int(num_payments) // 2))

    # 3 offers
    elif offer2_filled and offer3_filled:
        # first offer
        can.setFillColorRGB(0, 0, 0)
        can.drawString(62, 495, offers[1][OfferItem.FREQUENCY.value].get())

        num_payments = offers[1][OfferItem.PAYMENTS.value].get()
        term = offers[1][OfferItem.TERM.value].get()
        can.drawString(128, 495, term)
        can.drawString(138 if int(term) < 10 else 143, 495, "Month(s)")
        can.drawString(260, 495, format_currency(int(offers[1][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 495, num_payments)
        can.drawString(460, 495, format_currency(int(offers[1][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 481, "before refinance")

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 495, format_currency(int(offers[1][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 481, str(int(num_payments) // 2))

        # second offer
        can.setFillColorRGB(0, 0, 0)
        can.drawString(62, 452, offers[2][OfferItem.FREQUENCY.value].get())

        num_payments = offers[2][OfferItem.PAYMENTS.value].get()
        term = offers[2][OfferItem.TERM.value].get()
        can.drawString(128, 452, term)
        can.drawString(138 if int(term) < 10 else 143, 452, "Month(s)")
        can.drawString(260, 452, format_currency(int(offers[2][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 452, num_payments)
        can.drawString(460, 452, format_currency(int(offers[2][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 438, "before refinance")

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 452, format_currency(int(offers[2][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 438, str(int(num_payments) // 2))

        # third offer
        can.setFillColorRGB(0, 0, 0)
        can.drawString(62, 412, offers[3][OfferItem.FREQUENCY.value].get())

        num_payments = offers[3][OfferItem.PAYMENTS.value].get()
        term = offers[3][OfferItem.TERM.value].get()
        can.drawString(128, 412, term)
        can.drawString(138 if int(term) < 10 else 143, 412, "Month(s)")
        can.drawString(260, 412, format_currency(int(offers[3][OfferItem.PAYBACK.value].get())))
        can.drawString(345, 412, num_payments)
        can.drawString(460, 412, format_currency(int(offers[3][OfferItem.PAYMENT.value].get())))
        can.drawString(360, 398, "before refinance")

        can.setFillColorRGB(*BLUE_COLOR_RGB)
        can.drawString(194, 412, format_currency(int(offers[3][OfferItem.AMOUNT.value].get())))
        can.drawString(345, 398, str(int(num_payments) // 2))

    can.save()

    # move to the beginning of the StringIO buffer
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


Button(base, text="Register", width=10, command=submit).place(x=20, y=900)
base.mainloop()
