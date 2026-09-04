from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.note import Note
from app.extensions import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home/index.html")


@main.route("/dashboard")
@login_required
def dashboard():

    search_query = request.args.get("q", "").strip()

    notes_query = Note.query.filter_by(user_id=current_user.id)

    if search_query:
        notes_query = notes_query.filter(
            db.or_(
                Note.title.ilike(f"%{search_query}%"),
                Note.content.ilike(f"%{search_query}%")
            )
        )

    notes = notes_query.order_by(Note.created_at.desc()).all()

    return render_template(
        "dashboard/dashboard.html",
        user=current_user,
        notes=notes,
        search_query=search_query
    )
