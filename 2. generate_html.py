import os
import json
from tqdm import tqdm
with open("dict.json", "r", encoding="utf-8") as f:
    data=json.loads(f.read())
convert={
    'f': "feminine",
    'm': "masculine",
    'n': "neuter",
    'pl': "plural",
    'b': "both",
    'i': "imperfective",
    'p': "perfective",
    '': "unknown",
}
for word, dlist in data.items():
    for Dict in dlist:
        if Dict["overview"]["type"]=="noun":
            Dict["extra"]["gender"] = convert[Dict["extra"]["gender"]]
        if Dict["overview"]["type"]=="verb":
            Dict["extra"]["aspect"] = convert[Dict["extra"]["aspect"]]


import minify_html
from django.conf import settings
import django
from django.template.loader import get_template
settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['./template']
}])
django.setup()
css='<link rel="stylesheet" type="text/css" href="style.css" />\n'

def generate_html(dlist):
    text=""
    for Dict in dlist:
        text += get_template("base.html").render(Dict)
    text = minify_html.minify(text, minify_js=True)
    text = css+text
    return text


# data={
#     "знать": data["знать"]
# }

# # 一个词一个html
# for word, dlist in data.items():
#     with open("data/%s.html"%word, "w", encoding="utf-8") as f:
#         f.write(generate_html(dlist))

# # MdxBuilder的html
if os.path.exists("Mdx_html.txt"):
    os.remove("Mdx_html.txt")
with open("Mdx_html.txt", "a", encoding="utf-8") as f:
    for word, dlist in tqdm(data.items()):
        f.write(word+"\n"+generate_html(dlist)+"\n</>\n")
