"""
Read Screen Skill for Jarvis AI
Handles screen reading and OCR functionality
"""

import os
import time
from typing import List, Dict, Optional, Tuple
import base64
from io import BytesIO

try:
    import pyautogui
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    print("Some dependencies not installed. Install with: pip install pyautogui pytesseract pillow")


class ReadScreenSkill:
    """Skill for screen reading and OCR operations"""
    
    def __init__(self):
        # Configure pytesseract path if needed (Windows specific)
        tesseract_path = os.getenv("TESSERACT_PATH")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Disable pyautogui failsafe for automation
        pyautogui.FAILSAFE = False
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """
        Capture screenshot of screen or specific region
        
        Args:
            region: Tuple of (left, top, width, height) for specific region
            
        Returns:
            PIL.Image: Screenshot image
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {str(e)}")
            return None
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image to preprocess
            
        Returns:
            PIL.Image: Preprocessed image
        """
        try:
            # Convert to grayscale
            gray = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            blurred = enhanced.filter(ImageFilter.MedianFilter(size=1))
            
            # Scale up image for better OCR
            width, height = blurred.size
            scaled = blurred.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
            
            return scaled
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return image
    
    def extract_text_from_image(self, image: Image.Image, preprocess: bool = True) -> str:
        """
        Extract text from image using OCR
        
        Args:
            image: PIL Image to extract text from
            preprocess: Whether to preprocess image for better OCR
            
        Returns:
            str: Extracted text
        """
        try:
            if preprocess:
                image = self.preprocess_image(image)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image, config='--psm 6')
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}")
            return ""
    
    def read_screen_text(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """
        Read text from screen or specific region
        
        Args:
            region: Tuple of (left, top, width, height) for specific region
            
        Returns:
            str: Text found on screen
        """
        screenshot = self.capture_screen(region)
        if screenshot:
            return self.extract_text_from_image(screenshot)
        return ""
    
    def find_text_on_screen(self, search_text: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
        """
        Search for specific text on screen
        
        Args:
            search_text: Text to search for
            region: Specific region to search in
            
        Returns:
            bool: True if text found, False otherwise
        """
        screen_text = self.read_screen_text(region)
        return search_text.lower() in screen_text.lower()
    
    def get_screen_elements(self, region: Optional[Tuple[int, int, int, int]] = None) -> List[Dict]:
        """
        Get detailed information about screen elements
        
        Args:
            region: Specific region to analyze
            
        Returns:
            List[Dict]: List of detected elements with positions and text
        """
        try:
            screenshot = self.capture_screen(region)
            if not screenshot:
                return []
            
            # Get detailed OCR data with bounding boxes
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            
            elements = []
            n_boxes = len(data['level'])
            
            for i in range(n_boxes):
                confidence = int(data['conf'][i])
                if confidence > 50:  # Filter low confidence detections
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    text = data['text'][i].strip()
                    
                    if text:  # Only include elements with text
                        elements.append({
                            'text': text,
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'confidence': confidence
                        })
            
            return elements
        except Exception as e:
            print(f"Error getting screen elements: {str(e)}")
            return []
    
    def save_screenshot(self, filename: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
        """
        Save screenshot to file
        
        Args:
            filename: Path to save screenshot
            region: Specific region to capture
            
        Returns:
            bool: True if saved successfully
        """
        try:
            screenshot = self.capture_screen(region)
            if screenshot:
                screenshot.save(filename)
                return True
            return False
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")
            return False
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get screen dimensions
        
        Returns:
            Tuple[int, int]: (width, height) of screen
        """
        try:
            return pyautogui.size()
        except Exception as e:
            print(f"Error getting screen size: {str(e)}")
            return (0, 0)


def read_full_screen() -> str:
    """
    Read all text from the entire screen
    
    Returns:
        str: All text found on screen
    """
    skill = ReadScreenSkill()
    text = skill.read_screen_text()
    
    if text:
        return f"Screen content:\n{text}"
    else:
        return "Unable to read screen content"


def read_screen_region(left: int, top: int, width: int, height: int) -> str:
    """
    Read text from specific screen region
    
    Args:
        left: Left coordinate
        top: Top coordinate
        width: Width of region
        height: Height of region
        
    Returns:
        str: Text found in the region
    """
    skill = ReadScreenSkill()
    text = skill.read_screen_text(region=(left, top, width, height))
    
    if text:
        return f"Region content:\n{text}"
    else:
        return "No text found in the specified region"


def find_text_on_screen(search_text: str) -> str:
    """
    Search for specific text on screen
    
    Args:
        search_text: Text to search for
        
    Returns:
        str: Result message
    """
    skill = ReadScreenSkill()
    found = skill.find_text_on_screen(search_text)
    
    if found:
        return f"Text '{search_text}' found on screen"
    else:
        return f"Text '{search_text}' not found on screen"


def take_screenshot(filename: str = None) -> str:
    """
    Take a screenshot and optionally save it
    
    Args:
        filename: Optional filename to save screenshot
        
    Returns:
        str: Status message
    """
    skill = ReadScreenSkill()
    
    if filename:
        success = skill.save_screenshot(filename)
        if success:
            return f"Screenshot saved as {filename}"
        else:
            return "Failed to save screenshot"
    else:
        # Just take screenshot without saving
        screenshot = skill.capture_screen()
        if screenshot:
            return "Screenshot taken successfully"
        else:
            return "Failed to take screenshot"


def describe_screen() -> str:
    """
    Provide a description of what's currently on screen
    
    Returns:
        str: Description of screen content
    """
    skill = ReadScreenSkill()
    elements = skill.get_screen_elements()
    
    if not elements:
        return "Unable to analyze screen content"
    
    # Summarize screen content
    text_elements = [elem['text'] for elem in elements if len(elem['text']) > 3]
    
    if text_elements:
        return f"Screen contains the following text elements: {', '.join(text_elements[:10])}"
    else:
        return "Screen appears to contain mostly graphical content with minimal text"