from flask import Flask, request, jsonify, make_response, redirect, render_template, flash, session, url_for
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import requests 
from functools import wraps
app = Flask(__name__)
from requests.exceptions import RequestException
import os 

app.secret_key = os.getenv('SECRET_KEY')
api_url = os.getenv('API_URL')
from werkzeug.utils import secure_filename
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'static', 'uploads') 

# limiter_unauth = Limiter(get_remote_address, default_limits="20 per week") # idk this function are working or not, but the app can be initated


# limiter_auth = Limiter(key_func=lambda: session.get('access_token'), default_limits="20 per day") # same here

# limiter_auth.init_app(app)
# limiter_unauth.init_app(app)

def is_authenticated():
    # Simulate authentication check
    return request.headers.get("X-Authenticated-User") is not None

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            flash('Please log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def index():
    return(render_template('index.html'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('regist.html')


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        data = {
            'username': username,
            'email': email,
            'password': password
        }
        
        response = requests.post(api_url+'regist', json=data)
                
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/submit_page')
def submit_page():
    if not session.get('access_token'):
        return redirect(url_for('index'))
    if 'access_token' in session:
        return render_template('submit.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/scan', methods=['POST'])
def scan():
    if 'access_token' in session:
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path  = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            headers = {'Authorization': f'Bearer {session["access_token"]}'}
            files = {'file': (filename, open(file_path, 'rb'), file.content_type)}
            upload_response = requests.post(api_url+'uploadfile', headers=headers, files=files)
            
            # headers = {'Authorization': f'Bearer {session["access_token"]}'}
            # upload_response = requests.post(api_url+'uploadfile', headers=headers, files={'file': (file.filename, file, file.content_type)})
            
            if upload_response.status_code == 200:
                result = upload_response.json()
                art = result.get('detail').get('content')[0].get('art')
                filename = result.get('detail').get('content')[0].get('filename')
                confidence_value = float(result.get('detail').get('content')[0].get('confidence'))
                print("Filename from server:", filename)
                rounded_confidence = round(confidence_value, 2) 
                confidence = "{:.2%}".format(rounded_confidence)

                
                session['art'] = art
                session['filename'] = filename
                session['confidence'] = confidence
                return redirect(url_for('result'))
            else:
                return jsonify({"error": "Upload failed"}), 400
        else:
            return jsonify({"error": "No file selected"}), 400
    else:
        return jsonify({"error": "Cannot upload file without a valid token."}), 401
    
@app.route('/result')
def result():
    if not session.get('access_token'):
        return redirect(url_for('index'))
    art = session.get('art')
    filename = session.get('filename')
    confidence = session.get('confidence')
    image_url = url_for('static', filename=f'uploads/{filename}')


    if art is None or filename is None or confidence is None:
        flash('Result data is missing. Please try again.')
        return redirect(url_for('submit_page'))
        
    return render_template('result.html', art=art, filename=filename, confidence=confidence, image_url=image_url)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post(api_url + 'login', json={'username': username, 'password': password})
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            session['access_token'] = access_token
            flash('Login Success','alert')
            return redirect(url_for('submit_page'))
        else:
            if response.status_code == 401:
                error_message = response.json().get('detail', '')
                # flash(f"Login failed: {error_message}")
                return redirect(url_for('index'))
            else:
                flash("An unexpected error occurred during login.")
                return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
@require_login
def logout():
    try:
        requests.post(api_url + 'logout?username='+session['username'])
    except Exception as e:
        print(f"Failed to log out from the external service: {e}")
    
    session.pop('username', None)
    session.pop('access_token', None)
    session.pop('secret_key', None)

    flash('You have been logged out successfully.','alert')
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        response = requests.post(api_url + 'signup', json={'email': email, 'username': username, 'password': password})
        if response.status_code == 200:
            flash('Regist Succes','alert')
            return redirect(url_for('index'))
        else:
            if response.status_code == 400:
                error_message = response.json().get('detail', '')
                flash(f"Register failed: {error_message}")
                return redirect(url_for('register'))
            else:
                flash("An unexpected error occurred during login.")
                return redirect(url_for('register'))
    else:
        return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)