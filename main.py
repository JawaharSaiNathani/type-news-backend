from flask import Flask
import requests
from bs4 import BeautifulSoup as bs
from flask import jsonify

app = Flask(__name__)

def get_news():
    res = requests.get("https://economictimes.indiatimes.com/")
    soup = bs(res.text,"html.parser")
    news = []
    for x in soup.select(".topStories")[0].select("li"):
        if len(x.select("h4")) == 0:
            if x.select("a")[0]['href'].split('/')[1] == "news" or x.select("a")[0]['href'].split('/')[1] == "markets" or x.select("a")[0]['href'].split('/')[1] == "tech":
                res1 = requests.get("https://economictimes.indiatimes.com"+x.select("a")[0]['href'])
                soup1 = bs(res1.text,"html.parser")
                try:
                    news_article = {'heading':soup1.select(".article_wrap")[0].select(".topPart")[0].select("h1")[0].text.strip(),'paras':[]}
                    temp3 = soup1.select(".article_wrap")[0].select(".pageContent")[0].select(".artData")[0].select(".artText")[0]
                    for div in temp3.find_all("div"): 
                        div.decompose()
                    temp3 = temp3.text.strip()
                    temp3 = temp3.split("\n\n")
                    for x in temp3:
                        if len(x) > 3:
                            news_article['paras'].append(x.replace('\n',''))
                            news.append(news_article)
                except:
                    i = 1
    return jsonify({"news": [news]})

@app.route('/')
def news():
    return get_news()

if __name__ == "__main__":
        app.run()