from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author':'li chen',
        'title':'blog post1',
        'content': ' first post content',
        'date_posted':'Feb 16 2023'
    },
{
        'author':'Fang Yiting',
        'title':'blog post2',
        'content': ' wo shi da sha zi',
        'date_posted':'Feb 17 2023'
    }
]

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


if __name__ == '__main__':
    app.run(debug=True)
