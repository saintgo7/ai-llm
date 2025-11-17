"""
07. Image Processor - PIL/Pillow를 이용한 이미지 처리
"""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import os

class ImageProcessor:
    def __init__(self, image_path):
        """
        이미지 처리 클래스 초기화

        Args:
            image_path: 처리할 이미지 파일 경로
        """
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()

    def reset(self):
        """원본 이미지로 리셋"""
        self.image = self.original_image.copy()

    def resize(self, width, height, maintain_aspect=True):
        """이미지 크기 조정"""
        if maintain_aspect:
            self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return self

    def rotate(self, angle):
        """이미지 회전"""
        self.image = self.image.rotate(angle, expand=True)
        return self

    def flip_horizontal(self):
        """좌우 반전"""
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return self

    def flip_vertical(self):
        """상하 반전"""
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return self

    def crop(self, left, top, right, bottom):
        """이미지 자르기"""
        self.image = self.image.crop((left, top, right, bottom))
        return self

    def apply_blur(self, radius=2):
        """블러 효과 적용"""
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def apply_sharpen(self):
        """샤프닝 효과 적용"""
        self.image = self.image.filter(ImageFilter.SHARPEN)
        return self

    def apply_edge_enhance(self):
        """엣지 강화"""
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        return self

    def adjust_brightness(self, factor):
        """
        밝기 조정
        factor > 1.0: 밝게, factor < 1.0: 어둡게
        """
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_contrast(self, factor):
        """
        대비 조정
        factor > 1.0: 대비 증가, factor < 1.0: 대비 감소
        """
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_saturation(self, factor):
        """
        채도 조정
        factor > 1.0: 채도 증가, factor < 1.0: 채도 감소
        """
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def convert_to_grayscale(self):
        """흑백 변환"""
        self.image = self.image.convert('L')
        return self

    def add_watermark(self, text, position='bottom-right', opacity=128):
        """
        워터마크 추가

        Args:
            text: 워터마크 텍스트
            position: 위치 ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            opacity: 투명도 (0-255)
        """
        # RGB 모드로 변환 (필요시)
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')

        # 워터마크 레이어 생성
        watermark_layer = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_layer)

        # 폰트 설정 (기본 폰트 사용)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 위치 계산
        margin = 10
        if position == 'top-left':
            x, y = margin, margin
        elif position == 'top-right':
            x, y = self.image.width - text_width - margin, margin
        elif position == 'bottom-left':
            x, y = margin, self.image.height - text_height - margin
        elif position == 'bottom-right':
            x, y = self.image.width - text_width - margin, self.image.height - text_height - margin
        else:  # center
            x = (self.image.width - text_width) // 2
            y = (self.image.height - text_height) // 2

        # 워터마크 그리기
        draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

        # 이미지 합성
        self.image = Image.alpha_composite(self.image, watermark_layer)
        return self

    def create_thumbnail(self, size=(128, 128)):
        """썸네일 생성"""
        thumbnail = self.original_image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail

    def save(self, output_path, quality=95):
        """이미지 저장"""
        # RGBA를 RGB로 변환 (JPEG는 RGBA 지원 안함)
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            if self.image.mode == 'RGBA':
                rgb_image = Image.new('RGB', self.image.size, (255, 255, 255))
                rgb_image.paste(self.image, mask=self.image.split()[3])
                rgb_image.save(output_path, quality=quality)
            else:
                self.image.save(output_path, quality=quality)
        else:
            self.image.save(output_path)

        print(f"Image saved to {output_path}")

    def get_info(self):
        """이미지 정보 반환"""
        return {
            'format': self.image.format,
            'mode': self.image.mode,
            'size': self.image.size,
            'width': self.image.width,
            'height': self.image.height
        }

if __name__ == '__main__':
    print("Image Processor - Image processing utilities")
    print("\nExample usage:")
    print("processor = ImageProcessor('input.jpg')")
    print("processor.resize(800, 600).adjust_brightness(1.2).apply_sharpen()")
    print("processor.save('output.jpg')")
