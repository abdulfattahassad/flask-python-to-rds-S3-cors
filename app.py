from flask import Flask, render_template, request, jsonify,render_template_string
from flask_sqlalchemy import SQLAlchemy
import boto3
import json


app = Flask(__name__)

# Secrets Manager
secret_client = boto3.client('secretsmanager')
secret_response = secret_client.get_secret_value(SecretId='dbsecret05')
secrets = json.loads(secret_response['SecretString'])
DB_USERNAME = secrets['DB_USERNAME']
DB_PASSWORD = secrets['DB_PASSWORD']
DB_HOST = secrets['DB_HOST']
DB_NAME = secrets['DB_NAME']

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    suggest = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Added price column

# Create tables 

with app.app_context():
    db.create_all()

# S3 client
s3_client = boto3.client('s3')

bucket_name = 'cors'

# Routes
@app.route('/')

####. getobject return dictionary whcih has 'Body' key.  like like Body: <botocore.response.StreamingBody object at 0x7f8c2c0d1d90>. 
## so in order to access it  use obj['Body'].   then read it using .read(). . then convert to string
def index():
    
    key = 'index.html'
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    html_content = obj['Body'].read().decode('utf-8')
    return render_template_string(html_content)

@app.route('/menus')
def get_menus():
    
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    image_urls = []

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            image_urls.append(f"https://{bucket_name}.s3.amazonaws.com/{key}")

    return jsonify({"images": image_urls})


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    msg = request.form.get("msg")

    # Save to database
    new_menu = Menu(name=name, suggest=msg, price=0)
    db.session.add(new_menu)
    db.session.commit()

    return "Form submitted successfully!"


if __name__ == '__main__':
    app.run(debug=True)









