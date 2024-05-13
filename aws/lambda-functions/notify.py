from fpdf import FPDF
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
import json
from fpdf import FPDF
from io import BytesIO

def generate_pdf_from_data(data):
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add a title
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Health Data Report", ln=True, align="C")

    # Add content from data
    for category, values in data.items():
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt=category.capitalize(), ln=True, align="L")
        pdf.set_font("Arial", size=10)
        if values:
            # Get column names
            column_names = list(values[0].keys())
            # Add column names to table
            pdf.set_font("Arial", size=10, style='B')
            col_width = 200 / len(column_names)
            for col_name in column_names:
                pdf.cell(col_width, 10, col_name, border=1, ln=False, align="C")
            pdf.ln()
            # Add rows to table
            pdf.set_font("Arial", size=10)
            for row in values:
                for col_name in column_names:
                    pdf.cell(col_width, 10, str(row[col_name]), border=1, ln=False, align="C")
                pdf.ln()

    # Output PDF content as byte string
    pdf_bytes = pdf.output(dest='S')

    return pdf_bytes



  

def send_email_with_attachment(sender_email, recipient_email, subject, body_text, attachment_file_name, attachment_data):
    # Create a new SES client
    ses_client = boto3.client('ses')

    # Create a multipart/mixed parent container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Create a multipart/alternative child container
    msg_body = MIMEMultipart('alternative')

    # Add the body text
    text_part = MIMEText(body_text, 'plain')
    msg_body.attach(text_part)
    
    attachment_part = MIMEApplication(attachment_data, _subtype='pdf')
    attachment_part.add_header('Content-Disposition', 'attachment', filename=attachment_file_name)
    msg.attach(attachment_part)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container
    msg.attach(msg_body)

    # Send the email
    try:
        response = ses_client.send_raw_email(
            Source=sender_email,
            Destinations=[recipient_email],
            RawMessage={'Data': msg.as_string()}
        )
        print("Email sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Email sending failed:", e)



def lambda_handler(event, context):
    print("even : ")
    print(event)
    print("context")
    print(context)
    
    body = json.loads(event['Records'][0]['body'].replace("'", "\""))
    print("body")
    print(body)    
    # Example usage
    sender_email = 'pp2959@nyu.edu'
    recipient_email = body.pop('email')
    subject = "Your weekly Health report is ready !"
    body_text = "Please find your weekly health report attached with this mail."
    attachment_file_name = 'health_report.pdf'
    attachment_data = generate_pdf_from_data(body)
    
    send_email_with_attachment(sender_email, recipient_email, subject, body_text, attachment_file_name, attachment_data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# Example data
# data = { 'heartrate': [{'Time': 'May 06, 01 PM', 'Average Heartrate': 71.0}, {'Time': 'May 09, 09 AM', 'Average Heartrate': 85.0}, {'Time': 'May 09, 11 AM', 'Average Heartrate': 77.61925240345037}, {'Time': 'May 09, 12 PM', 'Average Heartrate': 89.5}, {'Time': 'May 09, 01 PM', 'Average Heartrate': 78.0}, {'Time': 'May 09, 02 PM', 'Average Heartrate': 76.49494609928132}, {'Time': 'May 09, 03 PM', 'Average Heartrate': 80.90168944583644}, {'Time': 'May 09, 04 PM', 'Average Heartrate': 75.42296010360093}, {'Time': 'May 09, 05 PM', 'Average Heartrate': 76.0}, {'Time': 'May 09, 06 PM', 'Average Heartrate': 75.63648979243274}, {'Time': 'May 09, 07 PM', 'Average Heartrate': 109.23357480325807}, {'Time': 'May 10, 04 PM', 'Average Heartrate': 77.0}, {'Time': 'May 10, 05 PM', 'Average Heartrate': 73.16667231500622}, {'Time': 'May 10, 06 PM', 'Average Heartrate': 75.00171146830385}, {'Time': 'May 10, 07 PM', 'Average Heartrate': 75.37504656393573}, {'Time': 'May 10, 08 PM', 'Average Heartrate': 95.70090679945625}], 'restingHeartRate': [{'Time': 'May 06, 01 PM', 'Average Resting Heartrate': 71}, {'Time': 'May 09, 09 AM', 'Average Resting Heartrate': 85}, {'Time': 'May 09, 11 AM', 'Average Resting Heartrate': 77}, {'Time': 'May 09, 12 PM', 'Average Resting Heartrate': 89}, {'Time': 'May 09, 01 PM', 'Average Resting Heartrate': 78}, {'Time': 'May 09, 02 PM', 'Average Resting Heartrate': 76}, {'Time': 'May 09, 03 PM', 'Average Resting Heartrate': 80}, {'Time': 'May 09, 04 PM', 'Average Resting Heartrate': 75}, {'Time': 'May 09, 05 PM', 'Average Resting Heartrate': 76}, {'Time': 'May 09, 06 PM', 'Average Resting Heartrate': 75}, {'Time': 'May 09, 07 PM', 'Average Resting Heartrate': 109}, {'Time': 'May 10, 04 PM', 'Average Resting Heartrate': 77}, {'Time': 'May 10, 05 PM', 'Average Resting Heartrate': 73}, {'Time': 'May 10, 06 PM', 'Average Resting Heartrate': 75}, {'Time': 'May 10, 07 PM', 'Average Resting Heartrate': 75}, {'Time': 'May 10, 08 PM', 'Average Resting Heartrate': 95}], 'steps': [{'Time': 'May 06, 12 AM', 'Average Steps': 60}, {'Time': 'May 06, 01 AM', 'Average Steps': 60}, {'Time': 'May 06, 02 AM', 'Average Steps': 60}, {'Time': 'May 06, 03 AM', 'Average Steps': 60}, {'Time': 'May 06, 04 AM', 'Average Steps': 60}, {'Time': 'May 06, 05 AM', 'Average Steps': 60}, {'Time': 'May 06, 06 AM', 'Average Steps': 60}, {'Time': 'May 06, 07 AM', 'Average Steps': 60}, {'Time': 'May 06, 08 AM', 'Average Steps': 60}, {'Time': 'May 06, 09 AM', 'Average Steps': 60}, {'Time': 'May 06, 10 AM', 'Average Steps': 60}, {'Time': 'May 06, 11 AM', 'Average Steps': 60}, {'Time': 'May 06, 12 PM', 'Average Steps': 60}, {'Time': 'May 06, 01 PM', 'Average Steps': 60}, {'Time': 'May 06, 02 PM', 'Average Steps': 60}, {'Time': 'May 06, 03 PM', 'Average Steps': 60}, {'Time': 'May 06, 04 PM', 'Average Steps': 60}, {'Time': 'May 06, 05 PM', 'Average Steps': 60}, {'Time': 'May 06, 06 PM', 'Average Steps': 60}, {'Time': 'May 06, 07 PM', 'Average Steps': 60}, {'Time': 'May 06, 08 PM', 'Average Steps': 60}, {'Time': 'May 06, 09 PM', 'Average Steps': 60}, {'Time': 'May 06, 10 PM', 'Average Steps': 60}, {'Time': 'May 06, 11 PM', 'Average Steps': 31}, {'Time': 'May 07, 12 AM', 'Average Steps': 18}, {'Time': 'May 07, 01 AM', 'Average Steps': 18}, {'Time': 'May 07, 02 AM', 'Average Steps': 18}, {'Time': 'May 07, 03 AM', 'Average Steps': 18}, {'Time': 'May 07, 04 AM', 'Average Steps': 18}, {'Time': 'May 07, 05 AM', 'Average Steps': 18}, {'Time': 'May 07, 06 AM', 'Average Steps': 18}, {'Time': 'May 07, 07 AM', 'Average Steps': 18}, {'Time': 'May 07, 08 AM', 'Average Steps': 18}, {'Time': 'May 07, 09 AM', 'Average Steps': 18}, {'Time': 'May 07, 10 AM', 'Average Steps': 18}, {'Time': 'May 07, 11 AM', 'Average Steps': 18}, {'Time': 'May 07, 12 PM', 'Average Steps': 18}, {'Time': 'May 07, 01 PM', 'Average Steps': 18}, {'Time': 'May 07, 02 PM', 'Average Steps': 18}, {'Time': 'May 07, 03 PM', 'Average Steps': 18}, {'Time': 'May 07, 04 PM', 'Average Steps': 18}, {'Time': 'May 07, 05 PM', 'Average Steps': 18}, {'Time': 'May 07, 06 PM', 'Average Steps': 18}, {'Time': 'May 07, 07 PM', 'Average Steps': 18}, {'Time': 'May 07, 08 PM', 'Average Steps': 18}, {'Time': 'May 07, 09 PM', 'Average Steps': 18}, {'Time': 'May 07, 10 PM', 'Average Steps': 18}, {'Time': 'May 07, 11 PM', 'Average Steps': 21}, {'Time': 'May 08, 12 AM', 'Average Steps': 22}, {'Time': 'May 08, 01 AM', 'Average Steps': 22}, {'Time': 'May 08, 02 AM', 'Average Steps': 22}, {'Time': 'May 08, 03 AM', 'Average Steps': 22}, {'Time': 'May 08, 04 AM', 'Average Steps': 22}, {'Time': 'May 08, 05 AM', 'Average Steps': 22}, {'Time': 'May 08, 06 AM', 'Average Steps': 22}, {'Time': 'May 08, 07 AM', 'Average Steps': 22}, {'Time': 'May 08, 08 AM', 'Average Steps': 22}, {'Time': 'May 08, 09 AM', 'Average Steps': 22}, {'Time': 'May 08, 10 AM', 'Average Steps': 22}, {'Time': 'May 08, 11 AM', 'Average Steps': 22}, {'Time': 'May 08, 12 PM', 'Average Steps': 22}, {'Time': 'May 08, 01 PM', 'Average Steps': 22}, {'Time': 'May 08, 02 PM', 'Average Steps': 22}, {'Time': 'May 08, 03 PM', 'Average Steps': 22}, {'Time': 'May 08, 04 PM', 'Average Steps': 22}, {'Time': 'May 08, 05 PM', 'Average Steps': 22}, {'Time': 'May 08, 06 PM', 'Average Steps': 22}, {'Time': 'May 08, 07 PM', 'Average Steps': 22}, {'Time': 'May 08, 08 PM', 'Average Steps': 22}, {'Time': 'May 08, 09 PM', 'Average Steps': 22}, {'Time': 'May 08, 10 PM', 'Average Steps': 22}, {'Time': 'May 08, 11 PM', 'Average Steps': 172}, {'Time': 'May 09, 12 AM', 'Average Steps': 244}, {'Time': 'May 09, 01 AM', 'Average Steps': 244}, {'Time': 'May 09, 02 AM', 'Average Steps': 244}, {'Time': 'May 09, 03 AM', 'Average Steps': 244}, {'Time': 'May 09, 04 AM', 'Average Steps': 244}, {'Time': 'May 09, 05 AM', 'Average Steps': 244}, {'Time': 'May 09, 06 AM', 'Average Steps': 244}, {'Time': 'May 09, 07 AM', 'Average Steps': 244}, {'Time': 'May 09, 08 AM', 'Average Steps': 244}, {'Time': 'May 09, 09 AM', 'Average Steps': 244}, {'Time': 'May 09, 10 AM', 'Average Steps': 244}, {'Time': 'May 09, 11 AM', 'Average Steps': 244}, {'Time': 'May 09, 12 PM', 'Average Steps': 244}, {'Time': 'May 09, 01 PM', 'Average Steps': 244}, {'Time': 'May 09, 02 PM', 'Average Steps': 244}, {'Time': 'May 09, 03 PM', 'Average Steps': 244}, {'Time': 'May 09, 04 PM', 'Average Steps': 244}, {'Time': 'May 09, 05 PM', 'Average Steps': 244}, {'Time': 'May 09, 06 PM', 'Average Steps': 244}, {'Time': 'May 09, 07 PM', 'Average Steps': 243}, {'Time': 'May 09, 08 PM', 'Average Steps': 244}, {'Time': 'May 09, 09 PM', 'Average Steps': 244}, {'Time': 'May 09, 10 PM', 'Average Steps': 244}, {'Time': 'May 09, 11 PM', 'Average Steps': 188}, {'Time': 'May 10, 12 AM', 'Average Steps': 162}, {'Time': 'May 10, 01 AM', 'Average Steps': 162}, {'Time': 'May 10, 02 AM', 'Average Steps': 162}, {'Time': 'May 10, 03 AM', 'Average Steps': 162}, {'Time': 'May 10, 04 AM', 'Average Steps': 162}, {'Time': 'May 10, 05 AM', 'Average Steps': 162}, {'Time': 'May 10, 06 AM', 'Average Steps': 162}, {'Time': 'May 10, 07 AM', 'Average Steps': 162}, {'Time': 'May 10, 08 AM', 'Average Steps': 162}, {'Time': 'May 10, 09 AM', 'Average Steps': 162}, {'Time': 'May 10, 10 AM', 'Average Steps': 162}, {'Time': 'May 10, 11 AM', 'Average Steps': 162}, {'Time': 'May 10, 12 PM', 'Average Steps': 162}, {'Time': 'May 10, 01 PM', 'Average Steps': 162}, {'Time': 'May 10, 02 PM', 'Average Steps': 162}, {'Time': 'May 10, 03 PM', 'Average Steps': 162}, {'Time': 'May 10, 04 PM', 'Average Steps': 162}, {'Time': 'May 10, 05 PM', 'Average Steps': 162}, {'Time': 'May 10, 06 PM', 'Average Steps': 162}, {'Time': 'May 10, 07 PM', 'Average Steps': 162}, {'Time': 'May 10, 08 PM', 'Average Steps': 162}, {'Time': 'May 10, 09 PM', 'Average Steps': 162}, {'Time': 'May 10, 10 PM', 'Average Steps': 162}, {'Time': 'May 10, 11 PM', 'Average Steps': 189}, {'Time': 'May 11, 12 AM', 'Average Steps': 202}, {'Time': 'May 11, 01 AM', 'Average Steps': 202}, {'Time': 'May 11, 02 AM', 'Average Steps': 202}, {'Time': 'May 11, 03 AM', 'Average Steps': 202}, {'Time': 'May 11, 04 AM', 'Average Steps': 202}, {'Time': 'May 11, 05 AM', 'Average Steps': 202}, {'Time': 'May 11, 06 AM', 'Average Steps': 202}, {'Time': 'May 11, 07 AM', 'Average Steps': 202}, {'Time': 'May 11, 08 AM', 'Average Steps': 202}, {'Time': 'May 11, 09 AM', 'Average Steps': 202}, {'Time': 'May 11, 10 AM', 'Average Steps': 202}, {'Time': 'May 11, 11 AM', 'Average Steps': 202}, {'Time': 'May 11, 12 PM', 'Average Steps': 202}, {'Time': 'May 11, 01 PM', 'Average Steps': 202}, {'Time': 'May 11, 02 PM', 'Average Steps': 202}, {'Time': 'May 11, 03 PM', 'Average Steps': 202}, {'Time': 'May 11, 04 PM', 'Average Steps': 202}, {'Time': 'May 11, 05 PM', 'Average Steps': 202}, {'Time': 'May 11, 06 PM', 'Average Steps': 202}, {'Time': 'May 11, 07 PM', 'Average Steps': 202}, {'Time': 'May 11, 08 PM', 'Average Steps': 202}, {'Time': 'May 11, 09 PM', 'Average Steps': 202}, {'Time': 'May 11, 10 PM', 'Average Steps': 202}, {'Time': 'May 11, 11 PM', 'Average Steps': 114}, {'Time': 'May 12, 12 AM', 'Average Steps': 71}, {'Time': 'May 12, 01 AM', 'Average Steps': 71}, {'Time': 'May 12, 02 AM', 'Average Steps': 71}, {'Time': 'May 12, 03 AM', 'Average Steps': 71}, {'Time': 'May 12, 04 AM', 'Average Steps': 71}, {'Time': 'May 12, 05 AM', 'Average Steps': 71}, {'Time': 'May 12, 06 AM', 'Average Steps': 71}, {'Time': 'May 12, 07 AM', 'Average Steps': 71}, {'Time': 'May 12, 08 AM', 'Average Steps': 71}, {'Time': 'May 12, 09 AM', 'Average Steps': 71}, {'Time': 'May 12, 10 AM', 'Average Steps': 71}, {'Time': 'May 12, 11 AM', 'Average Steps': 71}, {'Time': 'May 12, 12 PM', 'Average Steps': 71}, {'Time': 'May 12, 01 PM', 'Average Steps': 71}, {'Time': 'May 12, 02 PM', 'Average Steps': 71}, {'Time': 'May 12, 03 PM', 'Average Steps': 71}, {'Time': 'May 12, 04 PM', 'Average Steps': 71}, {'Time': 'May 12, 05 PM', 'Average Steps': 71}, {'Time': 'May 12, 06 PM', 'Average Steps': 71}, {'Time': 'May 12, 07 PM', 'Average Steps': 71}, {'Time': 'May 12, 08 PM', 'Average Steps': 71}, {'Time': 'May 12, 09 PM', 'Average Steps': 71}, {'Time': 'May 12, 10 PM', 'Average Steps': 71}, {'Time': 'May 12, 11 PM', 'Average Steps': 23}], 'sleep': [{'Time': 'May 09, 11 PM', 'Sleep Score': 0}], 'oxygen_saturation': [{'Time': 'May 10, 10 AM', 'Average Oxygen Saturation': 99}], 'activities': [{'Activity': 'Weightlifting', 'Duration(Min)': 30}, {'Activity': 'Badminton', 'Duration(Min)': 30}, {'Activity': 'Walking', 'Duration(Min)': 27}], 'blood_glucose': [{'Time': 'May 10, 12 PM', 'Average Blood Glucose': 3}, {'Time': 'May 11, 12 PM', 'Average Blood Glucose': 3}], 'blood_pressure': [{'Time': 'May 10, 12 PM', 'Average Blood Pressure': 117}, {'Time': 'May 11, 12 PM', 'Average Blood Pressure': 120}]}


# Generate PDF and save to file


