from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Welcome1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog_posts = Blog.query.all()
    return render_template('/blog.html', blog_posts=blog_posts)

def is_empty(text):
    if not len(text) > 0:
        return True
    else:
        return False

@app.route('/newpost', methods=['POST','GET'])
def new_blog():

    error_title = "Please fill in the title"
    error_body = "Please fill in the body"
    empty_title_error = ''
    empty_body_error = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if is_empty(title):
            empty_title_error = error_title
        if is_empty(body):
            empty_body_error = error_body

    if request.method == 'POST' and empty_body_error == '' and empty_title_error == '':
        new_post = Blog(title,body)
        db.session.add(new_post)
        db.session.commit()
        post_id = Blog.query.get(new_post.id)
        return render_template('post.html', post_id=post_id)
    else:
        return render_template('/newpost.html',empty_title_error=empty_title_error,empty_body_error=empty_body_error)


@app.route('/post')
def post():

    id = request.args.get('id')
    post_id = Blog.query.get(id)
    return render_template('/post.html',post_id=post_id)

if __name__ == '__main__':
    app.run()

