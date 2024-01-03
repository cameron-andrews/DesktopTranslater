from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self, language='chi_sim'):
        """
        Initialize OCRProcessor with the specified language.

        :param language: Language code for OCR (default is 'eng' for English).
        """
        self.language = language

    def perform_ocr(self, image: Image):
        """
        Perform OCR on the given image using the specified language.

        :param image: Path to the image file.
        :return: Extracted text from the image.
        """
        if image is None:
            return None
        try:
            # Set the language for OCR
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract installation path
            custom_config = f'--oem 3 --psm 6 -l {self.language}'
            # Perform OCR on the image
            result = pytesseract.image_to_string(image, config=custom_config)

            return result.strip()
        except Exception as e:
            print(f"Error during OCR: {str(e)}")
            return None