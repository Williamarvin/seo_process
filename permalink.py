import pandas as pd
import urllib3  
import certifi
import xmltodict

https = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

url = "https://stocktrademarket.com/post-sitemap.xml"

response = https.request('GET', url)

sitemap = xmltodict.parse(response.data)

sitemap_df = pd.DataFrame.from_dict(sitemap['urlset']['url'])

# Extract only the 'loc' column
sitemap_loc_df = sitemap_df[['link']]

# Save to a CSV file
sitemap_loc_df.to_csv('output.csv', index=False)




