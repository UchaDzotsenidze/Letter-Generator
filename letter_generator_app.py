
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from datetime import datetime
import os



# from reportlab.lib.pagesizes import LETTER
# from reportlab.pdfgen import canvas
# import os
import textwrap

def generate_pdf(name, date, vin, address, address2, model, plate, impoundDate, registeredOwnersName, noticeType):
    filename = f"{name.replace(' ', '_')}_letter.pdf"
    filepath = os.path.join("generated_pdfs", filename)

    os.makedirs("generated_pdfs", exist_ok=True)
    c = canvas.Canvas(filepath, pagesize=LETTER)
    width, height = LETTER

    # === Margins ===
    margin_left = 40
    margin_right = 60
    usable_width = width - margin_left - margin_right

    # === HEADER (Centered) ===
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 60, "BEN AND NINO AUTO REPAIR INC")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, "2603 STILLWELL AVE")
    c.drawCentredString(width / 2, height - 95, "BROOKLYN, NY 11223")
    c.drawCentredString(width / 2, height - 110, "(718) 339-8500 EXT 203")

    # === Date & Notice ===
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_left, height - 140, f"Date: {date}")
    c.drawRightString(width - margin_right, height - 140, f"{noticeType}")

    # === Start text object
    text_object = c.beginText()
    text_object.setTextOrigin(margin_left, height - 170)
    text_object.setFont("Helvetica", 12)

    # === Recipient Address ===
    text_object.textLine(name)
    text_object.textLine(address)
    text_object.textLine(address2)
    text_object.moveCursor(0, 20)

    # === Letter Body with Word Wrap ===
    body = f"""\
Dear Vehicle Owner / Registered Owner,

    This communication is to inform you that your vehicle has been impounded or recovered by Ben and Nino Auto Repair Inc., and in certain cases, by law enforcement. Please be advised that daily storage fees are accruing until the vehicle is released.

    To facilitate the redemption process, we strongly recommend contacting us prior to visiting our facility. This will allow us to update your bill and position the vehicle in an accessible area for prompt removal.

    Redemption hours are Monday through Friday, between 9:00 AM and 4:00 PM. Immediate attention is essential to avoid further actions, including the initiation of the lien process. Failure to contact us within five (5) days of receiving this notice may result in complications.

    To discuss the release process or address any inquiries, please contact us as soon as possible. Your vehicle will only be released upon full payment of all towing and storage fees.

    Ben and Nino Auto Repair Inc. will claim a lien pursuant to Section 184 of the New York State Lien Law on a {model}, with DMV license plate number {plate},
    and VIN {vin}, impounded on {impoundDate}, registered to {registeredOwnersName}.

    We appreciate your cooperation and look forward to your prompt response.

Sincerely,

Ben and Nino Auto Repair Inc."""

    # Wrap each paragraph manually
    for paragraph in body.split('\n\n'):
        lines = textwrap.wrap(paragraph, width=95)  # Adjust width for font size and margin
        for line in lines:
            text_object.textLine(line)
        text_object.textLine("")  # Blank line between paragraphs

    # === Draw to canvas and save
    c.drawText(text_object)
    c.save()
    return filepath


# Streamlit UI
st.title("PDF Letter Generator")

types = ["NOTICE", "FIRST NOTICE", "SECOND NOTICE", "FINAL NOTICE"]

date = st.date_input("Enter Date", value=datetime.today())
noticeType = st.selectbox("Select notice Type", types)
name = st.text_input("Enter recipient name / Company name").upper()
address = st.text_input("Enter Address").upper()
address2 = st.text_input("Enter City, State, Zip").upper()
vin = st.text_input("Enter VIN").upper()
model = st.text_input("Enter YEAR/MAKE/MODEL").upper()
plate = st.text_input("Enter plate number - if not available type N/A").upper()
impoundDate = st.date_input("Enter the date vehicle was impounded")
registeredOwnersName = st.text_input("Enter registered owner's name").upper()



if st.button("Generate PDF"):
    if name and vin:
        pdf_path = generate_pdf(name, date.strftime('%Y-%m-%d'), vin, address, address2, model, plate, impoundDate, registeredOwnersName, noticeType)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        st.success("PDF generated successfully!")
    else:
        st.warning("Please fill in all the fields.")
