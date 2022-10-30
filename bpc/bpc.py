import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

def get_bpc_emails():
    name = input('Please enter your name:')
    postcode_entry = input("Postcode to search:")
    if ' ' not in postcode_entry:
        print('Please enter your postcode with a space') 
        postcode_entry = input("Postcode to search:")
    within_n_miles = input("Distance in miles you want to search? 1, 2, 5, 10 or 15?")
    postcode = postcode_entry.split()
    base = 'https://www.bpc.org.uk/information-support/find-a-therapist-or-clinic/page/'
    page_n = map(str, list(range(1, 6)))
    filt = '/?location='+ postcode[0] +'%20' + postcode[1] + '&distance=' + within_n_miles +'&availability&specialism#038;distance=' + within_n_miles +'&availability&specialism'
    urls = []
    for n in page_n:
        urls.append(base + n + filt)

    print('Please wait,', name, '.....\n\n')
    emails = set()  
    for url in urls:
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url
        response = requests.get(url)
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.co.uk",response.text, re.I)) # re.I: (ignore case)
        emails.update(new_emails)
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I)) # re.I: (ignore case)
        emails.update(new_emails)
    email_list = ';\n'.join(emails)
    print('This is a list of bpc emails', within_n_miles, 'miles from postcode', postcode_entry, ':\n\n', email_list)