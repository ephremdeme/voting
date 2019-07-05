from flask import Blueprint, render_template, request, jsonify, send_file
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@main.route('/create_election', methods=["GET"])
def create_election():
    return render_template('addelection.html')


@main.route('/create_election', methods=["POST"])
def election_post():
    year = request.form.get('year')
    school = request.form.get('school')
    dept = request.form.get('dept')
    voter = request.files['file']
    voter.save('voter_list.xlsx')
    from util import ExcelUtil
    array = ExcelUtil.read_excel('voter_list.xlsx')
    ExcelUtil.write_to_excel(array)
    return send_file('../gen.xlsx',  as_attachment=True)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
