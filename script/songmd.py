import os
import re

songs = []

with open("song.txt", "r") as f:  # 打开文件
    data = f.readlines()  # 读取文件

    song = []
    for line in data:
        line = line.strip().replace("\n", "")
        if line != '' and line[0].isdigit() and line[1] != '.':
            songs.append(song)
            song = []
            song.append(line)
        else:
            song.append(line)

    if len(song) > 0:
        songs.append(song)
    print(songs)


head='''---
# You can also start simply with 'default'
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: /images/4_1.jpeg
# some information about your slides (markdown enabled)
title: 1爱
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# apply unocss classes to the current slide
class: text-center
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# https://sli.dev/guide/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/guide/syntax#mdc-syntax
mdc: true
'''
template_head_0 = '''
---
# <p v-if="$slidev.nav.clicks ==0">{}</p>
<div v-if="$slidev.nav.clicks ==0">
<pre>
{}
</pre>
</div>
'''

template_head = '''---
title: {}
layout: cover
background: {}
---
# <p v-if="$slidev.nav.clicks ==0">{}</p>
<div v-if="$slidev.nav.clicks ==0">
<pre>
{}
</pre>
</div>
'''
template_body = '''
<div v-click>
<div  v-if="$slidev.nav.clicks =={}">
<pre>
{}
</pre>
</div>
</div>
'''

template_foot = '''
<div v-click>
<div  v-if="$slidev.nav.clicks =={}">
<pre>
{}
</pre>
<div style="text-align:center"><Link to="{}" title="Replay"/></div>
</div>
</div>
'''
# images_path = '/Users/lisenmiao/program/IdeaProjects/slidev-test/public/images/'
images_path = '/Users/lism/Program/WebStormProjects/slidev-praise-v2/public/images/'


slide_file_name = '../slides-new.md'
with open(slide_file_name, 'w') as f:  # 设置文件对象
    f.write(head)  # 将head写入文件中

for (index, song) in enumerate(songs[1:]):
    # song = songs[108]
    # if song[0] == '109耶稣基督说了一句话':
    #     print(1)
    # print(song[0])
    id = re.findall(r"\d+\.?\d*", song[0])[0]
    jpeg = images_path + id + '_1.jpeg'
    jpg = images_path + id + '_1.jpg'
    png = images_path + id + '_1.png'
    image = '/images/202_1.jpeg'
    if os.path.exists(jpg):
        image = '/images/' + jpg.replace(images_path,'')
    elif os.path.exists(jpeg):
        image = '/images/' + jpeg.replace(images_path,'')
    elif os.path.exists(png):
        image = '/images/' + png.replace(images_path,'')
    else:
        print("图不存在:", id)

    title = song[0]
    ps = []
    p = []

    strs = []
    #首页为6，后面为7
    line_count_peer_page = 6
    for line in song[1:]:
        if line == '':
            continue
        p.append(line)
        if len(p) == line_count_peer_page:
            ps.append(p)
            p = []
            line_count_peer_page = 7
    if len(p) >0:
        ps.append(p)
    head = None
    if index==0:
        head = template_head_0
    else:
        head = template_head
    for (i, p) in enumerate(ps):
        str = ''
        if i ==0:
            str = (head.format(title, image, title, '\n'.join(p)))
            # str += '{{$clicks}}'
        elif i< len(ps)-1:
            str = (template_body.format(i, '\n'.join(p)))
        else:
            str = (template_foot.format(i, '\n'.join(p), id))
        if str != '':
            strs.append(str)

    with open(slide_file_name, 'a') as f:  # 设置文件对象
        f.write('\n'.join(strs))  # 将字符串写入文件中
