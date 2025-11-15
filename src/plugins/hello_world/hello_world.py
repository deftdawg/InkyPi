from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image, ImageColor, ImageDraw, ImageFont
from utils.app_utils import get_font
import logging

logger = logging.getLogger(__name__)

class HelloWorld(BasePlugin):
    def generate_image(self, settings, device_config):
        name = settings.get('name', 'World')
        foreground_color = settings.get('foregroundColor', '#000000')
        background_color = settings.get('backgroundColor', '#ffffff')
        font_size = float(settings.get('fontSize', '50'))
        
        # Convert hex colors to RGB tuples
        fg_rgb = ImageColor.getcolor(foreground_color, "RGB")
        bg_rgb = ImageColor.getcolor(background_color, "RGB")
        
        # Get device dimensions
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]
        
        w, h = dimensions
        
        # Create image with background color
        img = Image.new("RGB", (w, h), bg_rgb)
        draw = ImageDraw.Draw(img)
        
        # Draw centered H1 text
        text = f"Hello {name}"
        
        # Get font with specified size, scaling down if text doesn't fit
        font = get_font("Jost", font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Scale down if text is too large for the image (with 10px margin)
        margin = 10
        if text_width > w - margin or text_height > h - margin:
            scale_factor_w = (w - margin) / text_width if text_width > 0 else 1
            scale_factor_h = (h - margin) / text_height if text_height > 0 else 1
            scale_factor = min(scale_factor_w, scale_factor_h)
            font_size = max(font_size * scale_factor, 10)
            font = get_font("Jost", font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        
        x = (w - text_width) // 2
        y = (h - text_height) // 2
        
        draw.text((x, y), text, fill=fg_rgb, font=font)
        
        return img
