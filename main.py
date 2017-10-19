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

        if user and check_password(password, user.password):
            session['username'] = username
            return redirect('/posts')
        if not user:
            return render_template('login.html', username_error="Incorrect Username")
        else:
            return render_template('login.html', password_error="Incorrect Password")
    return render_template('login.html')

###signup route
@app.route('/index', methods=['GET', 'POST'])
def signup():
    password = (request.form['password'])
    verify = (request.form['verify'])
    email = (request.form['email'])
    username = (request.form['username'])
    password_error = ''
    verify_error = ''
    email_error = ''
    username_error = ''

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

    #email tests
   
    if len(email) > 0:
        if ' ' in email:
            email_error = 'invalid email, email cannot contain any spaces'
        elif email.count('@') > 1 in email:
            email_error = 'invalid email'
        elif email.count('.') < 1 in email:
            email_error = 'invalid email'
        elif ' ' in email:
            email_error = 'invalid email, email cannot contain spaces'

    #username tests
    if len(username) < 3:
        username_error = 'username must be greater than 3 characters'
    elif len(username) > 20:
        username_error = 'username must be greater than 20 characters'
    elif ' ' in username:
        username_error = 'invalid username, email cannot contain any spaces'
    if exists:
        username_error = "Username already exists."
        
    if not username_error and not password_error and not verify_error and not email_error and not exists:
        return render_template('usersignupwelcome.html', username=username)
    else:
        return render_template('index.html', password_error=password_error, verify_error=verify_error, email=email, email_error=email_error, username=username, username_error=username_error)

    render_template('blogs.html')



        #verify registration
        # #######add in if statement to check that the user has registered and is in the database##########
    #     if not username_error and not password_error and not verify_error and not email_error:
    #     return render_template('usersignupwelcome.html', username=username)
    # else:
    #     return render_template('index.html', password_error=password_error, verify_error=verify_error, email=email, email_error=email_error, username=username, username_error=username_error)

    # render_template('blogs.html') 

## Blogs Route
@app.route('/blogs', methods=['GET', 'POST'])
@app.route('/blogs', methods=['GET', 'POST'])
def blogs(title='', body='', owner=''):

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
        owner = User.query.filter_by(username=session['username']).first()

        post = Blog(title, body, owner)

        db.session.add(post)
        db.session.commit()
        page_id = new_post.id

        flash('Your blog has been posted!')
        #left hand assignment is what the page will look for and how to call that value
        return render_template('blogs.html', title=title, body=body, owner=owner)

    
    return render_template('posts.html')



######logout route##############
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
############### End Routing 

if __name__ == '__main__':
    app.secret_key = "secretkey"
    app.run(debug=True)
