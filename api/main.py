from flask import Blueprint, render_template, request, jsonify, send_file

from api.auth import admin_permission
from . import db
from api.BlockchainAPINode import votedb
from .models import Vote
from flask_login import login_required, current_user
from util.ExcelUtil import generate_pin_excel

from util.VoteUtil import VoteUtil

from . import token_required

main = Blueprint('main', __name__)


@main.route('/votes', methods=["GET"])
@token_required
def votes(current_user):
    print(current_user.votes[0].toJson())
    return jsonify({
        "votes": [vote.toJson() for vote in current_user.votes]
    })


@main.route('/file/<vote_hash>', methods=["GET"])
@token_required
def file( current_user, vote_hash):
     return send_file('../' + vote_hash + '.xlsx', as_attachment=True)
     


@main.route('/vote/<vote_hash>/cast', methods=["POST"])
def verify(vote_hash):
    data = request.get_json()
    print(data)
    pin = data['pin']
    candidate_addr = data['candidate_addr']
    vote = VoteUtil()
    voted = vote.cast_vote(vote_hash, pin, candidate_addr)
    if voted == True:
        return jsonify({
            "message": "Successfully Voted",
            "vote_hash": vote_hash
        })
    else:
        return voted

@main.route('/create_vote', methods=["POST"])
@token_required
def create_vote(current_user):
    data = request.get_json()
    name = data['name']
    organizer = data['organizer']
    voter_count = data['voter_count']
    candidates = data['candidates']
    vote_hash = votedb.vote_hash(name, organizer, current_user.id)
    print(data, vote_hash, "\n", current_user.id)

    votedb.store_vote_candidates(candidates, vote_hash)

    array = generate_pin_excel(int(voter_count), vote_hash)

    votedb.store_vote_voters(array, vote_hash)

    vote = Vote(vote_name=name, hash=vote_hash, user_id=current_user.id)
    db.session.add(vote)
    db.session.commit()
    print(current_user.votes)

    # return send_file('../new_gen.xlsx', as_attachment=True)

    return jsonify({
        "name": name,
        "address": vote_hash
    }), 200


@main.route('/get_candidate', methods=['POST'])
def get_candidate():
    # d0a01cc9499532f2da65c5a58b9c6a733f164b60bed9f0f1e0c078a4b0da29da
    json = request.get_json()
    sec_hash = json['sec_hash']
    print(sec_hash)
    print(votedb.get_vote_candidates(sec_hash))
    return jsonify({"candidate": votedb.get_vote_candidates(sec_hash)})


@main.route('/vote/<vote_hash>/candidates', methods=['GET'])
def get_candidates(vote_hash):
    # d0a01cc9499532f2da65c5a58b9c6a733f164b60bed9f0f1e0c078a4b0da29da
    print(votedb.get_vote_candidates(vote_hash))
    return jsonify({"candidates": votedb.get_vote_candidates(vote_hash)})
