from oh.process import process
from oh.reader import get_transcript_list

for trans in get_transcript_list():
    if trans['percent_completed'] == 100:
        print(trans['uid'], trans['title'])
        process(trans['uid'])
    else:
        print("Ignoring: ", trans['uid'], trans['percent_completed'])