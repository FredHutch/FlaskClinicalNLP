import logging

from flask import Blueprint, render_template, request, session, abort, jsonify, Response, current_app, g
from hdc_preprocessing import preprocess as preprocessInterface

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bp = Blueprint('preprocessing', __name__, url_prefix='/preprocess')


@bp.route("/", methods=['POST'])
def preprocess(type="all"):
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
    processed_text = ""

    try:
        processed_text = preprocessInterface.tokenize(note_text)
        processed_text = preprocessInterface.tag(processed_text)
        processed_text = preprocessInterface.sentences(processed_text)
        processed_text = preprocessInterface.dependency_parse(processed_text)
    except ValueError as e:
        msg = "An error occured while calling MedLP"
        logger.warning("An error occured while calling MedLPInterface: {}".format(e))
        return Response(msg, status=400)

    logger.info("preprocessing complete for text with options: {}".format(types))
    return Response(processed_text, mimetype=u'application/json')

