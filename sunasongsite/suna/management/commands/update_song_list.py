from django.core.management.base import BaseCommand

from suna.models import PlayList, Song

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Command(BaseCommand):
    help = 'Update song list - Tgd.kr'
    url = "https://tgd.kr/s/do____ob_"
    tgd_url = "https://tgd.kr"
    pattern = r"(\d{4}/\d{2}/\d{2})"

    def __init__(self, *args, **kwargs):
        self.p = re.compile(self.pattern)
        return super().__init__(*args, **kwargs)

    # def add_arguments(self, parser):
    #     parser.add_argument('--name', type=str)

    def handle(self, *args, **options):
        page_num = 1
        while True:
            articles = self.get_songlist_articles(page_num)
            if len(articles) > 0:
                self.update_song_list(articles)
                page_num += 1
            else:
                break
        print('== page_num:', page_num)

    def get_songlist_articles(self, page_num):
        page_url = f'{self.url}/page/{page_num}'
        response = requests.get(page_url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        articles = soup.select(".article-list-row")
        return articles

    def update_song_list(self, articles):
        for article in articles:
            title_line = article.find(
                    'div',
                    {'class': 'list-title'}).select_one('a')
            title = title_line.get('title')
            detail_url = title_line.get('href')
            if "노래리스트" in title.replace(' ', ''):
                result = self.p.search(title)
                if result:
                    date_str = result.group(1)
                    date_obj = datetime.strptime(
                            date_str, "%Y/%m/%d").date()
                    print(title, detail_url, date_obj)
                    self.get_page_content(detail_url, date_obj)
                else:
                    print('??? date?')
            else:
                print('??? title', title)
            print('---------------')

    def get_page_content(self, detail_url, created_date):
        page_url = f'{self.tgd_url}{detail_url}'
        response = requests.get(page_url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find(
                'div', {'id': 'article-content'})
        play_list, created = PlayList.objects.get_or_create(
                play_date=created_date)
        for t in content.findAll('li'):
            text = t.text
            is_high = False
            if '*' in text:
                is_high = True
                text = text.replace('*', '')
            if '-' in text:
                singer, song_title, *items = text.split('-')
                if items:
                    print('??? 이상한 라인..', text)
                    continue
                singer = singer.strip()
                song_title = song_title.strip()
                song, created = Song.objects.get_or_create(
                        title=song_title,
                        singer=singer)
                song.is_high = is_high
                if created:
                    song.ctime = created_date
                song.save()
                play_list.songs.add(song)
            else:
                print('노래 맞음? (수작업필요)', text)
