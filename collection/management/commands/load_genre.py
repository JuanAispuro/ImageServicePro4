import os
import requests
from  datetime import datetime, date, timezone 
import sys
from django.core.management.base import BaseCommand, CommandError
import requests

import json 
# from models import Artist, Genre, Artwork, Style, Period
from dotenv import load_dotenv
import os

import requests
import time
from bs4 import BeautifulSoup
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        folder_name = "csv_data"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        
        artists = [
        'banksy',
        'edward-hopper',
        'tamara-de-lempicka',
        'vincent-van-gogh',
        'salvador-dali',
        'miss-tic',
        'pablo-picasso',
        'jose-clemente-orozco',
        'rufino-tamayo',
        'jose-guadalupe-posada',
        'agim-sulaj',
        'abraham-mignon',
        'giotto',
        'claude-monet',
        'zdzislaw-beksinski',
        'henri-matisse',
        'rene-magritte',
        'paul-cezanne',
        'edward-hopper',
        'wassily-kandinsky',
        'pierre-auguste-renoir',
        'jean-michel-basquiat',
        'paul-gauguin',
        'gustave-dore',
        'leonardo-da-vinci',
        'rembrandt',
        'gustav-klimt',
        'm-c-escher',
        'egon-schiele',
        'paul-klee',
        'edgar-degas',
        'frida-kahlo',
        'andy-warhol',
        'albrecht-durer',
        'andy-warhol',
        'marc-chagall',
        'piet-mondrian',
        'joan-miro',
        'norman-rockwell',
        'gustave-courbet',
        'caravaggio',
        'michelangelo',
        'camille-pissarro',
        'jackson-pollock',
        'kazimir-malevich',
        'joaqu-n-sorolla',
        'ivan-aivazovsky',
        'alphonse-mucha',
        'ilya-repin',
        'diego-rivera',
        'oswaldo-guayasamin',
        'raphael',
        'seen',
        'katsushika-hokusai',
        'berthe-morisot',
        'fernando-botero',
        'johannes-vermeer',
        'keith-haring',
        'roy-lichtenstein',
        'sandro-botticelli',
        'pierre-bonnard',
        'william-blake',
        'zinaida-serebriakova',
        'andre-derain',
        'el-greco',
        'jean-francois-millet',
        'cy-twombly',
        'aubrey-beardsley',
        'victor-vasarely',
        'james-tissot',
        'david-alfaro-siqueiros',
        'friedensreich-hundertwasser',
        'tintoretto',
        'yayoi-kusama',
        'emil-nolde',
        'arnold-bocklin',
        'edouard-vuillard',
        'frantisek-kupka',
        'konstantin-makovsky',
        'anthony-van-dyck',
        'robert-delaunay',
        'giacomo-balla',
        'umberto-boccioni',
        'oskar-kokoschka',
        'donatello',
        'takashi-murakami',
        'blek-le-rat',
        'dan-witz',
        'carl-larsson',
        'bridget-riley',
        'auguste-rodin',
        'francisco-toledo',
        'el-lissitzky',
        'utagawa-kuniyoshi',
        'paula-rego',
        'henri-martin',
        'alberto-giacometti',
        'frederic-leighton',
        'frank-stella',
        'jenny-saville',
        'seraphine-louis',
        'martiros-sarian',
        'felicien-rops',
        'alberto-pereira']
        for artist in artists:
            if not os.path.exists(os.path.join(folder_name, f'{artist}.csv')):

                r = requests.get(f'https://www.wikiart.org/en/{artist}/')

                html_doc = r.text
                soup = BeautifulSoup(html_doc, 'html.parser')

                name = soup.article.h3.string.strip()
                birth_date = soup.article.find("span", attrs={"itemprop": "birthDate"}).string

                with open(os.path.join(folder_name, f'{artist}.csv'), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow((artist, name, birth_date))

                artwork_links = [link.get('href') for link in
                                soup.find("section", "wiki-layout-artworks-famous").find_all("a", attrs={"class": "artwork-name"})]
                artworks = []

                for aw in artwork_links:
                    time.sleep(.4)
                    awr = requests.get(f'https://www.wikiart.org{aw}')
                    html_doc = awr.text
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    title = soup.article.h3.string
                    if title is None:
                        title = artist + " " + aw
                    date_label = soup.article.find("span", attrs={"itemprop": "dateCreated"})
                    date = None if date_label is None else date_label.string
                    genre_label = soup.article.find("span", attrs={"itemprop": "genre"})
                    genre = None if genre_label is None else genre_label.string
                    image_url = \
                    soup.find_all("div", attrs={"class": "wiki-layout-artist-image-wrapper"}, limit=1)[0].find_all("img", limit=1)[0]
                    more_data = soup.article.find_all("a")
                    style = more_data[1].string
                    period = more_data[2].string
                    print(aw, title, date, style, period, genre, image_url.attrs['src'])
                    artworks.append((artist, aw, title, date, style, period, genre, image_url.attrs['src']))

                with open(os.path.join(folder_name, f'{artist}-art.csv'), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(artworks)

            
        
        
                


