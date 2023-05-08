import io
import sys

from PIL import Image
import pytesseract
from wand.image import Image as wi
from tika import parser


def extract_text_image(from_file,to_file, lang='deu', image_type='jpeg', resolution=300):
    print("-- Parsing image", from_file, "--")
    print("---------------------------------")
    pdf_file = wi(filename=from_file, resolution=resolution)
    image = pdf_file.convert(image_type)
    tf = open(to_file,"w",encoding="utf-8")
    for img in image.sequence:
        img_page = wi(image=img)
        image = Image.open(io.BytesIO(img_page.make_blob(image_type)))
        text = pytesseract.image_to_string(image, lang=lang)
        for part in text.split("\n"):
            # print("{}".format(part))
            tf.write("{}".format(part))
            tf.write("\n")
    tf.close()

def parse_text(from_file,to_file):
    tf = open(to_file,"w",encoding='utf-8')
    print("-- Parsing text", from_file, "--")
    text_raw = parser.from_file(from_file)
    print("---------------------------------")
    # print(text_raw['content'].strip())
    tf.write(text_raw['content'].strip())
    tf.close()
    print("---------------------------------")

def pdf2txt(from_file,to_file):
    # parse_text(from_file,to_file)
    extract_text_image(from_file, to_file)




if __name__ == '__main__':
    from_file = "D:\\学习资料\\学校课程\\研究生\\项目\\陈厅\\蚂蚁\\SolBugReports\\Beosin\\1BOX_202109071819.pdf"
    to_file = "txt/test3.txt"
    pdf2txt(from_file,to_file)