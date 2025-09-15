"""
WhatsApp Skill for Jarvis AI
Handles WhatsApp messaging functionality
"""

import os
import requests
from typing import Optional


class WhatsAppSkill:
    """Skill for WhatsApp messaging operations"""
    
    def __init__(self):
        self.api_key = os.getenv("WHATSAPP_API_KEY")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.base_url = "https://graph.facebook.com/v17.0"
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a contact
        
        Args:
            to_number: Recipient's phone number (with country code)
            message: Message content to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.api_key or not self.phone_number_id:
            print("WhatsApp API credentials not configured")
            return False
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "text": {"body": message}
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"WhatsApp message sent successfully to {to_number}")
                return True
            else:
                print(f"Failed to send WhatsApp message: {response.text}")
                return False
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False
    
    def get_contacts(self) -> list:
        """
        Get list of WhatsApp contacts (placeholder implementation)
        
        Returns:
            list: List of contact dictionaries
        """
        # This would typically integrate with WhatsApp Business API
        # or a contacts database
        return []
    
    def search_contact(self, name: str) -> Optional[str]:
        """
        Search for a contact by name
        
        Args:
            name: Contact name to search for
            
        Returns:
            str: Phone number if found, None otherwise
        """
        # Placeholder implementation
        # In real implementation, this would search through contacts
        contacts_db = {
            "mom": "+1234567890",
            "dad": "+1234567891",
            "john": "+1234567892"
        }
        
        return contacts_db.get(name.lower())


def send_whatsapp_message(contact_name: str, message: str) -> str:
    """
    Send a WhatsApp message to a named contact
    
    Args:
        contact_name: Name of the contact
        message: Message to send
        
    Returns:
        str: Status message
    """
    skill = WhatsAppSkill()
    phone_number = skill.search_contact(contact_name)
    
    if not phone_number:
        return f"Contact '{contact_name}' not found"
    
    success = skill.send_message(phone_number, message)
    if success:
        return f"WhatsApp message sent to {contact_name}"
    else:
        return f"Failed to send WhatsApp message to {contact_name}"


def send_whatsapp_to_number(phone_number: str, message: str) -> str:
    """
    Send a WhatsApp message to a phone number
    
    Args:
        phone_number: Recipient's phone number
        message: Message to send
        
    Returns:
        str: Status message
    """
    skill = WhatsAppSkill()
    success = skill.send_message(phone_number, message)
    
    if success:
        return f"WhatsApp message sent to {phone_number}"
    else:
        return f"Failed to send WhatsApp message to {phone_number}"