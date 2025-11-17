"""
02. Web Scraper - BeautifulSoup을 이용한 웹 스크래핑
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_page(self):
        """웹페이지 가져오기"""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching page: {e}")
            return False

    def extract_links(self):
        """모든 링크 추출"""
        if not self.soup:
            return []

        links = []
        for link in self.soup.find_all('a', href=True):
            links.append({
                'text': link.get_text(strip=True),
                'url': link['href']
            })
        return links

    def extract_images(self):
        """모든 이미지 추출"""
        if not self.soup:
            return []

        images = []
        for img in self.soup.find_all('img', src=True):
            images.append({
                'alt': img.get('alt', ''),
                'src': img['src']
            })
        return images

    def extract_text(self):
        """모든 텍스트 추출"""
        if not self.soup:
            return ""

        # 스크립트와 스타일 제거
        for script in self.soup(['script', 'style']):
            script.decompose()

        return self.soup.get_text(separator='\n', strip=True)

    def save_results(self, filename='scraped_data.json'):
        """결과를 JSON 파일로 저장"""
        data = {
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'links': self.extract_links(),
            'images': self.extract_images(),
            'text_preview': self.extract_text()[:500]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Results saved to {filename}")

if __name__ == '__main__':
    # 예제 사용
    url = 'https://example.com'
    scraper = WebScraper(url)

    if scraper.fetch_page():
        print(f"Successfully fetched: {url}")
        print(f"Found {len(scraper.extract_links())} links")
        print(f"Found {len(scraper.extract_images())} images")
        scraper.save_results()
    else:
        print("Failed to fetch the page")
