# -*- coding: utf-8 -*-

import os
from diskcache import Cache

cache = Cache('./cache')

languages = {
    'english': 'English',
    'англійська': 'English',
    'английский': 'English',

    'ukrainian': 'Ukrainian',
    'українська': 'Ukrainian',
    'украинский': 'Ukrainian',
    

    'polish': 'Polish',
    'польська': 'Polish',
    'польский': 'Polish',

    'russian': 'Russian',
    'російська': 'Russian',
    'русский': 'Russian',

    'french': 'French',
    'французька': 'French',
    'французский': 'French',

    'german': 'German',
    'німецька': 'German',
    'немецкий': 'German',

    'vietnamese': 'Vietnamese',
    "в'єтнамська": 'Vietnamese',
    'вьетнамский': 'Vietnamese',

    'hebrew': 'Hebrew',
    'іврит': 'Hebrew',
    'иврит': 'Hebrew',

    'italian': 'Italian',
    'італійська': 'Italian',
    'итальянский': 'Italian',
}
