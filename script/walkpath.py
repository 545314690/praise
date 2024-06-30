
import os
import re

from pypinyin import lazy_pinyin, Style
import Levenshtein
def 获取汉字首字母(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    首字母缩写 = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return 首字母缩写.upper()

def getPinYin(str_data):
    return ' '.join(lazy_pinyin(str_data))

def edit_distance(string_a, string_b):
    return Levenshtein.distance(string_a,string_b)
    """编辑距离"""
    # m = len(string_a)
    # n = len(string_b)
    # dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    # # 从空位置变到string_a每个位置的距离
    # for col in range(m + 1):
    #     dp[0][col] = col
    # # 从空位置变到string_b 每个位置的距离
    # for row in range(n + 1):
    #     dp[row][0] = row
    #
    # # 填表
    # for row in range(1, n+1):
    #     for col in range(1, m+1):
    #         if string_a[col-1] != string_b[row-1]:
    #             dp[row][col] = min(dp[row - 1][col], dp[row - 1][col-1], dp[row][col-1]) + 1
    #         else:
    #             dp[row][col] = dp[row-1][col-1]
    # return (dp[n][m])

if __name__ == '__main__':
    path = '/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/media/'
    banzou_path = '/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/ban/'
    g = os.walk(path)
    r = []  # 解决文件顺序混乱时用的列表

    for path,dir_list,file_list in g:
        for file_name in file_list:
            if file_name.endswith(".mp3") or file_name.endswith(".mkv"):
                # print(file_name)
                # f1 = re.findall(r"\d+\.?\d*", file_name)  # 这一段 是为了解决文件乱序问题
                # f1 = (f1[0], f1[1][:-1])
                # f1 = list(map(int, f1))
                r.append(file_name)
    alllist = sorted(r)
    print(alllist)

    songs = []

    with open("song.txt", "r") as f:  # 打开文件
        lines = f.readlines()  # 读取文件

        song = {"number":0, "name":"", "texts":[],"pinyin":[]}
        for line in lines:
            line = line.strip().replace("\n", "")
            if line != '' and line[0].isdigit() and line[1] != '.':
                if(int(song['number'])>0):
                    songs.append(song)
                number = re.findall(r"\d+?\d*", line)[0]
                firstLetter = 获取汉字首字母(line.replace(number,'').replace(' ',''))[0]
                # data = map.get(int(number))
                # if data is None:
                #     data = []
                song = {"number" : number, "letter": firstLetter, "name": line, "list": [], "texts": [],"pinyin":[],"songTexts":[]}
                # song['texts'].append(line)
            elif line != '':
                song['texts'].append(line)
                # song['pinyin'].append(getPinYin(line))
        songTexts = []
        songPinYin = []

        # print(songs)
    for song in songs:
        for text in song['texts']:
            arr = text.split(' ')
            for s in arr:
                if s:
                    song['songTexts'].append(s)
                    song['pinyin'].append(getPinYin(s))
    song_map = {}
    for s in songs:
        song_map[s['number']] = s


if len(song) > 0:
    songs.append(song)
    # print(song_map)
    songs2 = []

    localLrcPath = '../public/assets/lrc/'
    for file in alllist:
        number = re.findall(r"\d+?\d*", file)[0]
        while number[0]=='0':
            number = number[1:]
        song = song_map.get(number)
        lrcname = file.replace('.mp3', '') + '.lrc'

        lycLines = []
        lycStrLines = []
        # lycStrDoubleLines = []
        lycStrPinYinLines = []
        # lycStrPinYinDoubleLines = []
        songDoubleLines = []
        songPinYinDoubleLines = []

        songPinYinLines = song['pinyin']

        songTexts = song['songTexts']

        if os.path.exists(localLrcPath + lrcname):
            with open(localLrcPath + lrcname, "r") as f:  # 打开文件
                lycLines = f.readlines()  # 读取文件
                for i,lycLine in enumerate(lycLines):
                    string = lycLine.replace('\n','').split(']')[1]
                    lrcPinyin = getPinYin(string)
                    lycStrPinYinLines.append(lrcPinyin)

            for j,songPinYin in enumerate(songPinYinLines):
                try:
                    if j>0:
                        songDoubleLines.append(songTexts[j-1]+ ' ' + songTexts[j])
                        songPinYinDoubleLines.append(songPinYin[j-1]+ ' ' + songPinYin)
                    # if i>1:
                    #     songDoubleLines.append(songTexts[i-2]+ ' ' + songTexts[i-1]  + songTexts[i])
                    #     songPinYinDoubleLines.append(songPinYin[i-2]+ ' '+ songPinYin[i-1]+ ' ' + songPinYin)
                except Exception as e:
                    print(songPinYin)



        if len(lycStrPinYinLines) >0:
            for k,lycStrPinYinLine in enumerate(lycStrPinYinLines):
                distanceMap = {}
                distancePinYinMap = {}
                for m,songPinYinLine in enumerate(songPinYinLines):
                    distanceMap[songTexts[m]] = edit_distance(lycStrPinYinLine,songPinYinLine)
                for n,songPinYinDoubleLine in enumerate(songPinYinDoubleLines):
                    distanceMap[songDoubleLines[n]] = edit_distance(lycStrPinYinLine,songPinYinDoubleLine)
                sort = sorted(distanceMap.items(), key = lambda x:x[1], reverse = False)

                sourceStr = lycLines[k]
                print(sourceStr.replace('\n','') + " --> " + sort.__getitem__(0)[0])
                # print(sort)





        songs2.append(
            {
                "number": number,
                "title": song['name'],
                "letter": song['letter'],
                "texts": song['texts'],
                "lycStrLines": lycStrLines,
                "artist": ' ',
                "src": 'https://bfc.lovezn.online/player/assets/songs/' + file,
                "pic": 'img.png',
                "lrc": 'https://bfc.lovezn.online/player/assets/songs/' + lrcname
            }
        )

        # songs.append({
        #     "song_name": file.replace('.mp3',''),
        #     "artist": "BFC",
        #     "lrc_name": file.replace('.mp3','')
        # })
# print(edit_distance('爱是不嫉妒',"爱是不嫉妒"))
    print(songs2)