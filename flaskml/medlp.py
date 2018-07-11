import logging

from flask import Blueprint, render_template, request, session, abort, jsonify, Response, current_app, g
from flaskml import medlpInterface
from amazonserviceinterface.MedLPServiceInterface import MedLPServiceInterface
import ClinicalNotesProcessor.JSONParser as JSONParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bp = Blueprint('medlp', __name__, url_prefix='/medlp')

@bp.route("/train")
def train_new_model():
    return "Stub for training a new model!"


@bp.route("/train/<int:model_id>")
def update_existing_model(model_id):
    return "Stub for online training an existing model!"


@bp.route("/annotate/", methods=['POST'])
def annotate(type="all"):
    if not request.json or not 'extract_text' in request.json:
        abort(400)

    note_text = request.json['extract_text']
    if note_text:
        return _get_entities(note_text, type)
    else:
        msg = "No Entity Text was found"
        logger.info("No entities returned")
        return Response(msg, status=400)


@bp.route("/annotate/phi", methods=['POST'])
def annotate_phi():
    return annotate(type=["PERSONAL_IDENTIFIABLE_INFORMATION"])



@bp.route("/members/<string:name>/")
def getMember(name):
    return name


def _get_entities(note_text, entityTypes):
    try:
        entities = medlpInterface.get_entities(note_text, entityTypes=entityTypes)
    except ValueError as e:
        msg = "An error occured while calling MedLP"
        logger.warning("An error occured while calling MedLPInterface: {}".format(e))
        return Response(msg, status=400)

    logger.info("{} entities returned for entity types: {}".format(len(entities), entityTypes))
    return Response(entities, mimetype=u'application/json')

