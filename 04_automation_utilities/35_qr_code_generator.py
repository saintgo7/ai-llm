"""
35. QR Code Generator - QR 코드 생성기
"""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import io
from PIL import Image

class QRCodeGenerator:
    def __init__(self):
        self.qr = None

    def create_basic(self, data, size=10, border=4):
        """기본 QR 코드 생성"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )

        qr.add_data(data)
        qr.make(fit=True)

        return qr.make_image(fill_color="black", back_color="white")

    def create_colored(self, data, fill_color='blue', back_color='white'):
        """컬러 QR 코드 생성"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        return qr.make_image(fill_color=fill_color, back_color=back_color)

    def create_styled(self, data, module_drawer='rounded'):
        """스타일이 있는 QR 코드 생성"""
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)

        drawer = RoundedModuleDrawer() if module_drawer == 'rounded' else CircleModuleDrawer()

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer
        )

        return img

    def create_with_logo(self, data, logo_path, logo_size_ratio=0.3):
        """로고가 포함된 QR 코드 생성"""
        # QR 코드 생성 (높은 에러 정정)
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # 로고 추가
        logo = Image.open(logo_path)

        # 로고 크기 조정
        qr_width, qr_height = img.size
        logo_size = int(qr_width * logo_size_ratio)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # 로고를 중앙에 배치
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img.paste(logo, logo_pos)

        return img

    def save_qr_code(self, qr_image, filename='qrcode.png'):
        """QR 코드 저장"""
        qr_image.save(filename)
        print(f"QR code saved to {filename}")

    def qr_to_bytes(self, qr_image):
        """QR 코드를 바이트로 변환"""
        byte_io = io.BytesIO()
        qr_image.save(byte_io, format='PNG')
        return byte_io.getvalue()

class QRCodeScanner:
    """QR 코드 스캐너 (PIL 사용)"""

    @staticmethod
    def decode_from_file(filename):
        """파일에서 QR 코드 디코딩"""
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image

            img = Image.open(filename)
            decoded_objects = decode(img)

            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'rect': obj.rect
                })

            return results
        except ImportError:
            print("pyzbar not installed. Install with: pip install pyzbar")
            return []

# 사용 예제
if __name__ == '__main__':
    generator = QRCodeGenerator()

    print("=== QR Code Generator ===\n")

    # 1. 기본 QR 코드
    print("1. Generating basic QR code...")
    basic_qr = generator.create_basic("https://www.example.com")
    generator.save_qr_code(basic_qr, "basic_qr.png")

    # 2. 컬러 QR 코드
    print("2. Generating colored QR code...")
    colored_qr = generator.create_colored(
        "https://www.example.com",
        fill_color="darkblue",
        back_color="lightblue"
    )
    generator.save_qr_code(colored_qr, "colored_qr.png")

    # 3. 스타일 QR 코드
    print("3. Generating styled QR code...")
    styled_qr = generator.create_styled(
        "https://www.example.com",
        module_drawer='rounded'
    )
    generator.save_qr_code(styled_qr, "styled_qr.png")

    # 4. Wi-Fi QR 코드
    print("4. Generating Wi-Fi QR code...")
    wifi_qr_data = "WIFI:T:WPA;S:MyNetwork;P:mypassword;;"
    wifi_qr = generator.create_basic(wifi_qr_data)
    generator.save_qr_code(wifi_qr, "wifi_qr.png")

    # 5. vCard QR 코드
    print("5. Generating vCard QR code...")
    vcard = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD"""
    vcard_qr = generator.create_basic(vcard)
    generator.save_qr_code(vcard_qr, "vcard_qr.png")

    print("\nNote: Install qrcode with: pip install qrcode[pil]")
    print("For QR scanning, install: pip install pyzbar")

    # QR 코드 스캔 예제
    print("\n=== QR Code Scanner ===")
    results = QRCodeScanner.decode_from_file("basic_qr.png")
    if results:
        for result in results:
            print(f"Type: {result['type']}")
            print(f"Data: {result['data']}")
    else:
        print("Could not decode QR code (pyzbar may not be installed)")
