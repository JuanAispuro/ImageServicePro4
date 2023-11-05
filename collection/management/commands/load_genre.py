import os
import requests
from  datetime import datetime, date, timezone 
import sys
from django.core.management.base import BaseCommand, CommandError
import requests

import json 
from models import Artist, Genre, Artwork, Style, Period
from dotenv import load_dotenv
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        load_dotenv()
        
    
       
                


