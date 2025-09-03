import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_report_email(recipient_email: str, meeting_title: str, report_path: str):
    """
    Send the analysis report via email
    
    Args:
        recipient_email (str): Email address to send the report to
        meeting_title (str): Title of the meeting for the email subject
        report_path (str): Path to the PDF report file
    """
    
    # Email configuration (you'll need to set these environment variables)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    sender_email = os.environ.get('SENDER_EMAIL', 'your-email@gmail.com')
    sender_password = os.environ.get('SENDER_PASSWORD', 'your-app-password')
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Sales Call Analysis Report - {meeting_title}"
        
        # Email body
        body = f"""
Hello!

Your sales call analysis report is ready. Please find the detailed analysis attached.

Meeting: {meeting_title}
Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

The report includes:
- Overall performance score
- Category-specific scores and feedback
- Conversation highlights
- Missed opportunities
- Actionable improvement suggestions
- Full transcript

Best regards,
Your Sales Analysis System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF report
        if os.path.exists(report_path):
            with open(report_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(report_path)}'
            )
            
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"Report email sent successfully to {recipient_email}")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # You might want to implement a fallback notification method here

