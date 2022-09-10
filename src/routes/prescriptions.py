''' File related with the elements required for prescriptions handle

We use Blueprints
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are 
registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
'''
from flask import Blueprint,request
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

# Import the model for prescription
from src.models.prescription import Prescription

# Import library necessary to get the actual user
from flask_jwt_extended import get_jwt_identity,jwt_required

# Import the database
from src.database import db

# Define a blueprint for prescriptions, the name indicates where is defined, (this file) and also we specify an url.
prescriptions = Blueprint("prescriptions",__name__,url_prefix="/api/v1/prescription")


# Another way of declarate routes
@prescriptions.route('/',methods=['POST','GET'])
@jwt_required()
def handle_prescriptions():
    """Route used for getting or posting a prescription

    Returns:
        Http Message: ann http message
    """
    # We get the current logged user
    current_user = get_jwt_identity()
    
    # If the method is post, we capture the title and body and create a new prescripton
    # it is necessary to call commit for finish transaction
    if request.method == 'POST':
        title = request.get_json().get('title','')
        body = request.get_json().get('body','')
        prescription = Prescription(title=title, body=body, user_id=current_user) 
        db.session.add(prescription)
        db.session.commit()

        # Return a message with the new object
        return {
            'id':prescription.id,
            'title':prescription.title,
            'body':prescription.body,
            'expedition_date':prescription.expedition_date,
            'created_at':prescription.created_at,
            'updated_at':prescription.updated_at
        },HTTP_201_CREATED
    
    # If the method is get
    else:
        
        # We define pagination
        # Pagination, page 1 by default and 5 per page by default
        page = request.args.get('page',1,type=int)
        per_page=request.args.get('per_page',5,type=int)
        
        # We filter the prescriptions per user and then apply pagination
        prescriptions=Prescription.query.filter_by(user_id=current_user).paginate(page=page,per_page=per_page)
        
        # The container for the data
        data = []
        
        # We iterate over the prescription paginated
        for prescription in prescriptions.items:
            data.append({
            'id':prescription.id,
            'title':prescription.title,
            'body':prescription.body,
            'expedition_date':prescription.expedition_date,
            'created_at':prescription.created_at,
            'updated_at':prescription.updated_at 
            })
            
        # Information regarding prescriptions and pagination
        meta = {
            'page': prescriptions.page,
            'pages': prescriptions.pages,
            'total_count': prescriptions.total,
            'prev_page': prescriptions.prev_num,
            'next_page': prescriptions.next_num,
            'has_next': prescriptions.has_next,
            'has_prev': prescriptions.has_prev,
        }

        # for retrivieng all 11 of them in page 1
        # http://127.0.0.1:5000/api/v1/prescription?page=1&per_page=11
        
        # Return data and information regarding the pagination (meta)
        return {
            'data':data,
            'meta':meta
        },HTTP_200_OK

@prescriptions.get('/<int:id>')
@jwt_required()
def get_prescription(id:int):
    """Get prescription by id
---
tags:
  - Prescriptions
parameters:
  - in: header
    name: Authorization
    required: true
    
  - name: id
    description: The id of the prescription
    in: path
    required: true
    default: 1
responses:
  200:
    description: When a prescription with the given id exist and is returned sucessfully
    
  404:
    description: When a prescription with the given id
""" 
    """Get a prescription by id

    Args:
        id (int): The id of the prescription

    Returns:
        Http message: A http message
    """
    # We get the current user
    current_user = get_jwt_identity()
    # We filter the prescription by user and id
    prescription = Prescription.query.filter_by(user_id=current_user, id=id).first()
    
    # If there is no prescription for the id return a error message
    if not prescription:
        return {'message':'item not found'},HTTP_404_NOT_FOUND
    
    # Else, return the searched element
    return {
        'id':prescription.id,
        'title':prescription.title,
        'body':prescription.body,
        'expedition_date':prescription.expedition_date,
        'created_at':prescription.created_at,
        'updated_at':prescription.updated_at 
    },HTTP_200_OK

# We are gonna update using put or patch
@prescriptions.put('/<int:id>')
@prescriptions.patch('/<int:id>')
@jwt_required()
def edit_prescription(id:int):   
    """Edit a prescription given an id

    Args:
        id (int): The id of the prescription

    Returns:
        Http message: An http message
    """
    # we get the current logged user
    current_user = get_jwt_identity()
    # we look for the required item
    prescription = Prescription.query.filter_by(user_id=current_user, id=id).first()
    
    # if theres no item we return an error message
    if not prescription:
        return {'message':'Item not found'},HTTP_404_NOT_FOUND
    
    # We get the fields that cant be modified 
    title = request.get_json().get('title')
    body = request.get_json().get('body')
    
    # We set the new fields and we commit to the db
    prescription.title = title
    prescription.body = body
    db.session.commit()
    
    # Return the modified element
    return {
        'id':prescription.id,
        'title':prescription.title,
        'body':prescription.body,
        'expedition_date':prescription.expedition_date,
        'created_at':prescription.created_at,
        'updated_at':prescription.updated_at 
    },HTTP_200_OK
    
@prescriptions.delete("/<int:id>")
@jwt_required()
def delete_prescription(id:int):
    """Delete a prescription by id

    Args:
        id (int): The id of the prescription

    Returns:
        Http Message: an Http Message 
    """
    
    # We get the actual logged user
    current_user = get_jwt_identity()
    # We get the prescription we want to delete
    prescription = Prescription.query.filter_by(user_id=current_user,id=id).first()
    
    # if there's no prescription with the id given we return an error message
    if not prescription:
        return {'message':'Item not found'},HTTP_404_NOT_FOUND
    
    # else we delete the prescription and commit
    db.session.delete(prescription)
    db.session.commit()
    # return a message ok with no content
    return {},HTTP_204_NO_CONTENT