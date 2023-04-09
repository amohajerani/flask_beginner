from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, 'views')


@views.route('/')
def home():
    print('Running the request')
    return render_template('index.html', name='king')


@views.route('/profile/<username>')
def profile(username):
    args = request.args
    name = args.get('name')
    age = args.get('age')
    return render_template('index.html', username=username, name=name, age=age)
