from flask import Blueprint, jsonify

homepage = Blueprint('homepage', __name__)


@homepage.route('/')
def index():
    return jsonify("its working don't worry!")
