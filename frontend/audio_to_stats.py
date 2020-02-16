import os
import json
import string
import threading
from fuzzywuzzy import fuzz
from deep_disfluency.tagger.deep_tagger import DeepDisfluencyTagger
from lcs import lcs
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


disf = DeepDisfluencyTagger(
    config_file="C://Users//alexb//Documents//Treehack//frontend//configs//experiment_configs.csv",
    config_number=21,
    saved_model_dir="C://Users//alexb//Documents//Treehack//frontend//configs//epoch_40"
)

hesitation_tag = '%HESITATION'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


COMMON_FILE_NAME = "speech.wav"

"""
API endpoints to access NLP processing methods for news articles.
"""


def compute_stats(target_sentence, results):
    transcript = str(results['results'][0]['alternatives'][0]['transcript']).lower()
    print("Target: " + target_sentence)
    print("Transcript: " + transcript)

    words_to_confidence = dict()
    confs_list = []
    for w in target_sentence.split():
        if w in transcript:
            for i in results['results'][0]['alternatives'][0]['word_confidence']:
                if i[0] == w:
                    words_to_confidence[w] = i[1]
                confs_list.append(i[1])

    # Tags transcript for disfluencies
    for w in transcript.split():
        disf.tag_new_word(w)

    # for w, t in zip(transcript.split(), disf.output_tags):
    #     print(w + " : " + t)
    
    result = dict()
    words_analysis = []

    transcript = transcript.split()
    target_sentence = target_sentence.split()

    _, triplets = lcs(transcript, target_sentence)
    trans_pointer = 0

    prev_spoken_words = []

    for a, b, is_match in triplets:
        # assume a and b are lists of strings, could be empty
        """
        {
            is_match
            true_words
            spoken_words
            conf (if matched)
            type of spoken error
        }
        """
        data = {
            "is_match": is_match,
            "true_words": b,
            "spoken_words": a
        }


        if isinstance(a, list):
           for i in range(len(a)):
               a[i] = a[i].replace(hesitation_tag, '%')
        else:
            a = a.replace(hesitation_tag, '%')        

        hist_ratio = fuzz.ratio(' '.join(prev_spoken_words), a)
        print("{} / {} = {}".format(prev_spoken_words, a, hist_ratio))
        ratio = fuzz.ratio(' '.join(a), ' '.join(b))

        if hist_ratio > 50 or (isinstance(a, list) and len(set(a)) != len(a)):
            type = 'stutter'
        elif 50 < ratio < 100 or ('<f/>' not in disf.output_tags and '<e/>' not in disf.output_tags):
            type = 'dyspraxia'
        elif '%' in a:
            type = 'filler'
        else:
            type = 'none'

        if is_match:
            data["conf"] = confs_list[trans_pointer]

        if len(b) == 0:
            data['is_match'] = False
        
        data['type'] = type
        trans_pointer += len(a)
        words_analysis.append(data)
        prev_spoken_words = a

    result['words_analysis'] = words_analysis

    # Reset for later use
    disf.reset()

    return result


@app.route('/compute_stats_from_audio', methods=['POST'])
def compute_stats_from_audio():
    # check if the post request has the file part
    print("form", request.form)
    target_sentence = request.form.get('target_sentence')
    if target_sentence is None:
        print("No target sentence!")
        flash('No target sentence')
        return {}
    filename = secure_filename(COMMON_FILE_NAME)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # target_sentence = 'my grandfather you asked to know all about my grandfather he is nearly ninety three years old'
    # target_sentence = 'the missile knows where it is'  
    # target_sentence = 'the things they asked about were whether the judge should be the one that does the sentencing'
    results = json.loads(os.popen('python transcribe.py ' + filepath).read())
    stats = compute_stats(target_sentence, results)
    print(json.dumps(stats, indent=2))
    return stats

if __name__ == "__main__":
    
    app.run(port=5050)

    filename = '13842.wav'
    target_sentence = 'my grandfather you asked to know all about my grandfather he is nearly ninety three years old'
    # target_sentence = 'the missile knows where it is'  
    # target_sentence = 'the things they asked about were whether the judge should be the one that does the sentencing'
    results = json.loads(os.popen('python3 transcribe.py ' + filename).read()) 
    print(json.dumps(compute_stats(target_sentence, results), indent=2))


