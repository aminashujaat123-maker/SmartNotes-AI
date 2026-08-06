from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.note import Note

notes = Blueprint("notes", __name__)


@notes.route("/notes/create", methods=["GET", "POST"])
@login_required
def create_note():

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        note = Note(
            title=title,
            content=content,
            user_id=current_user.id
        )

        db.session.add(note)
        db.session.commit()

        flash("Note created successfully!", "success")

        return redirect(url_for("main.dashboard"))

    return render_template("dashboard/create_note.html")

@notes.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        note.title = request.form.get("title")
        note.content = request.form.get("content")

        db.session.commit()

        flash("Note updated successfully!", "success")

        return redirect(url_for("main.dashboard"))

    return render_template(
        "dashboard/edit_note.html",
        note=note
    )

@notes.route("/notes/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("Note deleted successfully!", "success")

    return redirect(url_for("main.dashboard"))