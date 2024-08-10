from flask import Flask, jsonify, request, Response, Blueprint
import requests

default_bp = Blueprint('default_bp', __name__, url_prefix='/')



@default_bp.route('/')
def home():
  return 'Hello, this is the home page!'

@default_bp.route('/about')
def about():
  return 'This is the about page.'

