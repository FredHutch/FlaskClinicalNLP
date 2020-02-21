import json
import logging

from flask import Blueprint, render_template, request, session, abort, jsonify, Response, current_app, g


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

spacy_interface = spacy.load('en_core_sci_md')
spacy_bio_ner_interface = spacy.load('en_ner_bionlp13cg_md')

bp = Blueprint('spacy', __name__, url_prefix='/spacy')


@bp.route("/", methods=['POST'])
def spacy(type="all"):
    if not request.json or not 'extract_text' in request.json:
        abort(400)

    note_text = request.json['extract_text']
    if note_text:
        return _get_preprocessed_text(note_text, type)
    else:
        msg = "No Entity Text was found"
        logger.info("No text was preprocessed")
        return Response(msg, status=400)


def _get_preprocessed_text(note_text, types):
    processed_text = {}

    try:
        processed_text['tokens'] = _tokenize(note_text)
        processed_text['pos_tags'] = _tag_pos(note_text)
        processed_text['entities'] = _label_entities(note_text)
        processed_text['sentences'] = _split_sentences(note_text)
        processed_text['dependencies'] = _parse_dependencies(note_text)
    except ValueError as e:
        msg = "An error occurred while attempting to preprocess the text with spacy"
        logger.warning("An error occurred while attempting to preprocess the text with spacy: {}".format(e))
        return Response(msg, status=400)

    logger.info("preprocessing complete for text with options: {}".format(types))
    return Response(json.dumps(processed_text), mimetype=u'application/json')


def _tokenize(text):
    if not isinstance(text, str):
        raise ValueError("Invalid Type Error")
    return [token.text for token in spacy_interface(text or "")]


def _tag_pos(text):
    if not isinstance(text, str):
        raise ValueError("Invalid Type Error")
    return [(token.text, token.pos_) for token in spacy_interface(text or "")]


def _label_entities(text):
    if not isinstance(text, str):
        raise ValueError("Invalid Type Error")
    return [(entity.text, entity.label_) for entity in spacy_bio_ner_interface(text or "").ents]


def _split_sentences(text):
    if not isinstance(text, str):
        raise ValueError("Invalid Type Error")
    return [sent.text for sent in spacy_interface(text or "").sents]


def _parse_dependencies(text):
    if not isinstance(text, str):
        raise ValueError("Invalid Type Error")
    return [(token.text, token.dep_, token.head.text, token.head.pos_, [str(child) for child in token.children])
            for token in spacy_interface(text or "")]