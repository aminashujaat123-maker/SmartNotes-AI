from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.note import Note

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home/index.html")


@main.route("/dashboard")
@login_required
def dashboard():

    notes = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Note.created_at.desc()
    ).all()

    return render_template(
        "dashboard/dashboard.html",
        user=current_user,
        notes=notes
    )