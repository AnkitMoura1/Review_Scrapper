import requests
from flask import Flask, request, render_template
from urllib.request import urlopen as u_opn
from bs4 import BeautifulSoup as bs

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def homepage():
    return render_template("index.html")


@app.route("/review", methods=["POST"])
def get_reviews():
    if request.method == "POST":
        try:
            search_string = request.form["search_string"].replace(" ", "_")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            u_client = u_opn(flipkart_url)
            flipkart_page = u_client.read()
            u_client.close()
            flipkart_html = bs(flipkart_page, "html.parser")  # removing unnecessary data from html page(flipkart_page)
            big_boxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            #   Extracting all products info using class , class is same for every product
            del big_boxes[0:3]  # removing 1st 3 big boxes which are not having product
            box = big_boxes[0]  # Each box in big_boxes will contain 1 product info
            product_link = "https://www.flipkart.com" + box.div.div.div.a["href"]
            product_res = requests.get(product_link)
            product_html = bs(product_res.text, "html.parser")
            product_name = product_html.findAll("div", {"class": "aMaAEs"})[0].div.h1.span.text
            price = product_html.findAll("div", {"class": "_30jeq3 _16Jk6d"})[0].text
            rating = product_html.findAll("div", {"class": "_2d4LTz"})[0].text
            comment_box = product_html.findAll("div", {"class": "t-ZTKy"})[0].div.div.text
            comment_box2 = product_html.findAll("div", {"class": "t-ZTKy"})[1].div.div.text
            return render_template("result.html", product_name=product_name, price=price, rating=rating,
                                   comment=comment_box, comment2=comment_box2)
        except:
            return "<h1>Something went wrong :(</h1>"


if __name__ == '__main__':
    app.run(debug=True)
