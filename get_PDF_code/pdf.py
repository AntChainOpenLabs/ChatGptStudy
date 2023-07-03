############
# 获取pdf的数据内容
############
import io
# import sys
import  os
import  time

from PIL import Image
import pytesseract
from wand.image import Image as wi
from tika import parser

# mode的一种： 将pdf转为图片再识别为文字
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

# mode的一种： 直接将pdf转换为文本
def parse_text(from_file,to_file):
    print(to_file)
    tf = open(to_file,"w",encoding='utf-8')
    print("-- Parsing text", from_file, "--")
    text_raw = parser.from_file(from_file)
    print("---------------------------------")
    # print(text_raw['content'].strip())
    tf.write(text_raw['content'].strip())
    tf.close()
    print("---------------------------------")


# 将pdf转为txt文本
# from_file : pdf的路径
# to_file : 转为文本的路径
# mode : 选择如何将pdf转为文本
def pdf2txt(from_file,to_file,mode = "parse_text"):
    # 获取开始时间
    start = time.time()
    if mode == "parse_text" :
        parse_text(from_file,to_file)
    elif mode == "extract_text_image" :
        extract_text_image(from_file, to_file)
    else:
        print("没有选择模式，不能转为pdf为文本")
    # 获取结束时间
    end = time.time()
    # 计算运行时间
    runTime = end - start
    # 输出运行时间
    print(from_file +"转化运行时间：", runTime, "秒")
    print(to_file)
    print("---------------------------------")

# 根据路径读取pdf并根据match_func的内容
# dir_path : pdf的目录路径
# txt_path : 转换为txt的目录位置
# mode : 读取pdf的模式
# match_func : 根据不同函数写的匹配函数
def read_pdf(dir_path, txt_path, match_func, mode= "parse_text" ):
    print("开始读取dir中的pdf文件")
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            # 拼接文件的完整路径
            # print(file_name,dirs)
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                pdf_name = file_name
                to_file = txt_path + "\\" + root.split("\\")[-1] + "_" + pdf_name + ".txt"
                if not os.path.exists(to_file): # 如果不存在该pdf的转换
                    pdf2txt(file_path, to_file,mode)
                with open(to_file,"r",encoding="utf-8") as f:
                    content = f.read()
                    #根据匹配模式截取想要的内容
                    match_func(content, root.split("\\")[-1] + "_" + file_name)

# 进行标题模糊匹配，确定是否是需要的漏洞
def suspected_vulnerability(bug_title):
    bug_title = bug_title.lower().split(" ")
    # Price oracle manipulation
    # TODO 进行进一步完善
    if "price" in bug_title or "oracle" in bug_title or "manipulation" in bug_title  or "AMM" in bug_title:
        return True
    # ID-related violations
    # TODO 进行进一步完善
    if "ID-related" in bug_title or "violations" in bug_title  or "fake" in bug_title or "arbitrary" in bug_title or "arbitrarily" in bug_title or "access" in bug_title:
        return True

    return False


if __name__ == '__main__':
    from_file = "..\\..\\SolBugReports\\blocksec\\1660885789323-2.pdf"
    to_file = r"test3.txt"
    pdf2txt(from_file,to_file)