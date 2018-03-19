# Amplify Amplifier

Web application to present transcripts from Amplify (State Library of NSW) with added 
value from various NLP processes.  

## Amplify API

https://amplify.sl.nsw.gov.au/transcripts.json

Get a list of transcripts that are available 

    {"entries": [list of transcripts]
     "current_page": 1,
     "per_page": 500,
     "total_entries": 241
     }

Each entry looks like:

    {
        "uid": "mloh103-tape0001-s001-m",
        "title": "Under the Rainbow [Tape 1 Side A] Interview with Jenny Del.",
        "description": "<p>Collected by the Richmond-Tweed Oral History Group. Recorded in Lismore on 13 November, 1992.</p>\r\n<p>Interview summary: Joining Nimbin and the quality of life. Her reasons for joining Nimbin, and its aims. The closeness of community life. Some of the effects on parenting. Everyone took drugs but initially very few drank alcohol. Account of a police raid. Discusses the use of heroin. How residents have grown. Discusses the roles of men and women.</p>",
        "image_url": "https://slnsw-amplify.s3.amazonaws.com/collections_v2/rainbow_archives/images/01_c09666_0011.jpg",
        "collection_id": 1,
        "collection_title": "Rainbow Archives",
        "duration": 1883,
        "lines_edited": 141,
        "percent_completed": 100,
        "percent_edited": 33,
        "percent_reviewing": 0,
        "users_contributed": 17,
        "audio_urls": [],
        "path": "/transcripts/mloh103-tape0001-s001-m"
    }
    
We can then get the actual transcript at:

https://amplify.sl.nsw.gov.au/transcripts/mloh103-tape0001-s001-m.json

or {{baseurl}}{{path}}.json

    {
    "id": "mloh103-tape0001-s001-m",
    "url": "https://amplify.sl.nsw.gov.au/transcripts/mloh103-tape0001-s001-m",
    "origin_url": "http://archival.sl.nsw.gov.au/Details/archive/110317356",
    "last_updated": "2017-09-01T03:49:04.969Z",
    "title": "Under the Rainbow [Tape 1 Side A] Interview with Jenny Del.",
    "description": "<p>Collected by the Richmond-Tweed Oral History Group. Recorded in Lismore on 13 November, 1992.</p>\r\n<p>Interview summary: Joining Nimbin and the quality of life. Her reasons for joining Nimbin, and its aims. The closeness of community life. Some of the effects on parenting. Everyone took drugs but initially very few drank alcohol. Account of a police raid. Discusses the use of heroin. How residents have grown. Discusses the roles of men and women.</p>",
    "audio_url": "https://slnsw-amplify.s3.amazonaws.com/collections_v2/rainbow_archives/audio/mloh103-tape0001-s001-m.mp3",
    "image_url": "https://slnsw-amplify.s3.amazonaws.com/collections_v2/rainbow_archives/images/01_c09666_0011.jpg",
    "duration": 1883,
    "lines": [{
              "id": 17780,
              "sequence": 0,
              "start_time": 7200,
              "end_time": 17510,
              "original_text": "I've never seen it before.\n",
              "best_text": "I've never seen it before. Okay tape I.D., it is Friday 13th of November, 1992. We're in Lismore",
              "transcript_line_status_id": 4,
              "speaker_id": -1
              },
              ...],
    "speakers": [],
    "statuses": []
    }

The text version (that my code understands) is at:

https://amplify.sl.nsw.gov.au/transcript_files/mloh103-tape0001-s001-m.text?timestamps=1&speakers=1

or {{baseurl}}{{path}}.text?timestamps=1&speakers=1



## Analysis Module

This module takes the transcript and applies topic segmentation, keyword extraction 
and NER to get an enriched version.  Output is a new JSON structure:

    # we represent documents like this
    example = {
        'document': 'transcripts/mloh103-tape0037-s001-m.text',
        'transcript': [
            {
                'speaker': 'Harry Vasiere', 
                'timestamp': '00:05:09.000', 
                'text': 'picked it up say you put it in the hole and then i read it down.'
            },
            {
                'speaker': 'Richard Raxworthy', 
                'timestamp': '00:05:19.000', 
                'text': 'Do you remember anything or any of the amusing incidents in the workshops while you'
            },
            {
                'speaker': 'Harry Vasiere', 
                'timestamp': '00:05:22.000', 
                'text': "were there. You know there's those days you never read"
            }
        ],
        'topics': [
            {
                'start': 0,
                'end': 13,
                'keywords': ['dalhousie', 'norman', 'met', 'shop', 'westerners'],
                'entities': [
                    {'...returned value from dbpedia...'}
                ]
            }
        ]
    }


## My web application 

Javascript front end requests JSON from backend and from Amplify directly 

/transcripts/ 

An index of the transcripts available, reproduced from the Amplify json feed.

/transcripts/{{id}}.json

Where {{id}} is a transcript uid like "mloh103-tape0001-s001-m", returns the 
analysed JSON for this transcript 

/transcripts/{{id}}

HTML page that displays the enhanced transcript for this recording. 


