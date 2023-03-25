from tqdm import tqdm
import pandas as pd

words=pd.read_csv("russian3/russian3 - words.csv", usecols=["id", "bare", "disabled", "type"])
words["bare"]=words["bare"].apply(lambda x:x.strip())
words=words[~pd.isna(words["type"])]
words=words[words["disabled"]==0]
words.drop(columns=["disabled", "type"], inplace=True)

dtype={"id":"int", "bare":"string"}
words=words.astype(dtype)
words.info()

word_dict=dict(zip(words["id"].values.tolist(), words["bare"].values.tolist()))

words_forms_csv=pd.read_csv("russian3/russian3 - words_forms.csv", usecols=["word_id", "form_bare"])
words_forms_csv=words_forms_csv[~words_forms_csv["form_bare"].isna()]
words_forms_csv["form_bare"]=words_forms_csv["form_bare"].apply(lambda x:x.strip())
words_forms_csv["form_bare"]=words_forms_csv["form_bare"].apply(lambda x:x.strip("()"))
words_forms_csv=words_forms_csv[words_forms_csv["form_bare"]!="-"]
words_forms_csv=words_forms_csv[words_forms_csv["form_bare"]!="—"]
# 因为words中剔除了部分type为NaN和disabled的，这里只链接form原型在words中的部分
words_forms_csv=words_forms_csv[words_forms_csv["word_id"].isin(words["id"].values)]

dtype={"word_id":"int", "form_bare":"string"}
words_forms_csv=words_forms_csv.astype(dtype)
words_forms_csv.info(show_counts=True)

words_forms_iter=zip(words_forms_csv["word_id"].values.tolist(), words_forms_csv["form_bare"].values.tolist())

del words
del words_forms_csv

with open("Mdx_html.txt", "a", encoding="utf-8") as f:
    for word_id, form_bare in tqdm(words_forms_iter):
        f.write("%s\n@@@LINK=%s\n</>\n"%(form_bare, word_dict[word_id]))
