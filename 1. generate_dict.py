# %%
import os
import pandas as pd
from utils import *
import json
import numpy as np
from tqdm import tqdm
import random


def show_na_column(df):
    print("NaN:", [i for i in list(df.isnull().sum().items()) if i[1]])


# %%
words = pd.read_csv("russian3/russian3 - words.csv", usecols=["id", "bare", "accented", "derived_from_word_id", "rank", "disabled", "usage_en", "type"])

# %%
# 有些词竟然还有多余的空格……
print("Check Space:")
print(words["bare"].str.contains(" $").sum())
print(words["bare"].str.contains("^ ").sum())

print("After strip()")
words["bare"] = words["bare"].apply(lambda x: x.strip())
print(words["bare"].str.contains(" $").sum())
print(words["bare"].str.contains("^ ").sum())

print("Check Space:")
print(words["accented"].str.contains(" $").sum())
print(words["accented"].str.contains("^ ").sum())

print("After strip()")
words["accented"] = words["accented"].apply(lambda x: x.strip())
print(words["accented"].str.contains(" $").sum())
print(words["accented"].str.contains("^ ").sum())

# %%
words["derived_from_word_id"] = words["derived_from_word_id"].fillna(-1)
words["rank"] = words["rank"].fillna(-1)
words["accented"] = words["accented"].map(convertStress)
words["usage_en"] = words["usage_en"].fillna("")
words["usage_en"] = words["usage_en"].replace("\\\\n", "\\n", regex=True)
dtype = {"id": "int", "bare": "string", "accented": "string", "derived_from_word_id": "int", "rank": "int", "disabled": "int", "usage_en": "string", "type": "string"}
words = words.astype(dtype)
words.info()
show_na_column(words)

# %%
not_nan_list = words[~pd.isna(words["type"])]
print("Total Not NaN:", len(not_nan_list))
print("Total Not NaN (not disabled):", len(not_nan_list[not_nan_list["disabled"] == 0]))
print("Total Not NaN (disabled):", len(not_nan_list[not_nan_list["disabled"] == 1]))
not_nan_list = not_nan_list[not_nan_list["disabled"] == 1]
print("Has Usage (disabled):", len(not_nan_list[not_nan_list["usage_en"].isna() == False]))
del not_nan_list

print()
nan_list = words[pd.isna(words["type"])]
print("Total NaN:", len(nan_list))
print("Total NaN (not disabled):", len(nan_list[nan_list["disabled"] == 0]))
print("Total NaN (disabled):", len(nan_list[nan_list["disabled"] == 1]))
nan_list = nan_list[nan_list["disabled"] == 0]
print("Has Usage (not disabled):", len(nan_list[nan_list["usage_en"].isna() == False]))
del nan_list

# %%
# Disabled的词、type为NaN的词，将没有主页面，但是可以被relate到
selected_words = words[~pd.isna(words["type"])].copy(deep=True)
selected_words = selected_words[selected_words["disabled"] == 0]
selected_words = selected_words.drop(columns=["disabled"])
selected_words.info()
show_na_column(selected_words)
selected_words_dict = selected_words.set_index("id").to_dict("index")
del selected_words

other_words = words[(pd.isna(words["type"])) | (words["disabled"] == 1)].copy(deep=True)
other_words = other_words.drop(columns=["bare", "derived_from_word_id", "rank", "disabled", "usage_en", "type"])
other_words.info()
show_na_column(other_words)
other_words_dict = other_words.set_index("id").to_dict("index")
del other_words

del words

# %%
words_forms_csv = pd.read_csv("russian3/russian3 - words_forms.csv", usecols=["word_id", "form_type", "form"])
words_forms_csv["form"] = words_forms_csv["form"].fillna("")

# 有些词竟然还有多余的空格……
print("Check Space:")
print(words_forms_csv["form"].str.contains(" $").sum())
print(words_forms_csv["form"].str.contains("^ ").sum())

print("After strip()")
words_forms_csv["form"] = words_forms_csv["form"].apply(lambda x: x.strip())
print(words_forms_csv["form"].str.contains(" $").sum())
print(words_forms_csv["form"].str.contains("^ ").sum())

# 有些词竟然还有多余的括号……
print("Check Parentheses:")
print(words_forms_csv["form"].str.contains("\)").sum())
print(words_forms_csv["form"].str.contains("\(").sum())

print("After strip()")
words_forms_csv["form"] = words_forms_csv["form"].apply(
    lambda x: x.strip("()"))
print(words_forms_csv["form"].str.contains("\)").sum())
print(words_forms_csv["form"].str.contains("\(").sum())

words_forms_csv["form"] = words_forms_csv["form"].map(convertStress)
dtype = {"word_id": "int", "form_type": "string", "form": "string"}
words_forms_csv = words_forms_csv.astype(dtype)
words_forms_csv.info(show_counts=True)
show_na_column(words_forms_csv)

print("Builing Word Form Dict...")
words_forms_csv_dict = {}
for i, row in tqdm(words_forms_csv.iterrows(), total=len(words_forms_csv)):
    word_id = row["word_id"]
    if words_forms_csv_dict.get(word_id) == None:
        words_forms_csv_dict[word_id] = {}

    form_type = row["form_type"]
    form = row["form"]
    if words_forms_csv_dict[word_id].get(form_type) == None:
        words_forms_csv_dict[word_id][form_type] = form
    else:
        words_forms_csv_dict[word_id][form_type] += ", "+form

del words_forms_csv

# %%
words_rels_csv = pd.read_csv("russian3/russian3 - words_rels.csv", usecols=["word_id", "rel_word_id", "relation"])
dtype = {"word_id": "int", "rel_word_id": "int", "relation": "string"}
words_rels_csv = words_rels_csv.astype(dtype)
words_rels_csv.info()
show_na_column(words_rels_csv)

print("Builing Word Relation Dict...")
words_rels_csv_dict = {}
for i, row in tqdm(words_rels_csv.iterrows(), total=len(words_rels_csv)):
    word_id = row["word_id"]
    rel_word_id = row["rel_word_id"]
    relation = row["relation"]

    if words_rels_csv_dict.get(word_id) == None:
        words_rels_csv_dict[word_id] = {
            "related": [],
            "synonym": [],
            "antonym": []
        }
    if rel_word_id not in words_rels_csv_dict[word_id][relation]:
        words_rels_csv_dict[word_id][relation].append(rel_word_id)

    if words_rels_csv_dict.get(rel_word_id) == None:
        words_rels_csv_dict[rel_word_id] = {
            "related": [],
            "synonym": [],
            "antonym": []
        }
    if word_id not in words_rels_csv_dict[rel_word_id][relation]:
        words_rels_csv_dict[rel_word_id][relation].append(word_id)

del words_rels_csv

# %%
nouns_csv = pd.read_csv("russian3/russian3 - nouns.csv")
# both->b
nouns_csv["gender"] = nouns_csv["gender"].map({"f": "f", "m": "m", "n": "n", "pl": "pl", "both": "b"})
nouns_csv["gender"] = nouns_csv["gender"].fillna("")
nouns_csv["partner"] = nouns_csv["partner"].fillna("")
nouns_csv["partner"] = nouns_csv["partner"].map(convertStress)
nouns_csv["animate"] = nouns_csv["animate"].fillna(0)
nouns_csv["indeclinable"] = nouns_csv["indeclinable"].fillna(0)
nouns_csv["sg_only"] = nouns_csv["sg_only"].fillna(0)
nouns_csv["pl_only"] = nouns_csv["pl_only"].fillna(0)
dtype = {"word_id": "int", "gender": "string", "partner": "string", "animate": "bool", "indeclinable": "bool", "sg_only": "bool", "pl_only": "bool"}
nouns_csv = nouns_csv.astype(dtype)
nouns_csv.info()
show_na_column(nouns_csv)

nouns_csv_dict = nouns_csv.set_index("word_id").to_dict("index")
del nouns_csv

# %%
verbs_csv = pd.read_csv("russian3/russian3 - verbs.csv", usecols=["word_id", "aspect", "partner"])
# imperfective->i, perfective->p, both->b
verbs_csv["aspect"] = verbs_csv["aspect"].map({"imperfective": "i", "perfective": "p", "both": "b"})
verbs_csv["aspect"] = verbs_csv["aspect"].fillna("")


def func(s):
    return convertStress(s).replace(";", ", ")


verbs_csv["partner"] = verbs_csv["partner"].fillna("")
verbs_csv["partner"] = verbs_csv["partner"].map(func)

dtype = {"word_id": "int", "aspect": "string", "partner": "string"}
verbs_csv = verbs_csv.astype(dtype)
verbs_csv.info()
show_na_column(verbs_csv)

verbs_csv_dict = verbs_csv.set_index("word_id").to_dict("index")
del verbs_csv

# %%
expressions_words_csv = pd.read_csv("russian3/russian3 - expressions_words.csv", usecols=["expression_id", "referenced_word_id"])
dtype = {"expression_id": "int", "referenced_word_id": "int"}
expressions_words_csv = expressions_words_csv.astype(dtype)
expressions_words_csv.info()
show_na_column(expressions_words_csv)

# %%
translations_csv = pd.read_csv("russian3/russian3 - translations.csv")
# 只留英语的翻译
translations_csv = translations_csv[translations_csv["lang"] == "en"]
translations_csv = translations_csv.drop(columns=["id", "lang", "position"])
translations_csv["example_ru"] = translations_csv["example_ru"].fillna("")
translations_csv["example_ru"] = translations_csv["example_ru"].map(convertStress)
translations_csv["example_tl"] = translations_csv["example_tl"].fillna("")
translations_csv["info"] = translations_csv["info"].fillna("")
dtype = {"word_id": "int", "tl": "string", "example_ru": "string", "example_tl": "string", "info": "string"}
translations_csv = translations_csv.astype(dtype)
translations_csv.info()
show_na_column(translations_csv)

print("Builing Word Translation Dict...")
translations_csv_dict = {}
for i, row in tqdm(translations_csv.iterrows(), total=len(translations_csv)):
    word_id = row["word_id"]
    if translations_csv_dict.get(word_id) == None:
        translations_csv_dict[word_id] = []

    translations_csv_dict[word_id].append([
        row["tl"],
        row["example_ru"],
        row["example_tl"],
        row["info"],
    ])

del translations_csv

# %%
sentences_translations_csv = pd.read_csv("russian3/russian3 - sentences_translations.csv", usecols=["sentence_id", "tl_en"])
sentences_translations_csv = sentences_translations_csv[sentences_translations_csv["tl_en"].isna() == False]
dtype = {"sentence_id": "int", "tl_en": "string"}
sentences_translations_csv = sentences_translations_csv.astype(dtype)
sentences_translations_csv.info()
show_na_column(sentences_translations_csv)

sentences_translations_csv_dict = sentences_translations_csv.set_index("sentence_id").to_dict("index")

# %%
sentences_csv = pd.read_csv("russian3/russian3 - sentences.csv", usecols=["id", "ru"])
dtype = {"id": "int", "ru": "string"}
sentences_csv = sentences_csv.astype(dtype)
# 剔除没有翻译的
sentences_csv = sentences_csv[sentences_csv["id"].isin(sentences_translations_csv["sentence_id"])]
sentences_csv["ru"] = sentences_csv["ru"].map(convertStress)
sentences_csv.info()
show_na_column(sentences_csv)

sentences_csv_dict = sentences_csv.set_index("id").to_dict("index")

# %%
sentences_words_csv = pd.read_csv("russian3/russian3 - sentences_words.csv", usecols=["sentence_id", "word_id"])
dtype = {"sentence_id": "int", "word_id": "int"}
sentences_words_csv = sentences_words_csv.astype(dtype)
# 剔除没有翻译的
sentences_words_csv = sentences_words_csv[sentences_words_csv["sentence_id"].isin(sentences_translations_csv["sentence_id"])]
sentences_words_csv.info(show_counts=True)
show_na_column(sentences_words_csv)

print("Builing Word to Sentence Dict...")
word_to_sentence_dict = {}
for i, row in tqdm(sentences_words_csv.iterrows(), total=len(sentences_words_csv)):
    word_id = row["word_id"]
    if word_to_sentence_dict.get(word_id) == None:
        word_to_sentence_dict[word_id] = [row["sentence_id"]]
    else:
        word_to_sentence_dict[word_id].append(row["sentence_id"])

print("Builing Sentence Dict...")
sentences_words_csv_dict = {}
for word_id in tqdm(word_to_sentence_dict):
    sentence_ids = word_to_sentence_dict[word_id]
    # 打乱排序
    random.shuffle(sentence_ids)
    # 取前10个
    sentence_ids = sentence_ids[:10]
    sentences_words_csv_dict[word_id] = []
    for sentence_id in sentence_ids:
        sentences_words_csv_dict[word_id].append([
            sentences_csv_dict[sentence_id]["ru"],
            sentences_translations_csv_dict[sentence_id]["tl_en"],
        ])

del word_to_sentence_dict
del sentences_csv
del sentences_csv_dict
del sentences_words_csv
del sentences_translations_csv
del sentences_translations_csv_dict

# %%


def get_accented(word_id: int):
    accented = ""
    try:
        accented = selected_words_dict[word_id]["accented"]
    except:
        try:
            accented = other_words_dict[word_id]["accented"]
        except:
            pass
    return accented


def get_extra_info(word_id: int, Type: str):
    info = {}
    if Type == "noun":
        try:
            info = nouns_csv_dict[word_id]
        except:
            pass
    elif Type == "verb":
        try:
            info = verbs_csv_dict[word_id]
        except:
            pass
    return info


def get_translations(word_id: int):
    translation_list = []
    try:
        translation_list = translations_csv_dict[word_id]
    except:
        pass
    return translation_list


def get_translation_str(word_id: int):
    translation_list = []
    try:
        translation_list = [i[0] for i in translations_csv_dict[word_id]]
    except:
        pass
    return "; ".join(translation_list)


def get_expressions(word_id: int, Type: str):
    # 若查的是单词，则返回expression列表
    if Type != "expression":
        expression_list = []
        if word_id in expressions_words_csv["referenced_word_id"].values:
            expression_id_list = expressions_words_csv[expressions_words_csv["referenced_word_id"] == word_id]["expression_id"].values.tolist()
            for expression_id in expression_id_list:
                expression_list.append([
                    get_accented(expression_id),
                    get_translation_str(expression_id)
                ])
        return expression_list
    # 若查的是expression，返回单词的列表
    else:
        part_list = []
        if word_id in expressions_words_csv["expression_id"].values:
            part_id_list = expressions_words_csv[expressions_words_csv["expression_id"] == word_id]["referenced_word_id"].values.tolist()
            for part_id in part_id_list:
                part_list.append([
                    get_accented(part_id),
                    get_translation_str(part_id)
                ])
        return part_list


def get_sentences(word_id: int):
    sentence_list = []
    try:
        sentence_list = sentences_words_csv_dict[word_id]
    except:
        pass
    return sentence_list


def get_forms(word_id: int):
    forms_dict = {}
    try:
        forms_dict = words_forms_csv_dict[word_id]
    except:
        pass
    return forms_dict


def get_relateds(word_id: int):
    relateds_word = {
        "related": [],
        "synonym": [],
        "antonym": []
    }
    try:
        relateds_word = words_rels_csv_dict[word_id]
    except:
        pass

    relateds = {}
    for k in relateds_word:
        relateds[k] = [[get_accented(v), get_translation_str(v)]for v in relateds_word[k]]
    return relateds


# %%
word_dict = {}
print(len(selected_words_dict))

for word_id, value in tqdm(selected_words_dict.items()):

    bare = value["bare"]
    accented = value["accented"]
    derived_from_word_id = value["derived_from_word_id"]
    rank = value["rank"]
    usage_en = value["usage_en"]
    Type = value["type"]

    if word_dict.get(bare) == None:
        word_dict[bare] = []

    temp_dict = {
        "id": word_id,
        "overview": {
            "type": Type,
            "accented": accented,
            "derived_from_word": get_accented(derived_from_word_id),
            "rank": rank
        },
        "extra": get_extra_info(word_id, Type),
        "translations": get_translations(word_id),
        "usage": usage_en,
        "expressions": get_expressions(word_id, Type),
        "sentences": get_sentences(word_id),
        "forms": get_forms(word_id),
        "relateds": get_relateds(word_id),
    }

    word_dict[bare].append(temp_dict)

# %%


class CustomJSONizer(json.JSONEncoder):
    def default(self, obj):
        return bool(obj) \
            if isinstance(obj, np.bool_) \
            else super().default(obj)


if not os.path.exists("output"):
    os.makedirs("output")

with open("output/dict.json", "w", encoding="utf-8") as f:
    json.dump(word_dict, f, ensure_ascii=False, cls=CustomJSONizer)
