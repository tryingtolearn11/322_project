from app import app 


''' All Handlers go here. For example: 
    Login function -> login(),
    Register function -> register()...
    
*** Keep ONLY those types of functions in here
'''


# Home Page 
@app.route('/')
@app.route("/index")
def index():
    return "Hello world!"


# Login Page
@app.route("/login")
def login():
    return ("Login Page :)")






