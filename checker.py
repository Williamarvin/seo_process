import requests
from bs4 import BeautifulSoup
import hashlib
import re
import json
import csv
import pandas as pd
import google.generativeai as genai

article_df = pd.read_csv('article_finalised.csv')
content_df = pd.read_csv('meta.csv')

genai.configure(api_key="AIzaSyC-auhr_7A-I8LBsl58X3YzH7y5K7_YAoE")

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# model = genai.GenerativeModel('gemini-1.0-pro-latest')
# response = model.generate_content("The opposite of hot is")

article_len = len(article_df)

count = 0
skipped = 0


for row in range(skipped, article_len):
    meta_description = content_df.loc[row, "meta_description"]

    if len(meta_description) < 120 or len(meta_description) > 170:

        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        title = article_df.loc[row, "title"]
        content = article_df.loc[row, "content"]

        focus_keyword = content_df.loc[row, "focus_keyword"]
        meta_title = content_df.loc[row, "meta_title"]
        
        meta_description = model.generate_content(f"Write meta description and don't exceed 20 words at all cost. Write an seo optimised meta description for website to optimise seo with title {title} and meta title of {meta_title}. The keyword is {focus_keyword}. Create curiousity. Make it engaging but don't repeat the same stuff info in the title. Here is the blog post content {content} and don't exceed 20 WORDS at all cost.", safety_settings=safety_settings)
        for candidate in meta_description.candidates:
            meta_description = [part.text for part in candidate.content.parts]


        focus_keyword = ''.join(focus_keyword)
        meta_title = ''.join(meta_title)
        meta_description = ''.join(meta_description)

        # write to csv file
        content_df.loc[row, "focus_keyword"] = focus_keyword
        content_df.loc[row, "meta_title"] = meta_title
        content_df.loc[row, "meta_description"] = meta_description

        # print("focus_keyword: ", focus_keyword)
        # print("meta_title: ", meta_title)
        # print("meta_description: ", meta_description)

        if count % 5 == 0:
            content_df.to_csv('article_checker_backup.csv', index=False)

        count+=1
        skipped+=1

# Remove the 'content' and 'permalink' columns
content_df = content_df.drop(columns=['content', 'permalink'])
content_df.to_csv('article_checked.csv', index=False)