subdl
=====

a subtitle downloader for your movies and tv-series

How to install
--------------

If have pip installed on your machine. Just do ::

    $ pip install subdl

If you do not have pip installed download this repository
https://github.com/dhirajt/subdl/archive/master.zip and run ::

    $ python setup.py install

after extracting it.

How to use
----------

subdl can download movies by detecting media files in you drive using -d
flag. It'll download the first subtitle availble. ::

    $ subdl -d /media/Hulk    # Hulk is my drive's name!

To choose from a list of subtitles use the choose flag. ::

    $ subdl -cd /media/Hulk  # prompts before downloading subs

To specify a name for a movie or tv episode use name flag. ::

    $ subdl -n 'the help'   # use quotes to specify names.

again this downloads the first subtitle available. To choose from a list
use the -c flag ::

    $ subdl -cn 'the help'  # prompts before downloading subs

To specify language use language flag. ::

    $ subdl -cn 'the help' -l 'eng'  # downloads enlish subtitles

If no language is specified only english subtitles are downloaded. See
below for supported languages.

Subtitle languages
------------------

Use only three characters for specifying language. ::

    {
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

Bugs
----

Use github issue tracker to report bugs.
https://github.com/dhirajt/subdl/issues
