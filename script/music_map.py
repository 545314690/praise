import os

ppt_path1 = '/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/media'
# ppt_path = '/Users/lism/Downloads/音频'
import re


map = {}
def gen_map(dir):
    g = os.walk(dir)
    for path,dir_list,file_list in g:
        for file_name in file_list:
            if file_name.endswith(".mp3") or file_name.endswith(".mkv"):
                name = re.findall(r"\d+?\d*", file_name)[0]
                while name[0]=='0':
                    name = name[1:]
                music = ('/praise/assets/media/'+file_name)
                music = (file_name)
                # print(name)
                key = int(name)
                if map.get(key) is None:
                    map[key] = []
                map.get(key).append(music)
gen_map(ppt_path1)
# gen_map(ppt_path)

print(map)

no_music = []
have_music = []

for i in range(1, 315):
    if map.get(i) is None:
        no_music.append(i)
    else:
        have_music.append({
            "number": i,
            "data": map.get(i)
        })
print('有音乐的',315-len(no_music),'首')
print('没有音乐的：',len(no_music),'首')
print('没有音乐的是：',no_music)
import operator
aa = [(k,map[k]) for k in sorted(map.keys())]
print(aa)
print(have_music)

from pypinyin import lazy_pinyin, Style

def 获取汉字首字母(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    首字母缩写 = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return 首字母缩写.upper()
    #return 首字母缩写[:-4].upper()  # 不要倒数后四位,去掉有限公司

songs = []

with open("song.txt", "r") as f:  # 打开文件
    data = f.readlines()  # 读取文件

    song = {"number":0, "name":"", "texts":[]}
    for line in data:
        line = line.strip().replace("\n", "")
        if line != '' and line[0].isdigit() and line[1] != '.':
            if(int(song['number'])>0):
                songs.append(song)
            number = re.findall(r"\d+?\d*", line)[0]
            firstLetter = 获取汉字首字母(line.replace(number,'').replace(' ',''))[0]
            data = map.get(int(number))
            if data is None:
                data = []
            song = {"number" : number, "letter": firstLetter, "name": line, "list": data, "texts": []}
            # song['texts'].append(line)
        elif line != '':
            song['texts'].append(line)

    if len(song) > 0:
        songs.append(song)
    print(songs)
# print(sorted(map.items(), key=operator.itemgetter(0)))
    # print(os.path.join(path, file_name))
            # toname = file_name.split(".")[0]+'.ppt'
            # print(os.path.join(path, toname))
            # os.rename(os.path.join(path, file_name), os.path.join(path, toname))
# extract_image(os.path.join(ppt_path, '002爱，我愿意.pptx'))
