#!/usr/bin/env python3

import os
import sys
import json
from urllib.parse import quote
import requests


TRIGGER = 'szt'
METADATA = {
    "iid": "org.albert.extension.external/v2.0",
    "name": "sztaki",
    "version": "1.0",
    "author": "Kiss György",
    "dependencies": ['python3-requests', 'xdg-utils'],
    "trigger": TRIGGER,
}
BASE_URL = 'http://szotar.sztaki.hu/'
AJAX_SEARCH_URL = BASE_URL + 'ajax/ac.php?url='
FULL_SEARCH_URL = BASE_URL + 'search'


def make_params(params):
    cons = [k + '=' + v for k, v in params.items()]
    return '?' + '&'.join(cons)


def ajax_search_request(word):
    params = {
        'searchWord': quote(word),
        'lang': 'eng',
        'toLang': 'hun',
        'outLanguage': 'hun',
        'labelHandling': 'INLINE_WITH_PROPERTY',
        'searchMode': 'word_prefix',
        'ignoreAccents': '1',
        'resultFormat': 'autocomplete_merged',
        'pageSize': '50',
    }

    response = requests.get(AJAX_SEARCH_URL + quote(make_params(params)))
    return response.json()


def make_full_search_url(word):
    # example URL: http://szotar.sztaki.hu/search?fromlang=hun&tolang=eng&searchWord=asztal&langcode=hu&u=0&langprefix=&searchMode=WORD_PREFIX&viewMode=full&ignoreAccents=0
    params = {
        'searchWord': quote(word),
        'fromlang': 'eng',
        'tolang': 'hun',
        'langcode': 'hu',
        'u': '0',  # I don't know what this is, but included by default
        'searchMode': 'WORD_PREFIX',
        'viewMode': 'full',
        'ignoreAccents': '1',
    }
    return FULL_SEARCH_URL + make_params(params)


def process_results(json_response):
    for result in json_response['contents']['result']:
        try:
            word_type = result['posLabel']['text']
        except KeyError:
            word_type = ''

        yield {
            'found_word': result['content'],
            'result_language': result['translationLangLabel']['text'],
            'word_type': word_type if not word_type.startswith('nincs') else '',
            'translation': result['translationExcerpt'],
        }


def make_items(results):
    items = []
    for i, result in enumerate(results):
        items.append({
            'id': str(i) + '-' + result['found_word'],
            'name': result['found_word'] + ':  ' + result['translation'],
            'description': result['result_language'] + ' ' + result['word_type'],
            'completion': TRIGGER + ' ' + result['found_word'],
            'icon': None,
            'actions': [{
                'name': 'open',
                'command': '/usr/bin/xdg-open',
                'arguments': [make_full_search_url(result['found_word'])],
            }],
        })
    return items


def handle_query(albert_op, word):
    if albert_op == 'METADATA':
        return METADATA

    elif albert_op == "QUERY":
        if not word or len(word) <= 2:
            return {'items': [{'id': 1, 'name': 'Szó keresése: ' + word}]}

        json_response = ajax_search_request(word)
        if 'result' not in json_response['contents']:
            return {'items': [{'id': 1, 'name': 'Nem található: ' + word}]}

        results = process_results(json_response)
        return {'items': make_items(results)}

    elif albert_op in ('INITIALIZE', 'FINALIZE', 'SETUPSESSION', 'TEARDOWNSESSION'):
        return None


def main():
    albert_op = os.environ.get("ALBERT_OP")
    albert_query = os.environ.get("ALBERT_QUERY")
    word = albert_query[4:] if albert_query else None

    res = handle_query(albert_op, word)
    if res is None:
        return 0

    out = json.dumps(res)
    print(out)

    return 0


if __name__ == '__main__':
    sys.exit(main())
