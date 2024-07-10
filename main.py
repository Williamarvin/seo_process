from permalink import permalink
from content import content
from gptProcess import meta
import os
import pandas as pd

url = "https://stocktrademarket.com/post-sitemap.xml"

# parameters
save_folder = "sess2"
api_key="AIzaSyC-auhr_7A-I8LBsl58X3YzH7y5K7_YAoE"

permalink_csv = os.path.join(save_folder, "permalist.csv")

if __name__ == "__main__":
    # # step 1
    # permaObj = permalink(url, permalink_csv)
    # permaObj.perma_csv()

    # # step 2
    # permalink_csv = permalink_csv
    # content_csv = "content.csv"

    # contentObj = content(permalink_csv, save_folder)
    # contentObj.content_process()

    # step 3
    article_df = os.path.join(save_folder,'content_csv.csv')
    meta_obj = meta(save_folder, article_df, api_key)
    meta_obj.gpt_process()

    print("processed finished")