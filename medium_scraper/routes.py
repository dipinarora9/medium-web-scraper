from flask import Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify("its working don't worry!")
