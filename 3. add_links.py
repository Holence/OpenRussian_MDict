from tqdm import tqdm
import pandas as pd

words=pd.read_csv("russian3/words.csv", usecols=["id", "bare", "disabled", "type"])
words=words[~pd.isna(words["type"])]
words=words[words["disabled"]==0]
words.drop(columns=["disabled", "type"], inplace=True)
words.info()

words_forms_csv=pd.read_csv("russian3/words_forms.csv", usecols=["word_id", "form"])
words_forms_csv=words_forms_csv[~words_forms_csv["form"].isna()]
words_forms_csv=words_forms_csv[words_forms_csv["form"]!="-"]
words_forms_csv=words_forms_csv[words_forms_csv["form"]!="—"]
words_forms_csv["form"].replace("'", "", regex=True, inplace=True)
words_forms_csv=words_forms_csv[words_forms_csv["word_id"].isin(words["id"].values)]
words_forms_csv=words_forms_csv[~words_forms_csv["form"].isin(words["bare"].values)]
words_forms_csv.info()

print(len(words_forms_csv))
with open("Mdx_html.txt", "a", encoding="utf-8") as f:
    for i,row in tqdm(words_forms_csv.iterrows()):
        word_id=row["word_id"]
        form=row["form"]
        orig_word = words[words["id"]==word_id].iloc[0]["bare"]
        f.write("%s\n@@@LINK=%s\n</>\n"%(form, orig_word))
