from PIL import Image
import base64
import io
from fastapi import UploadFile, HTTPException
from typing import Tuple

class ImageProcessor:
    """Handles image upload, validation, and processing"""
    
    # Supported formats
    ALLOWED_FORMATS = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}
    
    # Max dimensions (saves API costs)
    MAX_WIDTH = 1024
    MAX_HEIGHT = 1024
    
    # Max file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    async def validate_image(file: UploadFile) -> None:
        """Validate uploaded file is an image"""
        
        # Check content type
        if file.content_type not in ImageProcessor.ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed: JPEG, PNG, WebP"
            )
        
        # Check file size
        file.file.seek(0, 2)  # Move to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > ImageProcessor.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: 10MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
    
    @staticmethod
    async def process_image(file: UploadFile) -> Tuple[str, dict]:
        """
        Process uploaded image: validate, resize, convert to base64
        
        Returns:
            Tuple of (base64_string, metadata)
        """
        
        # Validate first
        await ImageProcessor.validate_image(file)
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get original dimensions
        original_width, original_height = image.size
        
        # Convert to RGB if needed (handles RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large (maintains aspect ratio)
        if original_width > ImageProcessor.MAX_WIDTH or original_height > ImageProcessor.MAX_HEIGHT:
            image.thumbnail((ImageProcessor.MAX_WIDTH, ImageProcessor.MAX_HEIGHT), Image.Resampling.LANCZOS)
        
        # Get final dimensions
        final_width, final_height = image.size
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85, optimize=True)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Metadata
        metadata = {
            "original_dimensions": f"{original_width}x{original_height}",
            "processed_dimensions": f"{final_width}x{final_height}",
            "format": "JPEG",
            "was_resized": (original_width != final_width or original_height != final_height)
        }
        
        return img_base64, metadata
    
    @staticmethod
    def estimate_image_quality(metadata: dict) -> str:
        """Estimate if image quality is good enough for analysis"""
        
        width, height = map(int, metadata["processed_dimensions"].split('x'))
        total_pixels = width * height
        
        if total_pixels >= 786432:  # 1024x768 or better
            return "excellent"
        elif total_pixels >= 307200:  # 640x480 or better
            return "good"
        elif total_pixels >= 76800:   # 320x240 or better
            return "acceptable"
        else:
            return "poor - may affect analysis accuracy"