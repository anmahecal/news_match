from bs4 import BeautifulSoup
import requests
from news_app.models import Company, News
from news_app import db

def save_news_to_db(news_function):
    from news_app import db
    def wrapper(*args, **kwargs):
        news_dict, company_id = news_function(*args, **kwargs)
        for key, value in news_dict.items():
            print(key, value)
            print('------')
            news_to_add = News(title=value.get('headline'), category=value.get('label'), relevance=key+1, company_id=company_id)
            db.session.add(news_to_add)
        db.session.commit()
    return wrapper

@save_news_to_db
def get_news(company: Company, quantity:int=10):
    '''
    Get scrapped headlines from News Websites

    url         -- website url
    html_title  -- parent html element that contains the headline
    html_class  -- specific class used in headline element
    quantity    -- Number of headlines to be scrapped (default 10)
    '''
    response = requests.get(company.base_url).text
    soup = BeautifulSoup(response, 'lxml')
    markup = soup.find_all(company.html_element, class_=company.element_class)
    label = soup.find_all(company.html_label, class_=company.label_class)
    headlines = markup[:quantity]
    label = label[:quantity]
    headlines = {i: {'headline': headlines[i].a.text, 'label': label[i].a.text} for i in range(quantity)}
    return headlines, company.id
