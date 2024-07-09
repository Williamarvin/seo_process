import requests
from bs4 import BeautifulSoup
import hashlib
import re
import json
import csv
import pandas as pd
import google.generativeai as genai

article_df = pd.read_csv('article_finished.csv')
final_df = pd.read_csv('article_finalised.csv')

# article_df.to_csv("finished.csv", index=False)

# 2. meta title prompt: Write around 40-55 characters. Write an seo optimised meta title for website to optimise seo with keyword .. . and content .. . Create curiousity, include date.
# 3. meta description: Write around 50-150 characters. Write an seo optimised meta description for website to optimise seo with title .. . The keyword is .. . Create curiousity to click on the result. Include focus keyword.. . Include a Call to Action. Make it engaging but don't repeat the same stuff info in the title. Here is the blog post content .. .
# 1. focus_keyword: Can you give me a focused keyword with maximum of 5 words for website and optimise it for seo, for title .. . and content .. .

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
    meta_description = final_df.loc[row, "meta_description"]

    if len(meta_description) < 120 or len(meta_description) > 170:
        print(row)

        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        title = article_df.loc[row, "title"]
        content = article_df.loc[row, "content"]

        focus_keyword = model.generate_content(f"Can you give me a focused keyword with maximum of 5 words for website and optimise it for seo, for title {title}. and content {content}. Just give me the keyword nothing else", safety_settings=safety_settings)
        for candidate in focus_keyword.candidates:
            focus_keyword = [part.text for part in candidate.content.parts]
        
        meta_title = model.generate_content(f"Write meta title and don't exceed 50 characters at all cost. Write an seo optimised meta title for website to optimise seo with keyword {focus_keyword} and article title {title}. and content {content}. Create curiousity, include date. don't exceed 50 characters at all cost" ,safety_settings=safety_settings)
        for candidate in meta_title.candidates:
            meta_title = [part.text for part in candidate.content.parts]
        
        meta_description = model.generate_content(f"Write meta description and don't exceed 20 words at all cost. Write an seo optimised meta description for website to optimise seo with title {title} and meta title of {meta_title}. The keyword is {focus_keyword}. Create curiousity. Make it engaging but don't repeat the same stuff info in the title. Here is the blog post content {content} and don't exceed 20 WORDS at all cost.", safety_settings=safety_settings)
        for candidate in meta_description.candidates:
            meta_description = [part.text for part in candidate.content.parts]


        focus_keyword = ''.join(focus_keyword)
        meta_title = ''.join(meta_title)
        meta_description = ''.join(meta_description)

        # write to csv file
        final_df.loc[row, "focus_keyword"] = focus_keyword
        final_df.loc[row, "meta_title"] = meta_title
        final_df.loc[row, "meta_description"] = meta_description

        # print("focus_keyword: ", focus_keyword)
        # print("meta_title: ", meta_title)
        # print("meta_description: ", meta_description)

        if count % 5 == 0:
            final_df.to_csv('article_checker.csv', index=False)

        count+=1
        skipped+=1

# Remove the 'content' and 'permalink' columns
article_df = article_df.drop(columns=['content', 'permalink'])
article_df.to_csv('article_finalfinal.csv', index=False)