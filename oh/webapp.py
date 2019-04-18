"""Web application to display enhanced transcripts from Amplify"""

from flask import Flask, render_template, jsonify
from .process import process
from .reader import get_transcript_list

application = Flask(__name__)


@application.route('/')
def index():
    transcripts = get_transcript_list()

    return render_template('index.html', transcripts=transcripts)


@application.route('/transcript/<uid>')
def transcript(uid):
    return render_template('transcript.html', uid=uid)


@application.route('/transcripts/<uid>.json')
def enhance(uid):
    """Generate rich annotations for this transcript id"""

    rich = process(uid)

    return jsonify(rich)

