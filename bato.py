import requests
from bs4 import BeautifulSoup

base_url = f"https://bato.to/series/"
#base_url = f"http://127.0.0.1:1126/?seriesId="

def get_chapters(id):
    """
    Get amount of chapters of a title
    """
    id = str(id)
    r = requests.get(base_url + id)
    soup = BeautifulSoup(r.content, 'html.parser')
    #try:
    print(r.url)
    episode_list = soup.find("div", class_="mt-4 episode-list")
    head_div = episode_list.find("div", class_="head")
    h4_element = head_div.find("h4")

    number = int(h4_element.text.split("(")[-1].split(")")[0])
    return number
    #except Exception as e:
    #    print(e)
    #    return None

def get_metadata(id):
    """
    Gets series metadata (title)
    """
    id = str(id)
    r = requests.get(base_url + id)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        title = soup.find('h3', class_='item-title').text.strip()
        return title
    except:
        return None

links = [
    "https://bato.to/series/",
    "https://wto.to/series/",
    "https://mto.to/series/",
    "https://dto.to/series/",
    "https://hto.to/series/",
    "https://batotoo.com/series/",
    "https://battwo.com/series/",
    "https://batotwo.com/series/",
    "https://comiko.net/series/",
    "https://mangatoto.com/series/",
    "https://mangatoto.net/series/",
    "https://mangatoto.org/series/",
    "https://comiko.org/series/",
    "https://batocomic.com/series/",
    "https://batocomic.net/series/",
    "https://batocomic.org/series/",
    "https://readtoto.com/series/",
    "https://readtoto.net/series/",
    "https://readtoto.org/series/",
    "https://xbato.com/series/",
    "https://xbato.net/series/",
    "https://xbato.org/series/",
    "https://zbato.com/series/",
    "https://zbato.net/series/",
    "https://zbato.org/series/"
]
