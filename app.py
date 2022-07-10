from flask import Flask, render_template, redirect, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/', methods=["GET", "POST", 'DELETE'])
def index():
    results = []
    if request.method == "POST":
        key = request.form['key']

        url = 'https://www.ask.com/web?q='+key
        response = requests.get(url)

        if str(response) == '<Response [200]>':
            html_text = response.text
            soup = BeautifulSoup(html_text, 'lxml')

            div_objet = soup.find_all('div', class_='PartialSearchResults-item')
            for info in div_objet:
                title = info.a.getText()
                Description = info.p.getText()
                link = info.a['href']
                short_link = str(link).split('?')[0]
                result = []
                result.append(title)
                result.append(Description)
                result.append(link)
                result.append(short_link)
                results.append(result)
    return render_template('index.html', results=results, n=len(results))


if __name__ == '__main__':
    app.run()