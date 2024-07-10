import pandas as pd
import urllib3  
import certifi
import xmltodict



class permalink:

    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path

    def perma_csv(self):

        https = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

        url = self.url

        response = https.request('GET', url)

        sitemap = xmltodict.parse(response.data)

        sitemap_df = pd.DataFrame.from_dict(sitemap['urlset']['url'])

        # Extract only the 'loc' column
        sitemap_loc_df = sitemap_df[['loc']].rename(columns={'loc': 'link'})

        # Save to a CSV file
        sitemap_loc_df.to_csv(self.save_path, index=False)




