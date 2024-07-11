from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return "Hello world!"