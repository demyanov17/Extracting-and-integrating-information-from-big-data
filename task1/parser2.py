import re
import json
import requests
from bs4 import BeautifulSoup

HTMLFile = open("source3.html", "r")

# Reading the file 
index = HTMLFile.read()


soup = BeautifulSoup(index, 'lxml')

name = soup.find("meta", property="og:title")["content"]#.find('content')
#print(name)

name = str(name)
# print(name)

#print(index)

# data = re.search(r"window.__INITIAL_STATE__ =(.*);", index).group(1)
#data = json.loads(data)

# pretty print the data:
#data = data.split(".parse('")[-1][:-2]

#data.replace()
#data = json.loads(data)
#print(data)
# # pretty print the data:
#print(json.dumps(data, indent=4))
#data = data.replace("\\", "")
#print(data[165030:])
#["elementInfo"][id, name]

#['elementInfo', 'badges', 'status', 'article', 'allProductsLink', 'prices', 'sectionsTree', 'gallery', 'galleryThumbs', 'linkedProducts', 'hasLeasing', 'creditText',
#'tradeIn', 'yaPay', 'deliveries', 'banners', 'preOrderInfo', 'trailer', 'security', 'advantages', 'withoutPrice', 'yaPayBadge', 'yaPayBadgeCashback', 'tabs', 'productType',
#'discountProduct', 'hasAccessoriesOrServices', 'analytics', 'breadcrumbs', 'csrf', 'seo', 'yandexId']

#["elementInfo"][id, name]
#sectionsTree {'special': {'price': 499990, 'currency': 'RUB'}
print(soup.find_all("li")[50:])




#print(json.loads(data)["tabs"]["list"])
#print((json.loads(data)["tabs"]["content"][0])["introSpecs"])

#important! print((json.loads(data)["tabs"]["content"][0])["introSpecs"])



#print(type(json.loads(data)))
#print(soup.select_one("script", type="application/javascript").contents)
#popmechanic-desktop