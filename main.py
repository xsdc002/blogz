from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(777))

    def __init__(self, title, body):
        self.title = title
        self.body = body

blogs=[]
@app.route('/')
def index():
    blogs=Blog.query.order_by("id dec").all()
    return render_template('index.html', title = 'Build a Blog', blogs=blogs)

@app.route('/addblog')
def addblog():
    return render_template('add a blog entry.html', title = 'add blog')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        
    blogs = Blog.query.all()

    return render_template('main blog page.html', blogs=blogs)

@app.route('/addblog', methods=['POST', 'GET'])
def ilikedogs():
    if request.method == 'POST':
        blogid = request.args.get('id')
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        blogs = ''
        if blogid is None:
            blogs = Blog.query.all()
            return redirect('/')
        else:
            blog=Blog.query.get(int(blogid))
            return render_template('add a blog entry.html', blogs=[blog])
        
        return render_template("add a new post.html")
    @app.route('/blogpage', methods=['POST', 'GET'])
    def poo():
        if request.method == 'POST':
            blogid = int(request.form['blogid'])
            title = Blog.query.get('title')
            body = Blog.query.get('body')
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            
            return render_template('add a blog entry.html', newblog=newblog)
    
        if request.method == 'GET':
            blogid = request.args.get('id')
            if blogid is None:
                blogs = Blog.query.all()
                return redirect('/')
            else:
                blog = Blog.query.get(int(blogid))
                return render_template('Main blog page.html', blogs=[blog])
if __name__ == '__main__':
    app.run()
