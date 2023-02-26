from flask import Blueprint
from flask import render_template


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def search():
    return render_template('search.html', title='Search two players')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/test")
def test():
    return render_template('test.html')


