from flask import Flask, request, send_file, jsonify, render_template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

def create_invoice_pdf(filename, date, party_name, pan, destination, quantity, rate, bank_details):
    logo_path = "header.png"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Add logo image at the top
    logo_width = 500  # Adjust the width as needed
    logo_height = 110  # Adjust the height as needed
    c.drawImage(logo_path, (width - logo_width - 50) / 2, height - logo_height - 20, width=logo_width, height=logo_height)

    # # Header
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(200, height - logo_height - 60, "JK COMMERCIAL")

    # c.setFont("Helvetica", 10)
    # c.drawString(30, height - logo_height - 80, "42 KALI KRISHNA TAGORE STREET, 1ST FLOOR, KOLKATA-700007")
    # c.drawString(30, height - logo_height - 95, "PHONE: 94333-74617, (033) 2259-1689, 2259-0637")

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(450, height - logo_height - 50, f"Date: {date}")

    # Party Details
    c.setFont("Helvetica", 10)
    c.drawString(30, height - logo_height - 80, f"Party Name: {party_name}")
    c.drawString(30, height - logo_height - 100, f"PAN: {pan}")
    c.drawString(30, height - logo_height - 120, f"GSTIN: 1234")

    c.drawString(30, height - logo_height - 140, "To")
    c.drawString(30, height - logo_height - 160, "Premium Chicks Feeds Pvt Ltd")
    # Destination and Quantity
    c.drawString(30, height - logo_height - 200, f"Destination: {destination}")
    c.drawString(30, height - logo_height - 220, f"Quantity: {quantity} Mton Maize @ {rate}/-")

    # Bank Details

    c.drawString(30, height - logo_height - 280, f"Bank Details: {bank_details['bank_name']}")
    c.drawString(30, height - logo_height - 300, f"A/c No: {bank_details['account_number']}")
    c.drawString(30, height - logo_height - 320, f"Branch: {bank_details['branch']}")
    c.drawString(30, height - logo_height - 340, f"IFSC: {bank_details['ifsc']}")

    # Signature
    c.drawString(30, height - logo_height - 580, "SIGNATURE")

    # Save the PDF
    c.showPage()
    c.save()

# def main():
#     # Get input from the user
#     # date = input("Enter the date (DD/MM/YY): ")
#     # party_name = input("Enter the party name: ")
#     # pan = input("Enter the PAN: ")
#     # destination = input("Enter the destination: ")
#     # quantity = input("Enter the quantity: ")
#     # rate = input("Enter the rate: ")

#     # bank_name = input("Enter the bank name: ")
#     # account_number = input("Enter the account number: ")
#     # branch = input("Enter the branch: ")
#     # ifsc = input("Enter the IFSC code: ")
    
    
#     bank_name = "HDFC BANK LIMITED"
#     account_number = "123445"
#     branch = "Chinar Park"
#     ifsc = "12344"

#     bank_details = {
#         "bank_name": bank_name,
#         "account_number": account_number,
#         "branch": branch,
#         "ifsc": ifsc
#     }

#     # Create the PDF
#     # create_invoice_pdf(
#     #     "JKCOMMERCIAL_Invoice.pdf",
#     #     date,
#     #     party_name,
#     #     pan,
#     #     destination,
#     #     quantity,
#     #     rate,
#     #     bank_details
#     # )
    
#     create_invoice_pdf(
#     "JKCOMMERCIAL_Invoice.pdf",
#     "18/10/23",
#     "M/s J.K.COMMERCIAL",
#     "AAFHB5228L",
#     "JUNGALPUR (UNICATTLE)",
#     60,
#     2250, 
#     bank_details
# )

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    filename = "JKCOMMERCIAL_Invoice.pdf"
    bank_details = {
        "bank_name": data['bank_name'],
        "account_number": data['account_number'],
        "branch": data['branch'],
        "ifsc": data['ifsc']
    }
    create_invoice_pdf(
        filename,
        data['date'],
        data['party_name'],
        data['pan'],
        data['destination'],
        data['quantity'],
        data['rate'],
        bank_details
    )
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)