from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


############### Start Form Models 




############### End Form Models



############### Start Datebase Models 

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(777))

    def __init__(self, title, body):
        self.title = title
        self.body = body
############### End Datebase Models 


############### Start Routing 
## Index Route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')




## Blogs Route
@app.route('/blogs', methods=['GET', 'POST'])
@app.route('/blogs', methods=['GET', 'POST'])
def blogs(title='', body=''):

    if title != '':
        return render_template('blogs.html', title=title, body=body)

    else:
        
        posts = db.session.query(Blog).limit(50)
        return render_template('blogs.html', posts=posts)



## Post Route 
@app.route('/posts', methods=['GET', 'POST'])
def posts():
       
    if request.method == 'POST':

        #grabbing variables with the values from the form
        title = request.form['title']
        body = request.form['body']

        post = Blog(title, body)

        db.session.add(post)
        db.session.commit()

        flash('Your blog has been posted!')
        #left hand assignment is what the page will look for and how to call that value
        return render_template('blogs.html', title=title, body=body)

    
    return render_template('posts.html')
        


############### End Routing 




if __name__ == '__main__':
    app.secret_key = "secretkey"
    app.run(debug=True)
