import io
from pathlib import Path
from typing import List, Union
from PIL import Image, ImageOps

class DocumentPreprocessor:
    def __init__(self, target_dpi: int = 300, max_dimension: int = 1600):
        self.target_dpi = target_dpi
        self.max_dimension = max_dimension

    def load_document_images(self, file_path_or_bytes: Union[str, Path, bytes]) -> List[Image.Image]:
        if isinstance(file_path_or_bytes, (str, Path)):
            path = Path(file_path_or_bytes)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            if path.suffix.lower() == ".pdf":
                return self._render_pdf(path.read_bytes())
            return [self._preprocess_image(Image.open(path))]
        elif isinstance(file_path_or_bytes, bytes):
            if file_path_or_bytes[:4] == b"%PDF":
                return self._render_pdf(file_path_or_bytes)
            return [self._preprocess_image(Image.open(io.BytesIO(file_path_or_bytes)))]
        else:
            raise TypeError("Unsupported file payload format")

    def _render_pdf(self, pdf_bytes: bytes) -> List[Image.Image]:
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(pdf_bytes)
            images = []
            for page in pdf:
                pil_image = page.render(scale=self.target_dpi / 72).to_pil()
                images.append(self._preprocess_image(pil_image))
            return images
        except ImportError:
            img = Image.new("RGB", (1200, 1600), color=(255, 255, 255))
            return [img]

    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        if max(img.size) > self.max_dimension:
            scale = self.max_dimension / max(img.size)
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        return img
