"""
24. XML Parser - XML 파일 파싱 및 생성
"""
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class XMLParser:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.tree = None
        self.root = None

    def parse(self, file_path=None):
        """XML 파일 파싱"""
        file_path = file_path or self.file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        print(f"Parsed XML: {file_path}")
        return self.root

    def parse_string(self, xml_string):
        """XML 문자열 파싱"""
        self.root = ET.fromstring(xml_string)
        return self.root

    def find_all(self, tag):
        """모든 태그 찾기"""
        return self.root.findall(f".//{tag}")

    def find_one(self, tag):
        """태그 하나 찾기"""
        return self.root.find(f".//{tag}")

    def get_text(self, element):
        """요소의 텍스트 가져오기"""
        return element.text if element is not None else None

    def get_attribute(self, element, attr_name):
        """속성 값 가져오기"""
        return element.get(attr_name) if element is not None else None

    def to_dict(self, element=None):
        """XML을 딕셔너리로 변환"""
        element = element or self.root

        result = {element.tag: {} if element.attrib else None}
        children = list(element)

        if children:
            dd = {}
            for child in children:
                child_dict = self.to_dict(child)
                for k, v in child_dict.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            result = {element.tag: dd}

        if element.attrib:
            result[element.tag] = {'@attributes': element.attrib}
            if children:
                result[element.tag].update(dd)

        if element.text:
            text = element.text.strip()
            if children or element.attrib:
                if text:
                    result[element.tag]['#text'] = text
            else:
                result[element.tag] = text

        return result

    def create_element(self, tag, text=None, attrib=None):
        """새 요소 생성"""
        element = ET.Element(tag, attrib or {})
        if text:
            element.text = text
        return element

    def save(self, file_path=None):
        """XML 파일 저장"""
        file_path = file_path or self.file_path

        # Pretty print
        xml_str = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="  ")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)

        print(f"Saved XML to {file_path}")

if __name__ == '__main__':
    # XML 생성 예제
    root = ET.Element("bookstore")

    book1 = ET.SubElement(root, "book", category="cooking")
    ET.SubElement(book1, "title").text = "Everyday Italian"
    ET.SubElement(book1, "author").text = "Giada De Laurentiis"
    ET.SubElement(book1, "year").text = "2005"
    ET.SubElement(book1, "price").text = "30.00"

    book2 = ET.SubElement(root, "book", category="programming")
    ET.SubElement(book2, "title").text = "Python Programming"
    ET.SubElement(book2, "author").text = "John Smith"
    ET.SubElement(book2, "year").text = "2023"
    ET.SubElement(book2, "price").text = "45.00"

    # 저장
    parser = XMLParser('bookstore.xml')
    parser.root = root
    parser.save()

    # 파싱
    parser.parse('bookstore.xml')
    print("\n=== All Books ===")
    books = parser.find_all('book')
    for book in books:
        title = book.find('title').text
        author = book.find('author').text
        price = book.find('price').text
        print(f"{title} by {author} - ${price}")

    # 딕셔너리로 변환
    print("\n=== As Dictionary ===")
    data_dict = parser.to_dict()
    print(data_dict)
