from flask import Flask, redirect, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "secretkey"


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
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')


    def __init__(self, username, password):
        self.username = username
        self.password = password


############### End Datebase Models 


############### Start Routing 
###must be signed in to go to certain pages###

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

## Index Route
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

    users = User.query.all()
    return render_template('index.html', users=users)

####login route
@app.route('/login', methods=['POST', 'GET'])

def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            flash('You are now signed in')
            print(session)
            return redirect('/')
        
        flash('Please recheck username or password.')
        return render_template('login.html')
    elif request.method == 'GET':
        return render_template('login.html')
            
    return render_template('login.html')


###signup route
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # signup = request.form['signup']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
       
 #password tests
        if password == '' or len(password) < 3 or len(password) > 20 or ' ' in password:
            error = 'Passwords must be between 3 and 20 characters and must not contain spaces'
            return render_template('signup.html', error=error)

        #username tests
        if username == '' or len(username) < 3 or len(username) > 20 or ' ' in username:
            error = 'Usernames must be between 3 and 20 characters and must not contain spaces'
            return render_template('signup.html', error=error)

    ###verif)y password 
        if not verify_password == password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)
        user = User.query.filter_by(username=username).first()
        if user:
            flash("That username already exists")
            return render_template('signup.html')

        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        flash('You are now signed in')
        return render_template('index.html')   
    return render_template('signup.html')
              

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    # title = request.form['title']
    # body = request.form["body"]
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    posts = db.session.query(Blog).limit(50)
    # page_id = Blog.query.get('id')
    

    if blog_id:
        posts = Blog.query.filter_by(id=blog_id).first()
        return render_template("posts.html", title=posts.title, body=posts.body, user=posts.owner.username, user_id=posts.owner_id)
    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', entries=entries)

    return render_template('blogs.html', posts=posts)

# New post route. Redirects to post page.
## Post Route 
@app.route('/posts')
def posts():
    return render_template('posts.html', title="Posts")

@app.route('/posts', methods=['GET', 'POST'])
def newposts():
         
    # if request.method == 'POST':

        #grabbing variables with the values from the form
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first() 

        

        title_error = ""
        body_error = ""

        if title == "":
            title_error = flash("Y'all need a title for your blog.")
            
        if body == "":
            body_error = flash("Y'all need some content for your blog, make it interesting.")

        if not title_error and not body_error:
            posts = Blog(title, body, owner)
            db.session.add(posts)
            db.session.commit()
            page_id = posts.id
            return redirect ("blog?id={0}".format(page_id))

        else:
            return render_template("posts.html", title=title, body=body, title_error=title_error, body_error=body_error)



######logout route##############
@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        flash('Thanks for visiting!')
        return render_template('login.html')

    flash('You are not logged in')
    return render_template('login.html')



############### End Routing 

if __name__ == '__main__':
    app.run(debug=True)
