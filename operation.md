# Operation

General:
读音: accented
Form of xxx: derived_from_word_id
Rank: rank
Type: type

Translation:
translations.csv中查word_id，多个tl,example_ru,example_tl,info

Usage info:
usage_en

Expression:
到expressions_words.csv中的referenced_word_id中查，若有则记录下expression_id（word_id），到words.csv中对应的word_id的expression提取出来，再到translations.csv中找word_id对应的翻译

Examples:
到sentences_words.csv中的word_id中查，若有则记录下sentence_id，到sentences.csv中对应的id将sentence提取出来，再到sentences_translations.csv中找sentence_id对应的翻译

Related words:
到words_reals.csv中word_id与rel_word_id中互查并去重，找出对应关系，再到translations.csv中找word_id对应的翻译

## Noun

General:
在nouns.csv中找gender,partner,animate,indeclinable,sg_only,pl_only

Declension:
words_forms.csv

## Verb

General:
在verbs.csv中找aspect,partner

Conjugation:
words_forms.csv

- 若为imperfective，Future处为：

  буду + 原型
  будешь + 原型
  будет + 原型
  будем + 原型
  будете + 原型
  будут + 原型

- 若为perfective，Present处为空

Participles:
words_forms.csv

|                 |        |                                |
| --------------- | ------ | ------------------------------ |
| Active present  | ...... | someone who is doing           |
| Active past     | ...... | someone who was doing          |
| Passive present | ...... | something which is being done  |
| Passive past    | ...... | something which was being done |
| Gerund present  | ...... | while doing (present)          |
| Gerund past     | ...... | while doing (past)             |

## Adjective

Declension:
words_forms.csv

Comparatives:
words_forms.csv

若为空：
comparative
superlative / -ая / -ее / -ие

Short forms:
words_forms.csv

## Adverb

无

## Other

无

## Expression

Expression parts:
到expressions_words.csv中的中查referenced_word_id，列出对应的词与翻译
