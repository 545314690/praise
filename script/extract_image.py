import os
from zipfile import ZipFile
# 解压目录
unzip_path = "unzip"
# 如果解压目录不存在则创建
if not os.path.exists(unzip_path):
    os.mkdir(unzip_path)

image_path = '/Users/lisenmiao/program/IdeaProjects/slidev-test/public/images/'
ppt_path = '/Users/lisenmiao/Desktop/ppt/zm-修改后2022-10-9/'
import re
def extract_image(path):
    if path.endswith('.DS_Store'):
        return
    pages = 1
    try:
        with ZipFile(path) as f:
            for file in f.namelist():
                print(file)
                if file.startswith("ppt/media/"):
                    f.extract(file, path=unzip_path)
                    if file.endswith("jpeg") or file.endswith("png"):
                        name = re.findall(r"\d+\.?\d*", path.replace(ppt_path,''))[0]
                        # image_name = name + '.' + os.path.splittext(path)[-1]
                        image_name = name + '_' + str(pages) + '.' + file.split(".")[1]
                        if image_name[0]=='0':
                            image_name = image_name[1:]
                            if image_name[0]=='0':
                                image_name = image_name[1:]
                        pages = pages+1
                        toname = image_path + '/' + image_name;
                        # print(file, toname)
                        os.rename(unzip_path + '/' + file, toname)
    except:
        print(path)
        # print()
        # os.rename(path , path.split(".")[0] + '.ppt')


# g = os.walk(r"/Users/lisenmiao/Desktop/ppt/pps")
g = os.walk(ppt_path)

for path,dir_list,file_list in g:
    for file_name in file_list:
        if file_name.endswith(".pptx"):
            # print(os.path.join(path, file_name))
            # toname = file_name.split(".")[0]+'.ppt'
            # print(os.path.join(path, toname))
            # os.rename(os.path.join(path, file_name), os.path.join(path, toname))
            extract_image(os.path.join(path, file_name))
# extract_image(os.path.join(ppt_path, '002爱，我愿意.pptx'))
