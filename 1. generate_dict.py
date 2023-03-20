# %%
import pandas as pd
from utils import *
import json
import numpy as np
from tqdm import tqdm

def show_na_column(df):
    print("NaN:", [i for i in list(df.isnull().sum().items()) if i[1]])

# %%
words=pd.read_csv(
    "russian3/words.csv",
    usecols=["id", "bare", "accented", "derived_from_word_id", "rank", "disabled", "usage_en", "type"])

# %%
# 有些词竟然还有多余的空格……
print(words["bare"].str.contains(" $").sum())
print(words["bare"].str.contains("^ ").sum())
words["bare"]=words["bare"].apply(lambda x:x.strip())
print(words["bare"].str.contains(" $").sum())
print(words["bare"].str.contains("^ ").sum())

print(words["accented"].str.contains(" $").sum())
print(words["accented"].str.contains("^ ").sum())
words["accented"]=words["accented"].apply(lambda x:x.strip())
print(words["accented"].str.contains(" $").sum())
print(words["accented"].str.contains("^ ").sum())

# %%
words["derived_from_word_id"].fillna(-1, inplace=True)
words["rank"].fillna(-1, inplace=True)
words["usage_en"].fillna("", inplace=True)
words["usage_en"].replace("\\\\n", "\\n", regex=True,inplace=True)
dtype={"id":"int", "bare":"string", "accented":"string", "derived_from_word_id":"int", "rank":"int", "disabled":"int", "usage_en":"string", "type":"string"}
words=words.astype(dtype)
words.info()
show_na_column(words)

# %%
not_nan_list=words[~pd.isna(words["type"])]
print("Total Not NaN:", len(not_nan_list))
print("Total Not NaN (not disabled):", len(not_nan_list[not_nan_list["disabled"]==0]))
print("Total Not NaN (disabled):", len(not_nan_list[not_nan_list["disabled"]==1]))
not_nan_list=not_nan_list[not_nan_list["disabled"]==1]
print("Has Usage (disabled):", len(not_nan_list[not_nan_list["usage_en"].isna()==False]))
del not_nan_list

print()
nan_list=words[pd.isna(words["type"])]
print("Total NaN:", len(nan_list))
print("Total NaN (not disabled):", len(nan_list[nan_list["disabled"]==0]))
print("Total NaN (disabled):", len(nan_list[nan_list["disabled"]==1]))
nan_list=nan_list[nan_list["disabled"]==0]
print("Has Usage (not disabled):", len(nan_list[nan_list["usage_en"].isna()==False]))
del nan_list

# %%
# Disabled的词、type为NaN的词，将没有主页面，但是可以被relate到
selected_words=words[~pd.isna(words["type"])].copy(deep=True)
selected_words=selected_words[selected_words["disabled"]==0]
selected_words.drop(columns=["disabled"], inplace=True)
selected_words.info()
show_na_column(selected_words)

other_words=words[(pd.isna(words["type"])) | (words["disabled"]==1)].copy(deep=True)
other_words.drop(columns=["bare", "derived_from_word_id", "rank", "disabled", "usage_en", "type"], inplace=True)
other_words.info()
show_na_column(other_words)

del words

# %%
words_forms_csv=pd.read_csv("russian3/words_forms.csv", usecols=["word_id","form_type","form"])
words_forms_csv["form"].fillna("", inplace=True)

# 有些词竟然还有多余的空格……
print(words_forms_csv["form"].str.contains(" $").sum())
print(words_forms_csv["form"].str.contains("^ ").sum())
words_forms_csv["form"]=words_forms_csv["form"].apply(lambda x:x.strip())
print(words_forms_csv["form"].str.contains(" $").sum())
print(words_forms_csv["form"].str.contains("^ ").sum())

dtype={"word_id":"int", "form_type":"string", "form":"string"}
words_forms_csv=words_forms_csv.astype(dtype)
words_forms_csv.info(show_counts=True)
show_na_column(words_forms_csv)

# %%
words_rels_csv=pd.read_csv("russian3/words_rels.csv", usecols=["word_id","rel_word_id","relation"])
dtype={"word_id":"int", "rel_word_id":"int", "relation":"string"}
words_rels_csv=words_rels_csv.astype(dtype)
words_rels_csv.info()
show_na_column(words_rels_csv)

# %%
nouns_csv=pd.read_csv("russian3/nouns.csv")
# both->b
nouns_csv["gender"]=nouns_csv["gender"].map({"f":"f", "m":"m", "n":"n", "pl":"pl","both":"b"})
nouns_csv["gender"].fillna("", inplace=True)
nouns_csv["partner"].fillna("", inplace=True)
nouns_csv["animate"].fillna(0, inplace=True)
nouns_csv["indeclinable"].fillna(0, inplace=True)
nouns_csv["sg_only"].fillna(0, inplace=True)
nouns_csv["pl_only"].fillna(0, inplace=True)
dtype={"word_id":"int", "gender":"string", "partner":"string", "animate":"bool", "indeclinable":"bool", "sg_only":"bool", "pl_only":"bool"}
nouns_csv=nouns_csv.astype(dtype)
nouns_csv.info()
show_na_column(nouns_csv)

# %%
verbs_csv=pd.read_csv("russian3/verbs.csv", usecols=["word_id","aspect","partner"])
# imperfective->i, perfective->p, both->b
verbs_csv["aspect"]=verbs_csv["aspect"].map({"imperfective":"i", "perfective":"p", "both":"b"})
verbs_csv["aspect"].fillna("", inplace=True)
verbs_csv["partner"].fillna("", inplace=True)
dtype={"word_id":"int", "aspect":"string", "partner":"string"}
verbs_csv=verbs_csv.astype(dtype)
verbs_csv.info()
show_na_column(verbs_csv)

# %%
expressions_words_csv=pd.read_csv("russian3/expressions_words.csv", usecols=["expression_id", "referenced_word_id"])
dtype={"expression_id":"int", "referenced_word_id":"int"}
expressions_words_csv=expressions_words_csv.astype(dtype)
expressions_words_csv.info()
show_na_column(expressions_words_csv)

# %%
translations_csv=pd.read_csv("russian3/translations.csv")
translations_csv=translations_csv[translations_csv["lang"]=="en"] # 只留英语的翻译
translations_csv.drop(columns=["id", "lang", "position"], inplace=True)
translations_csv["example_ru"].fillna("", inplace=True)
translations_csv["example_tl"].fillna("", inplace=True)
translations_csv["info"].fillna("", inplace=True)
dtype={"word_id":"int", "tl":"string", "example_ru":"string", "example_tl":"string", "info":"string"}
translations_csv=translations_csv.astype(dtype)
translations_csv.info()
show_na_column(translations_csv)

# %%
sentences_csv=pd.read_csv("russian3/sentences.csv", usecols=["id", "ru"])
dtype={"id":"int", "ru":"string"}
sentences_csv=sentences_csv.astype(dtype)
sentences_csv.info()
show_na_column(sentences_csv)

# %%
sentences_words_csv=pd.read_csv("russian3/sentences_words.csv", usecols=["sentence_id", "word_id"])
dtype={"sentence_id":"int", "word_id":"int"}
sentences_words_csv=sentences_words_csv.astype(dtype)
sentences_words_csv.info()
show_na_column(sentences_words_csv)

# %%
sentences_translations_csv=pd.read_csv("russian3/sentences_translations.csv", usecols=["sentence_id", "tl_en"])
sentences_translations_csv=sentences_translations_csv[sentences_translations_csv["tl_en"].isna()==False]
dtype={"sentence_id":"int", "tl_en":"string"}
sentences_translations_csv=sentences_translations_csv.astype(dtype)
sentences_translations_csv.info()
show_na_column(sentences_translations_csv)

# %%
def get_accented(word_id: int):
    accented=""
    if word_id in selected_words["id"].values:
        accented=convertStress(selected_words[selected_words["id"]==word_id].iloc[0]["accented"])
    elif word_id in other_words["id"].values:
        accented=convertStress(other_words[other_words["id"]==word_id].iloc[0]["accented"])
    return accented

def get_extra_info(word_id: int, Type: str):
    info={}
    if Type=="noun":
        if word_id in nouns_csv["word_id"].values:
            row=nouns_csv[nouns_csv["word_id"]==word_id].iloc[0]
            info={
                "gender": row["gender"],
                "partner": convertStress(row["partner"]),
                "indeclinable": row["indeclinable"],
                "animate": row["animate"],
                "sg_only": row["sg_only"],
                "pl_only": row["pl_only"],
            }
    elif Type=="verb":
        if word_id in verbs_csv["word_id"].values:
            row=verbs_csv[verbs_csv["word_id"]==word_id].iloc[0]
            info={
                "aspect": row["aspect"],
                "partner": convertStress(row["partner"]).replace(";", ", ")
            }
    
    return info

def get_translations(word_id: int):
    translation_list=[]
    if word_id in translations_csv["word_id"].values:
        table=translations_csv[translations_csv["word_id"]==word_id]
        for i, row in table.iterrows():
            translation_list.append([
                row["tl"],
                convertStress(row["example_ru"]),
                row["example_tl"],
                row["info"],
            ])
    return translation_list

def get_translation_str(word_id: int):
    translation_list=[]
    if word_id in translations_csv["word_id"].values:
        table=translations_csv[translations_csv["word_id"]==word_id]
        for i, row in table.iterrows():
            translation_list.append(row["tl"])
    return "; ".join(translation_list)

def get_expressions(word_id: int, Type: str):
    # 若查的是单词，则返回expression列表
    if Type!="expression":
        expression_list=[]
        if word_id in expressions_words_csv["referenced_word_id"].values:
            expression_id_list=expressions_words_csv[expressions_words_csv["referenced_word_id"]==word_id]["expression_id"].values.tolist()
            for expression_id in expression_id_list:
                expression_list.append([
                    get_accented(expression_id),
                    get_translation_str(expression_id)
                ])
        return expression_list
    # 若查的是expression，返回单词的列表
    else:
        part_list=[]
        if word_id in expressions_words_csv["expression_id"].values:
            part_id_list=expressions_words_csv[expressions_words_csv["expression_id"]==word_id]["referenced_word_id"].values.tolist()
            for part_id in part_id_list:
                part_list.append([
                    get_accented(part_id),
                    get_translation_str(part_id)
                ])
        return part_list

def get_sentences(word_id: int):
    sentence_list=[]
    if word_id in sentences_words_csv["word_id"].values:
        sentence_id_list=sentences_words_csv[sentences_words_csv["word_id"]==word_id]["sentence_id"].values
        for sentence_id in sentence_id_list:
            if sentence_id in sentences_csv["id"].values and sentence_id in sentences_translations_csv["sentence_id"].values:
                sentence_list.append([
                    convertStress(sentences_csv[sentences_csv["id"]==sentence_id].iloc[0]["ru"]),
                    sentences_translations_csv[sentences_translations_csv["sentence_id"]==sentence_id].iloc[0]["tl_en"],
                ])
            # 取前10个
            if len(sentence_list)==10:
                break
    return sentence_list

def get_forms(word_id: int):
    forms_dict={}
    if word_id in words_forms_csv["word_id"].values:
        table=words_forms_csv[words_forms_csv["word_id"]==word_id]
        forms_list=table["form_type"].unique().tolist()
        for form_type in forms_list:
            form=", ".join(table[table["form_type"]==form_type]["form"])
            # form_bare=", ".join(table[table["form_type"]==form_type]["form_bare"])
            forms_dict[form_type]=convertStress(form)
    return forms_dict

def get_relateds(word_id: int):
    relateds_word={
        "related":[],
        "synonym":[],
        "antonym":[]
    }
    if word_id in words_rels_csv["word_id"].values:
        table=words_rels_csv[words_rels_csv["word_id"]==word_id]
        for i, row in table.iterrows():
            rel_word_id=row["rel_word_id"]
            relation=row["relation"]
            relateds_word[relation].append(rel_word_id)
    if word_id in words_rels_csv["rel_word_id"].values:
        table=words_rels_csv[words_rels_csv["rel_word_id"]==word_id]
        for i, row in table.iterrows():
            rel_word_id=row["word_id"]
            relation=row["relation"]
            if rel_word_id not in relateds_word[relation]:
                relateds_word[relation].append(rel_word_id)
    for k in relateds_word:
        relateds_word[k] = [ [get_accented(v), get_translation_str(v)] for v in relateds_word[k] ]
    return relateds_word


# %%
word_dict={}
print(len(selected_words))
for i,row in tqdm(selected_words.iterrows()):
    word_id=row["id"]
    bare=row["bare"]
    accented = row["accented"]
    derived_from_word_id = row["derived_from_word_id"]
    rank = row["rank"]
    usage_en = row["usage_en"]
    Type=row["type"]
    
    if word_dict.get(bare)==None:
        word_dict[bare]=[]
    
    temp_dict={
        "id": word_id,
        "overview":{
            "type": Type,
            "accented": convertStress(accented),
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

with open("dict.json", "w", encoding="utf-8") as f:
    json.dump(word_dict, f, ensure_ascii=False, cls=CustomJSONizer)


