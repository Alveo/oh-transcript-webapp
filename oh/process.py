"""Process an oral history transcript to generate an
    enhanced version for presentation. """

from nltk.tokenize.texttiling import TextTilingTokenizer
import nltk
nltk.download('stopwords')


from sklearn.feature_extraction.text import TfidfVectorizer

import spotlight

from .reader import cached_apply, get_transcript


def segment_transcript(doc):
    """doc is a document object with text lines
    in 'transcript',
    add a list of 'topics' to the document object
    and return it
    """

    tok = TextTilingTokenizer()

    lines = [turn['text'] for turn in doc['lines']]
    text = "\n\n".join(lines)

    doc['topics'] = []
    start = 0
    for topic in tok.tokenize(text):
        length = len(topic.strip().split('\n\n'))
        end = start + length
        doc['topics'].append({'start': start, 'end': end})
        start = end

    return doc


def topic_documents(doc):
    """generate a list of documents as strings
    given a document object"""

    if 'topics' not in doc:
        return []

    documents = []
    for topic in doc['topics']:
        strings = [turn['text'] for turn in doc['lines'][topic['start']:topic['end']]]
        documents.append(" ".join(strings))

    return documents


def tokenizer(doc):
    """Tokenise a document"""

    trans = "".maketrans("()[],.?!-;:\"", "            ")

    words = doc.split()
    return [w.translate(trans) for w in words]


def topic_keywords(doc, n=5):
    """Given a document object with 'topics', add a
    list of keywords to each topic"""

    documents = topic_documents(doc)
    vec = TfidfVectorizer(stop_words='english', tokenizer=tokenizer)
    mat = vec.fit_transform(documents)
    words = vec.get_feature_names()
    for index in range(len(documents)):
        row = mat[index,].toarray().tolist()[0]
        zrow = list(zip(words, row))
        zrow.sort(key=lambda t: -t[1])
        topic = doc['topics'][index]
        topic['keywords'] = [x[0] for x in zrow if x[1] >= 0.2]

    return doc

from sklearn.metrics.pairwise import cosine_similarity


def topic_features(doc, max_features=100):
    """Given a document object with 'topics', add a
    feature vector for each topic"""

    documents = topic_documents(doc)
    vec = TfidfVectorizer(stop_words='english', max_features=max_features)
    mat = vec.fit_transform(documents)
    doc['topic_distances'] = cosine_similarity(mat).tolist()

    for index in range(len(documents)):
        row = mat[index,].toarray().tolist()[0]
        topic = doc['topics'][index]
        topic['features'] = row

    return doc


def topic_entities(doc):
    """Find named entities in the topic using
    dbpedia spotlight"""

    url = 'http://model.dbpedia-spotlight.org/en/annotate'
    only_place_filter = {
            'policy': "whitelist",
            'types': "schema:Place",
            'coreferenceResolution': False
    }
    documents = topic_documents(doc)

    for index in range(len(documents)):
        document = documents[index]
        try:
            entities = dict()
            for e in spotlight.annotate(url, document, confidence=0.5, support=50):
                entities[e['surfaceForm']] = e['URI']

        except spotlight.SpotlightException:
            entities = {}
        doc['topics'][index]['entities'] = list(entities.items())

    return doc


def doprocess(uid):

    doc = cached_apply(uid, get_transcript)
    segment_transcript(doc)
    topic_keywords(doc)
    topic_features(doc)
    topic_entities(doc)

    return doc


def process(uid):

    return cached_apply(uid, doprocess)


if __name__=='__main__':

    result = doprocess('mloh103-tape0001-s001-m')

    for topic in result['topics']:
        print(topic['keywords'])

