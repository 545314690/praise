import os
import sys
import xml.etree.ElementTree as ET
from openpyxl import Workbook

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python script.py [folder_path]")
        sys.exit(1)

    # 获取命令行参数中的文件夹路径
    folder_path = sys.argv[1]

    # 初始化Excel工作簿和工作表
    wb = Workbook()
    ws = wb.active
    ws.title = "Annotations"

    # 设置Excel标题
    titles = ["folder", "filename", "path", "object name", "xmin", "ymin", "xmax", "ymax", "width", "height"]
    ws.append(titles)

    # 遍历文件夹中的所有XML文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)

            # 解析XML文件
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 提取所需字段
            folder = root.find('folder').text
            filename = root.find('filename').text
            path = root.find('path').text
            name = root.find('.//object/name').text
            xmin = int(root.find('.//object/bndbox/xmin').text)
            ymin = int(root.find('.//object/bndbox/ymin').text)
            xmax = int(root.find('.//object/bndbox/xmax').text)
            ymax = int(root.find('.//object/bndbox/ymax').text)

            # 计算标注框的宽度和高度
            width = xmax - xmin
            height = ymax - ymin

            # 将提取的数据写入Excel
            ws.append([folder, filename, path, name, xmin, ymin, xmax, ymax, width, height])

    # 保存Excel文件
    wb.save('annotations.xlsx')

if __name__ == "__main__":
    main()