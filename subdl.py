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
    args = parser.parse_args()
	
    find_opensubtitles(name=args.name,
                       lang=args.lang,
                       directory=args.dir)
	




def find_opensubtitles(name,lang,directory):

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
                print '%s. %s\n' % (index+1,item)
            choice = int(raw_input('Choice (number) : '))

        if media_files:
            name = media_files[choice-1].lower()
            replaced_name = name.replace('.',' ').replace('-',' ').split(' ')[:-1]
            search_key = ' '.join(replaced_name)
            to_exclude = re.findall(words_exclude,search_key)
            name = ' '.join([ word for word in replaced_name if word not in to_exclude ])

    #print name

    if not name:
        print ("Error: Couldn't find a name to search for. Try adding a name like \n"
               "subdl --name='the help' \n")
        sys.exit(0)

    base_url = 'http://www.opensubtitles.org'
    search_url = 'http://www.opensubtitles.org/en/search2'

    try:
        pg_response = requests.get(search_url,params={'MovieName':name})
    except ConnectionErrror:
        print "Error: Can't connect to the internet\n"

    soup = BeautifulSoup(pg_response.text)

    result_table = soup.find('table',id='search_results')
    if not result_table:
        print ("Sorry couldn't find any subs. Maybe check the filename or try \n"
               "adding a name like subdl --name='the help'\n")
        sys.exit(0)

    table_rows = result_table.findAll('tr')
    result_rows = [ item for item in table_rows if 'name' in item.get('id','') ]
    #print result_rows

    subs_links = [ base_url+item.findAll('td')[4].a['href'] for item in result_rows 
                   if item.findAll('td')[1].a['href'][-3:] == lang ]
    #print subs_links
    save_subs(subs_links[0],directory)

def save_subs(link,directory):
    pg_response = requests.get(link)
    filename = pg_response.headers.get('content-disposition').split('=')[1].strip('"')  
    filename = os.path.join(directory,filename)

    with open(filename,'w') as zipf:
        zipf.write(pg_response.content)
    print filename  
    with zipfile.ZipFile(filename, "r") as zipf:
        zipf.extractall(path=directory)


if __name__ == '__main__':
    main()