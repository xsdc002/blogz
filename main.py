from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


############### Start Form Models 




############### End Form Models



############### Start Datebase Models 

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(777))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')


    def __init__(self, username, password):
        self.username = username
        self.password = password


############### End Datebase Models 


############### Start Routing 
## Index Route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

####login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        #return render_template('usersignupwelcome.html')
        
    
        if user and check_password(password, user.password):
            session['username'] = username
            return redirect('posts.html')
        if not user:
            return render_template('login.html', username_error="Incorrect Username")
        else:
            return render_template('login.html', password_error="Incorrect Username or Password")
    return render_template('login.html')
###signup route
# 
###signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    password = (request.form['password'])
    verify = (request.form['verify'])
    username = (request.form['username'])
    password_error = ''
    verify_error = ''
    username_error = ''    
    signup = request.form['signup']

     #password tests
    if len(password) < 3:
        password_error = 'Password must be greater than 3 characters'
    elif len(password) > 20:
        password_error = 'Password must be less than 20 characters'

    elif ' ' in password:
        password_error = 'Password cannot contain any spaces'
    


    #verify tests
    if len(verify) < 3:
        verify_error = 'verify must be greater than 3 characters'
    elif len(verify) > 20:
        verify_error = 'verify must be greater than 20 characters'
    elif verify != password:
        verify_error = 'passwords do not match'
    elif ' ' in verify:
        verify_error = 'verify cannot contain any spaces'

    #username tests
    if len(username) < 3:
        username_error = 'username must be greater than 3 characters'
    elif len(username) > 20:
        username_error = 'username must be greater than 20 characters'
    elif ' ' in username:
        username_error = 'invalid username, email cannot contain any spaces'

    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(login.html('login'))
    return render_template('signup.html', form=form)


####newpost route
@app.route('/newpost')
def post():
    return render_template('newpost.html', title="New Post")

## Post Route
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':  
    
        #grabbing variables with the values from the form
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        #post = Blog(title, body, owner)

    if request.method == 'POST':
        post = Blog(title, body, owner)  
        new_post = Blog(title, body, owner)
        db.session.add(new_post)
        db.session.commit()
        page_id = new_post.id
        return redirect("/blog?id={0}".format(page_id))
    else:
        flash('Your blog has been posted!')
        #left hand assignment is what the page will look for and how to call that value
        return render_template('newpost.html', title=title, body=body, owner=owner)

    
    #return render_template('posts.html')



######logout route##############
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
############### End Routing 

if __name__ == '__main__':
    app.secret_key = "secretkey"
    app.run(debug=True)
