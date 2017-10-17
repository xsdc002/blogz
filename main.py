from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#######start form models



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(777))

    def __init__(self, title, body):
        self.title = title
        self.body = body

###### end form models


######start routing

#index route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html') 



##blog route
@app.route('/blogs', methods=['GET', 'POST'])
def blogs(title='', body=''):

    if title != '':
        return render_template('blogs.html', title=title, body=body)
    
    return render_template('blogs.html')

###post route
@app.route('/posts', methods=['GET', 'POST'])
def posts():
   
    if request.method == 'POST':

        app.logger.debug('The request made was', request.method)

        #grabbing variables with the values from the form
        title = request.form['title']
        body = request.form['body']
        
        #left hand assignment is what the page will look for and how to call that value
        return render_template('blogs.html', title=title, body=body)

    
    return render_template('posts.html')



#####end routing

if __name__ == '__main__':
    app.run()