#!/usr/bin/env python
# *-* coding: utf-8 *-*

__appname__ = "subdl"
__version__ = "0.0.1"
__author__ = "Dhiraj Thakur <dhirajt@github.com>"
__license__ = "GPLv3"

import argparse
import os 
import requests
import sys

from BeautifulSoup import BeautifulSoup as bs


def main():
	parser = argparse.ArgumentParser(
						description='Download movie/tv-series subtitles',
						prog='subdl')
	parser.add_argument('-d','--dir', default='.', nargs='?',
	                    help='folder to search for movies')
	parser.add_argument('-l','--lang', default='eng', type=str, nargs='?',
	                    help='language of the subtitles to download')
	parser.add_argument('-n','--name', default='', type=str, nargs='?',
	                    help='specify movie/tv-series name to search for')
	args = parser.parse_args()
	
	archive, found = find_opensubtitles(name=args.name,language=args.lang)
	








if __name__ == '__main__':
	main()