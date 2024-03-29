from flask import Blueprint, request, g
from models.folder import Folder
from models.user import User
from serializers.folder import FolderSchema
from marshmallow.exceptions import ValidationError
from decorators.secure_route import secure_route
from models.users_folder import users_folder_join


folder_schema = FolderSchema()

router = Blueprint(__name__, "users")

@router.route("/folders", methods=["GET"])
@secure_route
def get_all_the_folders():

    folders = g.current_user.folders

    return folder_schema.jsonify(folders, many=True), 200


@router.route("/folders/<int:folder_id>", methods=["GET"])
@secure_route
def get_single_folder(folder_id):
    folder = Folder.query.get(folder_id)
    print('folder')
    if not folder:
        return { 'message': 'Folder not found' }, 404

    for item in g.current_user.folders:
        if item.id == folder_id:
            return folder_schema.jsonify(item), 200
        
    return {'errors': 'This is not your folder!'}, 401
        

@router.route("/folders", methods=["POST"])
@secure_route
def make_folder():

    folder_dictionary = request.json
  
    try:
        folder = folder_schema.load(folder_dictionary)

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }

    folder.save()
   
    print(folder.id)
    print(g.current_user.folders)

    g.current_user.folders.append(folder)
    g.current_user.save()

    print(g.current_user.folders)

    return folder_schema.jsonify(folder), 200


@router.route("/folders/<int:folder_id>", methods=["PUT"])
@secure_route
def update_folder(folder_id):

    existing_folder = Folder.query.get(folder_id)
    folder_dictionary = request.json


    try:
        for item in g.current_user.folders:
            if item.id == existing_folder.id:
                folder = folder_schema.load(

                folder_dictionary,
                instance=existing_folder,
                partial=True)

                folder.save()

                return folder_schema.jsonify(folder), 201
                

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }

    return {'errors': 'This is not your folder!'}, 401

@router.route("/folders/<int:folder_id>/users", methods=["POST"])
@secure_route
def add_user_to_folder(folder_id):

    existing_folder = Folder.query.get(folder_id)
    # print('existing folder', existing_folder)

    new_user_email = request.json.get('email')

    new_user = User.query.filter_by(email=new_user_email).first()

    # print('new user', new_user)
    

    if not new_user:
        return {'errors': 'This user is not registered!'}, 404

    try:
        for item in g.current_user.folders:
            if item.id == existing_folder.id:
                # print('folder users 1', existing_folder.users)
                
                # print('new user', new_user)
               
                existing_folder.users.append(new_user)
                # print('folder usrs 2', existing_folder.users)

                existing_folder.save()

                return folder_schema.jsonify(existing_folder), 201
                

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }, 400

    return {'errors': 'This is not your folder!'}, 401

@router.route("/folders/<int:folder_id>", methods=["DELETE"])
@secure_route

def remove_folder(folder_id):

    folder = Folder.query.get(folder_id)
    user = g.current_user

    try:
        for item in user.folders:
            if item.id == folder.id:
                
                if len(folder.users) > 1:
                    
                    folder.users.remove(user)
                    folder.save()
                    
                else:
                    folder.remove()

                return { 'message': 'Folder deleted successfully' }, 200

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }, 400

    return {'errors': 'This is not your folder!'}, 401







