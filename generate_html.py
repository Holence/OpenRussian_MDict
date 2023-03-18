import json
with open("dict.json", "r", encoding="utf-8") as f:
    data=json.load(f)

import minify_html
from django.conf import settings
import django
from django.template.loader import get_template
settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['./template']
}])
django.setup()

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
css='<link rel="stylesheet" type="text/css" href="style.css" />\n'

noun=data["человек"]
for Dict in noun:
    if Dict["overview"]["type"]=="noun":
        Dict["extra"]["gender"] = convert[Dict["extra"]["gender"]]
    if Dict["overview"]["type"]=="verb":
        Dict["extra"]["aspect"] = convert[Dict["extra"]["aspect"]]
    
    res=css+get_template("base.html").render(Dict)
    res = minify_html.minify(res, minify_js=True)
    with open("data/n.html", "w", encoding="utf-8") as f:
        f.write(res)

verb=data["любить"]
for Dict in verb:
    if Dict["overview"]["type"]=="noun":
        Dict["extra"]["gender"] = convert[Dict["extra"]["gender"]]
    if Dict["overview"]["type"]=="verb":
        Dict["extra"]["aspect"] = convert[Dict["extra"]["aspect"]]
    
    res=css+get_template("base.html").render(Dict)
    res = minify_html.minify(res, minify_js=True)
    with open("data/v.html", "w", encoding="utf-8") as f:
        f.write(res)