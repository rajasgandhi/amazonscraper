import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import json
from flask import Flask, render_template, request
import os

app=Flask(__name__)

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html', title='Home')

@app.route("/productinfo", methods=['POST'])
def search():
    PRODUCT_URL = request.form['url']
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    response = requests.post(PRODUCT_URL, headers=HEADERS)
    response.raise_for_status()

    #print(response.text)
    soup = bs(response.content, features="lxml")
    title = soup.select("#productTitle")[0].get_text().strip()
    #print(title)

    categories = []
    for li in soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
        categories.append(li.get_text().strip())
    #for x in categories:
        #print (x)

    features = []
    for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
        features.append(li.get_text().strip())
    #for y in features:
        #print(y)

    price = soup.select("#priceblock_saleprice")[0].get_text()
    #print(price)

    review_count = int(soup.select("#acrCustomerReviewText")[0].get_text().split()[0])
    #print(review_count)

    availability = soup.select("#availability")[0].get_text().strip()
    #availabilty

    jsonObject = {'title': title,
                  'categories': categories,
                  'features': features,
                  'price': price,
                  'review_count': review_count,
                  'availability': availability}
    return render_template('products.html', title='Product Info', productinfo=json.dumps(jsonObject, indent=2))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
