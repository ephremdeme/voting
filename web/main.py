from flask import Blueprint, render_template, request, jsonify, send_file

from web.BlockchainAPINode import votedb
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def index():
    return render_template('explorer.html')


@main.route('/create_election', methods=["GET"])
def create_election():
    return render_template('addelection.html')


@main.route('/create_election', methods=["POST"])
def election_post():
    year = request.form.get('year')
    school = request.form.get('school')
    dept = request.form.get('dept')
    sec = request.form.get('section')
    candidate = request.form.get('candidate[]')
    candidate = str(candidate).splitlines()
    sec_hash = votedb.sec_hash(year, school, dept, sec)
    voter = request.files['file']
    voter.save('voter_list.xlsx')
    print(sec_hash)
    from util import ExcelUtil
    array = ExcelUtil.read_excel('voter_list.xlsx')
    votedb.store_sec_address(array, sec_hash)

    votedb.store_sec_candidate(array=candidate, section=sec_hash)
    ExcelUtil.write_to_excel(array)
    print(votedb.get_sec_candidate(sec_hash))
    return send_file('../gen.xlsx', as_attachment=True)


@main.route('/get_candidate', methods=['POST'])
def get_candidate():
    # d0a01cc9499532f2da65c5a58b9c6a733f164b60bed9f0f1e0c078a4b0da29da
    json = request.get_json()
    sec_hash = json['sec_hash']
    print(sec_hash)
    print(votedb.get_sec_candidate(sec_hash))
    return jsonify({"candidate": votedb.get_sec_candidate(sec_hash)})


@main.route('/profile')
@login_required
def profile():
    return render_template('explorer.html', name=current_user.name)


