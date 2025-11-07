from PIL import Image
import io
import pytesseract


def parse_image(data: bytes) -> str:
    image = Image.open(io.BytesIO(data))
    text = pytesseract.image_to_string(image)
    return text.strip()


