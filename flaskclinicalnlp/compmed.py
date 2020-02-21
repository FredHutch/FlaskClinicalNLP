import json
import logging

from flask import Blueprint, render_template, request, session, abort, jsonify, Response, current_app, g
from flaskclinicalnlp import compmed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bp = Blueprint('compmed', __name__, url_prefix='/compmed')

@bp.route("/", methods=['POST'])
def annotate(**kwargs):
    if not request.json or not 'extract_text' in request.json:
        abort(400)

    note_text = request.json['extract_text']
    if note_text:
        return _get_entities(note_text, **kwargs)
    else:
        msg = "No Entity Text was found"
        logger.info("No entities returned")
        return Response(msg, status=400)


@bp.route("/phi", methods=['POST'])
def annotate_phi():
    return annotate(entityTypes=["PROTECTED_HEALTH_INFORMATION"])


@bp.route("/medication", methods=['POST'])
def annotate_medication():
    return annotate(entityTypes=["MEDICATION"])


@bp.route("/condition", methods=['POST'])
def annotate_condition():
    return annotate(entityTypes=["MEDICAL_CONDITION"])


@bp.route("/ttp", methods=['POST'])
def annotate_ttp():
    return annotate(entityTypes=["TEST_TREATMENT_PROCEDURE"])


@bp.route("/anatomy", methods=['POST'])
def annotate_anatomy():
    return annotate(entityTypes=["ANATOMY"])


@bp.route("/members/<string:name>/")
def getMember(name):
    return name


def _get_entities(note_text, **kwargs):

    try:
        if 'entityTypes' in kwargs and kwargs['entityTypes'] == ["PROTECTED_HEALTH_INFORMATION"]:
            entities = compmed.get_phi(note_text)
        else:
            entities = compmed.get_entities(note_text, **kwargs)
    except ValueError as e:
        msg = "An error occurred while calling Comprehend Medical"
        logger.warning("An error occurred while calling Comprehend Medical Interface: {}".format(e))
        return Response(msg, status=400)

    logger.info("{} entities returned for entity types".format(len(entities)))
    return Response(json.dumps(entities), mimetype=u'application/json')