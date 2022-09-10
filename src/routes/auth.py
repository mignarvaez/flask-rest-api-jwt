''' File related with the auth process

We use Blueprints
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are 
registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
'''
from flask import Blueprint, request, jsonify

from src.database import db

# We use werkzeug.security for dealing with password
from werkzeug.security import check_password_hash, generate_password_hash

# Constants about HTTP messages
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

# Validators for fields
import validators

# The model of patient
from src.models.patient import Patient

# Import utilities for jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity

# Import swagger annotation
from flasgger import swag_from

# Define a blueprint for auth, the name indicates where is defined, (this file) and also we specify an url.
auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    """User Registration
    ---
tags:
  - Authentication
parameters:
  - name: body
    description: The body should contain the user Registration data
    in: body
    required: true
    schema:
      type: object
      required:
        - "username"
        - "password"
        - "email@email.com"
      properties:
        email:
          type: "email"
          example: "email@email.com"
        username:
          type: "username"
          example: "username"
        password:
          type: "string"
          format: password
          example: "********"
responses:
  201:
    description: When a user successfully logs in

  400:
    description: Fails to Register due to bad request data"""
    
    # We retrive this information from the request body
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    # Check for the password, username and email
    if len(password)<6:
        return jsonify({'error':"Password is too short"}),HTTP_400_BAD_REQUEST
    
    if len(username)<3:
        return jsonify({'error':"Username is too short"}),HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return jsonify({'error':"Usename should be alphanumeric and should not have spaces"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error':"Email is not valid"}),HTTP_400_BAD_REQUEST
    
    # Check if the email or username is already taken
    if Patient.query.filter_by(email=email).first() is not None:
        return jsonify({'error':"Email is taken"}),HTTP_409_CONFLICT
    
    if Patient.query.filter_by(username=username).first() is not None:
        return jsonify({'error':"Username is taken"}),HTTP_409_CONFLICT
    
    # If there is any error with the fields we generate the hash password
    pwd_hash=generate_password_hash(password)
    
    # Save the new patient in the database
    patient = Patient(username=username,password=pwd_hash,email=email)
    db.session.add(patient)
    db.session.commit()
    
    # Return a message with information of the patient
    return {'message':"Patient created",
            'user':{
                'username':username, 'email':email
            }}, HTTP_201_CREATED

@auth.post('/login')
def login():
    """User log in
---
tags:
  - Authentication
parameters:
  - name: body
    description: The body should contain the user login credentials
    in: body
    required: true
    schema:
      type: object
      required:
        - "email"
        - "password"
      properties:
        email:
          type: "email"
          example: "user@gmail.com"
        password:
          type: "string"
          format: password
          example: "********"
responses:
  200:
    description: When a user successfully logs in

  400:
    description: Fails to login due to bad request data

  401:
    description: A user supplies incorrect credentials
""" 
    # When we use request.json['NAME'] the application will throw a 400 error if name is not found, and application fail
    # when we use .get tha application will continue and the result of the method will be nonea and application won't fail
    # for query strings it is better to use .get
    email = request.json.get('email','')
    password = request.json.get('password','') 
    
    # Find user by email
    patient = Patient.query.filter_by(email=email).first()
    
    # If exist we check the password
    if patient:
        is_pass_correct=check_password_hash(patient.password, password)
        # If pass is correct we create jwt refresh and access token and return them
        if is_pass_correct:
            refresh = create_refresh_token(identity=patient.id)
            access = create_access_token(identity=patient.id)

            return {
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':patient.username,
                    'email':patient.email 
                }
            },HTTP_200_OK
    # If patient does not exist
    return {'error':'Wrong credentials'},HTTP_401_UNAUTHORIZED

# With jwt_required we specify that it is necessary a jwt token for access this endpoint
@auth.get('/me')
@jwt_required()
def me():
    
    # We get the id of the user who is logged
    patient_id = get_jwt_identity()
    # We get the information related to the patient logged and return his username and email.
    patient = Patient.query.filter_by(id=patient_id).first()
    return {
        'username': patient.username,
        'email': patient.email
    },HTTP_200_OK

# token used for refresh user token    
@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity=get_jwt_identity()
    access = create_access_token(identity=identity)
    return {
        'access':access
    },HTTP_200_OK