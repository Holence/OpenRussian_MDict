# OpenRussian_MDict

Convert [OpenRussian.org](https://en.openrussian.org/) CSVs to mdx

# About OpenRussian.org

> <https://en.openrussian.org/about>
>
> We love the world that Wikipedia has introduced: Free information that will be valid for the next 500 years and for everybody's use. Many companies have created databases of the Russian language, but the data was never shared. Our data is getting better every day and is free for download by everyone so other portals and apps can build on this.
>
> We have a good core database and users have contributed exactly 209,336 enhancements for the data so far.
>
> We want to keep improving the data and constantly add new fields, e.g. which grammatical cases go with which verb. In the end we want to be the best vocabulary portal that we can be, to support learners worldwide looking up words.
>
> <https://en.openrussian.org/contribute>
>
> OpenRussian.org is a community-driven website, where everyone can edit and improve the site's content. All changes get applied immediately but get reviewed later on by an admin team so don't be afraid to break things. We are very happy for everyone that participates!

# Download

You can download pre-build mdict at [Release Page](https://github.com/Holence/OpenRussian_MDict/releases)

# Building

Run `run.cmd` or run each python script step by step:

1. Get CSVs from OpenRussian.org [Database](https://app.togetherdb.com/db/fwoedz5fvtwvq03v/openrussian_public). (get_csv.py)

2. From CSVs to dict.json (generate_dict.py \ generate_dict.ipynb)

3. From dict.json to Mdx_html.txt (generate_html.py)

4. Append other word forms (linking to bare form) using "@@@LINK=" (add_links.py)

Final Step: [MdxBuilder](https://www.pdawiki.com/forum/thread-42526-1-1.html) (v3.0 RC1 Recommended)

![MdxBuilder](pic/MdxBuilder.jpg)

# Screenshots

PC

<img src="pic/Eudic_win10.jpg" alt="Eudic_win10" style="zoom:50%;" />

Android

<img src="pic/Eudic_android.png" alt="Eudic_android" style="zoom:50%;" />

# Licenses

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
