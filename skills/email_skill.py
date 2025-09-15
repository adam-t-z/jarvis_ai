"""
Email Skill for Jarvis AI
Handles email sending and reading functionality
"""

import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime


class EmailSkill:
    """Skill for email operations"""
    
    def __init__(self):
        self.smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.imap_server = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
        self.imap_port = int(os.getenv("EMAIL_IMAP_PORT", "993"))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
    
    def send_email(self, to_email: str, subject: str, body: str, cc: List[str] = None) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient's email address
            subject: Email subject
            body: Email body content
            cc: List of CC recipients (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.email_address or not self.email_password:
            print("Email credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Attach body
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.email_address, self.email_password)
            
            # Send email
            text = msg.as_string()
            recipients = [to_email] + (cc or [])
            server.sendmail(self.email_address, recipients, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def read_recent_emails(self, count: int = 5) -> List[Dict]:
        """
        Read recent emails from inbox
        
        Args:
            count: Number of recent emails to fetch
            
        Returns:
            List[Dict]: List of email dictionaries with subject, sender, date, body
        """
        if not self.email_address or not self.email_password:
            print("Email credentials not configured")
            return []
        
        emails = []
        
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select('inbox')
            
            # Search for all emails
            result, data = mail.search(None, 'ALL')
            email_ids = data[0].split()
            
            # Get recent emails
            recent_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
            
            for email_id in reversed(recent_ids):  # Most recent first
                result, data = mail.fetch(email_id, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # Extract email details
                subject = email_message['Subject']
                sender = email_message['From']
                date = email_message['Date']
                
                # Get email body
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = email_message.get_payload(decode=True).decode('utf-8')
                
                emails.append({
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body[:500] + "..." if len(body) > 500 else body  # Truncate long emails
                })
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Error reading emails: {str(e)}")
            
        return emails
    
    def search_emails(self, search_term: str, count: int = 10) -> List[Dict]:
        """
        Search emails by subject or sender
        
        Args:
            search_term: Term to search for
            count: Maximum number of results
            
        Returns:
            List[Dict]: List of matching email dictionaries
        """
        if not self.email_address or not self.email_password:
            print("Email credentials not configured")
            return []
        
        emails = []
        
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select('inbox')
            
            # Search in subject and sender
            result1, data1 = mail.search(None, f'SUBJECT "{search_term}"')
            result2, data2 = mail.search(None, f'FROM "{search_term}"')
            
            # Combine results
            email_ids = list(set(data1[0].split() + data2[0].split()))
            email_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
            
            for email_id in reversed(email_ids):
                result, data = mail.fetch(email_id, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                subject = email_message['Subject']
                sender = email_message['From']
                date = email_message['Date']
                
                emails.append({
                    'subject': subject,
                    'sender': sender,
                    'date': date
                })
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Error searching emails: {str(e)}")
            
        return emails


def send_email_to(recipient: str, subject: str, message: str) -> str:
    """
    Send an email to a recipient
    
    Args:
        recipient: Email address of recipient
        subject: Email subject
        message: Email body
        
    Returns:
        str: Status message
    """
    skill = EmailSkill()
    success = skill.send_email(recipient, subject, message)
    
    if success:
        return f"Email sent successfully to {recipient}"
    else:
        return f"Failed to send email to {recipient}"


def read_recent_emails(count: int = 5) -> str:
    """
    Read recent emails and return summary
    
    Args:
        count: Number of recent emails to read
        
    Returns:
        str: Summary of recent emails
    """
    skill = EmailSkill()
    emails = skill.read_recent_emails(count)
    
    if not emails:
        return "No recent emails found or unable to access email"
    
    summary = f"Here are your {len(emails)} most recent emails:\n\n"
    for i, email_data in enumerate(emails, 1):
        summary += f"{i}. From: {email_data['sender']}\n"
        summary += f"   Subject: {email_data['subject']}\n"
        summary += f"   Date: {email_data['date']}\n\n"
    
    return summary


def search_emails_by_term(search_term: str) -> str:
    """
    Search emails by term and return results
    
    Args:
        search_term: Term to search for
        
    Returns:
        str: Search results summary
    """
    skill = EmailSkill()
    emails = skill.search_emails(search_term)
    
    if not emails:
        return f"No emails found matching '{search_term}'"
    
    summary = f"Found {len(emails)} emails matching '{search_term}':\n\n"
    for i, email_data in enumerate(emails, 1):
        summary += f"{i}. From: {email_data['sender']}\n"
        summary += f"   Subject: {email_data['subject']}\n"
        summary += f"   Date: {email_data['date']}\n\n"
    
    return summary