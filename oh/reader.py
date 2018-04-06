from __future__ import print_function
import re
import os
import requests
import json

AMPLIFY_TEXT_URL = "https://amplify.sl.nsw.gov.au/transcript_files/%s.text?timestamps=1&speakers=1"
AMPLIFY_TRANSCRIPT_URL = "https://amplify.sl.nsw.gov.au/transcripts/%s.json"
CACHE_DIR = 'cache'
if os.getenv('AMPLIFY_CACHE'):
    CACHE_DIR = os.getenv('AMPLIFY_CACHE')

print("CACHE_DIR", CACHE_DIR)

def parseline(line):
    """Parse one line of a transcript

00:00:14.000 <Richard Raxworthy> a catcher didn't you Mr. Vasiere?

    return the timestamp, speaker and text
    """

    pattern = "(\d\d:\d\d:\d\d\.\d\d\d)( <([^>]+)>)? (.*)"

    match = re.match(pattern, line)
    if match:
        m = match.groups()
        return (m[0], m[2], m[3])
    else:
        return '', '', ''


def cached_json(url):
    """Get a url from the cache or
    request"""

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    filename = os.path.join(CACHE_DIR, url.replace('/','_').replace(':','.'))
    if os.path.exists(filename):
        with open(filename) as input:
            result = json.load(input)
    else:
        r = requests.get(url, verify=False)
        result = r.json()
        with open(filename, 'w') as out:
            json.dump(result, out)
    return result


def cached_apply(uid, fn):
    """Get a transcript from the cache or
    generate a new one"""

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    filename = os.path.join(CACHE_DIR, fn.__name__ + "-" + uid + ".json")
    if os.path.exists(filename):
        with open(filename) as input:
            result = json.load(input)
    else:
        result = fn(uid)
        with open(filename, 'w') as out:
            json.dump(result, out)
    return result


def get_transcript(uid):
    """Get the JSON transcript for the given document UID"""

    url = AMPLIFY_TRANSCRIPT_URL % uid
    r = requests.get(url, verify=False)
    return r.json()


def read_transcript(uid):
    """Read a transcript from the given document UID
    Return a list of strings representing speaker turns"""

    url = AMPLIFY_TEXT_URL % uid
    doc = {
        'uid': uid,
        'url': url,
        'transcript': []
    }
    meta = dict()
    r = requests.get(url, verify=False)
    inheader = True
    for line in r.text.split('\n'):
        if inheader:
            if line is "":
                inheader = False
            elif not line.startswith('This') and not line.startswith('Read'):
                field, value = line.split(':', maxsplit=1)
                meta[field.lower()] = value.strip()
        elif line is not '':
            timestamp, speaker, text = parseline(line)
            doc['transcript'].append({'timestamp': timestamp, 'speaker': speaker, 'text': text})

    meta['uid'] = uid

    doc['meta'] = meta
    return doc


def get_transcript_list():
    """Retrieve a list of available transcripts from
    the Amplify site, return a list of dictionaries"""

    url = "https://amplify.sl.nsw.gov.au/transcripts.json"

    result = cached_json(url)

    if 'entries' in result:
        return result['entries']
    else:
        return []


if __name__=='__main__':

    doc = get_transcript_list()

    import json
    print(json.dumps(doc, indent=True))