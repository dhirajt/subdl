#!/usr/bin/env python
# *-* coding: utf-8 *-*

__appname__ = "subdl"
__version__ = "0.0.1"
__author__ = "Dhiraj Thakur <dhirajt@github.com>"
__license__ = "GPLv3"

import argparse
import logging
import os
import re
import requests
import sys
import zipfile


from BeautifulSoup import BeautifulSoup
from operator import itemgetter
from HTMLParser import HTMLParser 
from requests.exceptions import ConnectionError


media_extensions = ["3g2",  "3gp", "3gp2", "3gpp", "60d", "ajp", "asf", "asx",
                    "avchd", "avi", "bik", "bix", "box", "cam", "dat", "divx",
                    "dmf", "dv", "dvr-ms", "evo", "flc", "fli", "flic", "flv",
                    "flx", "gvi", "gvp", "h264", "m1v", "m2p", "m2ts", "m2v",
                    "m4e", "m4v", "mjp", "mjpeg", "mjpg", "mkv", "moov",
                    "mov", "movhd", "movie", "movx", "mp4", "mpe", "mpeg",
                    "mpg", "mpv", "mpv2", "mxf", "nsv", "nut", "ogg", "ogm",
                    "omf", "ps", "qt", "ram", "rm", "rmvb", "swf", "ts", "vfw",
                    "vid", "video", "viv", "vivo", "vob", "vro", "wm", "wmv",
                    "wmx", "wrap", "wvx", "wx", "x264", "xvid" ]

words_exclude = ('xvid|divx|480p|480i|320p|320i|720p|720i|1080p|1080i|dvdscr|'
                 'ts|pdtv|hdtv|dvdrip|x264|\d+|subs|subtitles')


def main():
    parser = argparse.ArgumentParser(
                        description='Download movie/tv-series subtitles',
                        prog='subdl')
    parser.add_argument('-d','--dir', default='.', nargs='?',
                        help='folder to search for movies')
    parser.add_argument('-l','--lang', default='all', type=unicode, nargs='?',
                        help='language of the subtitles')
    parser.add_argument('-n','--name', default='', type=unicode, nargs='?',
                        help='specify movie/tv-series name')
    parser.add_argument('-c','--choose', action='store_true',
                        help='choose subs from a list')
    args = parser.parse_args()
	
    find_opensubtitles(name=args.name,
                       lang=args.lang,
                       directory=args.dir,
                       choose=args.choose)
	

def find_opensubtitles(name,lang,directory,choose):

    opensubs_lang = {
		"all": "ALL",
		"afr": "Afrikaans",     
		"alb": "Albanian",
		"ara": "Arabic",            
		"arm": "Armenian",      
		"baq": "Basque",
		"ben": "Bengali",
		"bos": "Bosnian",
		"pob": "Portuguese-BR",
		"bre": "Breton",
		"bul": "Bulgarian",
		"bur": "Burmese",            
		"cat": "Catalan",
		"chi": "Chinese",
		"hrv": "Croatian",          
		"cze": "Czech",
		"dan": "Danish",
		"dut": "Dutch",
		"eng": "English",
		"epo": "Esperanto",
		"est": "Estonian",
		"fin": "Finnish",
		"fre": "French",
		"glg": "Galician",
		"geo": "Georgian",
		"ger": "German",
		"ell": "Greek",
		"heb": "Hebrew",
		"hin": "Hindi",
		"hun": "Hungarian",
		"ice": "Icelandic",
		"ind": "Indonesian",
		"ita": "Italian",
		"jpn": "Japanese",
		"kaz": "Kazakh",
		"khm": "Khmer",
		"kor": "Korean",
		"lav": "Latvian",
		"lit": "Lithuanian",
		"ltz": "Luxembourgish",
		"mac": "Macedonian",
		"may": "Malay",
		"mal": "Malayalam",
		"mon": "Mongolian",
		"nor": "Norwegian",
		"oci": "Occitan",
		"per": "Farsi",
		"pol": "Polish",
		"por": "Portuguese",
		"rum": "Romanian",
		"rus": "Russian",
		"scc": "Serbian",
		"sin": "Sinhalese",
		"slo": "Slovak",
		"slv": "Slovenian",
		"spa": "Spanish",
		"swa": "Swahili",
		"swe": "Swedish",            
		"syr": "Syriac",
		"tgl": "Tagalog",
		"tam": "Tamil",         
		"tel": "Telugu",            
		"tha": "Thai",
		"tur": "Turkish",
		"ukr": "Ukrainian",
		"urd": "Urdu",           
		"vie": "Vietnamese",     
	}
    if lang == 'all':
        lang = 'eng'

    if lang not in opensubs_lang:
        print 'Error: language not available on opensubtitles.org'
        sys.exit(0)

    if not name:
        current_dir_items = os.listdir(directory)

        files = [ f for f in current_dir_items if os.path.isfile(os.path.join(directory,f)) ]

        media_files = [ f for f in files if f.split('.')[-1] in media_extensions ]

        choice = 0
        if len(media_files) > 1:
            print 'Found multiple media files. Choose the file to search subs for:\n'
            for index,item in enumerate(media_files):
                print '%s. %s' % (index+1,item)
            while choice not in range(1,len(media_files)+1):
                choice = int(raw_input('Choice (number) : '))-1

        if media_files:
            name = media_files[choice].lower()
            replaced_name = name.replace('.',' ').replace('-',' ').split(' ')[:-1]
            search_key = ' '.join(replaced_name)
            to_exclude = re.findall(words_exclude,search_key)
            name = ' '.join([ word for word in replaced_name if word not in to_exclude ])

    #print name

    if not name:
        print ("Error: Couldn't find a name to search for. Try adding a name like \n"
               "subdl --name='the help' \n")
        sys.exit(0)

    sub_link = find_subs(name=name,lang=lang,choose=choose)
    save_subs(sub_link,directory)
    
def find_subs(name,lang='eng',link=None,choose=False):

    base_url = 'http://www.opensubtitles.org'
    search_url = 'http://www.opensubtitles.org/en/search2'

    if link:
        link = base_url+link
    try:
        if link:
            pg_response = requests.get(link)
        else:
            pg_response = requests.get(base_url,params={'MovieName':name,
                                                        'SubLanguageID':lang})
    except ConnectionError:
        print "\nError: Can't connect to the internet"
        sys.exit(0)

    soup = BeautifulSoup(pg_response.text)

    result_table = soup.find('table',id='search_results')
    if not result_table:
        print ("Sorry couldn't find any subs. Maybe check the filename or try \n"
               "adding a name like subdl --name='the help'\n")
        sys.exit(0)

    table_rows = result_table.findAll('tr')
    result_rows = [ item for item in table_rows if 'name' in item.get('id','') ]
    
    name_rows = []
    for item in result_rows:
        if item.findAll('td')[1].a['href'][-3:] == lang:
            text = item.findAll('td')[0].findAll(text=True)
            if len(text)==4:
                name_rows.append(text[1].replace('\n','').replace('\t',''))
            else:
                name_rows.append(u'')

    #print result_rows
    subs_links = [ [ item.findAll('td')[0].a.string,
                     base_url+item.findAll('td')[4].a['href']
                   ] 
                   for item in result_rows 
                   if item.findAll('td')[1].a['href'][-3:] == lang ]
    choice = 0
    if choose:
        for index,item in enumerate(subs_links):
            print '%s. %10s - %s' % (index+1,
                                item[0].replace('\n','').replace('\t',''),
                                name_rows[index])
        while choice not in range(1,len(subs_links)+1):
            choice = int(raw_input('Choice (number) : '))-1

    return subs_links[choice][1]


def save_subs(link,directory):
    if not link:
        return False
    pg_response = requests.get(link)
    filename = pg_response.headers.get('content-disposition').split('=')[1].strip('"')  
    filename = os.path.join(directory,filename)

    with open(filename,'w') as zipf:
        zipf.write(pg_response.content)

    with zipfile.ZipFile(filename, "r") as zipf:
        zipf.extractall(path=directory)


if __name__ == '__main__':
    main()