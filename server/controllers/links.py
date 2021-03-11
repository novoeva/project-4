from flask import Blueprint, request

#import the models
from models.link import Link
from models.comment import Comment

#importing all the schemas
from serializers.link import LinkSchema
from serializers.comment import CommentSchema

link_schema = LinkSchema()


from marshmallow.exceptions import ValidationError

# ! Initialise comment schema.
comment_schema = CommentSchema()

router = Blueprint(__name__, "links")


@router.route("/links", methods=["GET"])
def get_all_the_links():

    links = Link.query.all()


    return  link_schema.jsonify(links, many=True), 200




@router.route("/links/<int:link_id>", methods=["GET"])
def get_single_link(link_id):
    link = Link.query.get(link_id)

    if not link:
        return { 'message': 'Link not found' }, 404
    # ! 2) Serialize my link model to json.
    return link_schema.jsonify(link), 200

@router.route("/links", methods=["POST"])
def make_link():
    link_dictionary = request.json
  
    try:
  
        link = link_schema.load(link_dictionary)
    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }

    link.save()

    return link_schema.jsonify(link), 200


@router.route("/links/<int:link_id>", methods=["PUT"])
def update_link(link_id):

    existing_link = Link.query.get(link_id)
    link_dictionary = request.json

    try:

        link = link_schema.load(

            link_dictionary,
            instance=existing_link,
            partial=True
        )

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }


    link.save()


    return link_schema.jsonify(link), 201

@router.route("/links/<int:link_id>", methods=["DELETE"])
def remove_link(link_id):
    link = Link.query.get(link_id)

    link.remove()

    return { 'message': 'Link deleted successfully' }, 200


# ! POSTing a comment
@router.route('/links/<int:link_id>/comments', methods=['POST'])
def create_comment(link_id):

    comment_dictionary = request.json

    # ! Get the whole link model
    link = Link.query.get(link_id)

    try:
        comment = comment_schema.load(comment_dictionary)
        # ! Here I'm adding the whole cake, not just the ID
        comment.link = link

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }

    comment.save()

    return comment_schema.jsonify(comment)


# ! DELETE a comment

@router.route('/links/<int:link_id>/comments/<int:comment_id>', methods=['DELETE'])
def remove_comment(link_id, comment_id):

    comment = Comment.query.get(comment_id)

    comment.remove()

    link = Link.query.get(link_id)

    return link_schema.jsonify(link), 202



@router.route('/links/<int:link_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(link_id, comment_id):

    comment_dictionary = request.json
    existing_comment = Comment.query.get(comment_id)

    try:
        comment = comment_schema.load(
            comment_dictionary,
            instance=existing_comment,
            partial=True
        )

    except ValidationError as e:
        return { 'errors': e.messages, 'messages': 'Something went wrong' }

    comment.save()

    link = Link.query.get(link_id)

    return link_schema.jsonify(link), 201
