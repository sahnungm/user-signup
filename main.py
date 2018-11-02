from flask import Flask, request, redirect
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))



@app.route("/")
def index():
    template = jinja_env.get_template('create-account.html')
    return template.render()

@app.route("/Create", methods=['POST'])
def create():
    username = request.form['username']
    password = request.form['password']
    v_pwd = request.form['verify_password']
    email = request.form['email']

    pwd_error = verify(v_pwd, password)
    username_error = ""
    email_error = email_check(email)

    
    if username == "":
        username_error = "Please choose a Username"
    else:
        username_error = check(username)
    
    if (pwd_error == "" and username_error == "" and email_error == ""):
        template = jinja_env.get_template('welcome.html')
        #incorrect --return redirect('/welcome?title="Welcome"&username=username')
        return template.render(title="Welcome", username=username)

    template = jinja_env.get_template('create-account.html')
    return template.render(title="Create-Account", username=username, username_error=username_error, email=email, email_error=email_error, pwd_error=pwd_error)
    #incorrect form --redirect('/?username={0}&username_error={1}&email={2}&email_error={3}&pwd_error={4}'.format(username, username_error, email, email_error, pwd_error))

def verify(v_pwd, password):

    if v_pwd != password:
        return "Passwords do not match."
    if password == "":
        return "Please enter a password"
    else:
        return check(password)
    
def check(entry):
    if len(entry) < 3 or len(entry) > 20:
        return "Must be 3-20 characters."
    for a in entry:
        if a == " ":
            return "Must contain no spaces"
    return ""
    
def email_check(email):
    if email != "":
        return check(email)
    else:
        for a in email:
            if a == "@":
                for b in range(email[a], len(email)-a-1, 1):
                    if b == ".":
                        return ""
    if email == "":
        return ""

    return "Please enter a valid email.(example@email.com)"

@app.route("/welcome")
def welcome(title, username):

    template = jinja_env.get_template('welcome.html')
    return template.render(title="Welcome", username=username)


app.run()