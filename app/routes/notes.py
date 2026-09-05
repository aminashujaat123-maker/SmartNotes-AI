from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
import io
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from app.utils.summarizer import generate_summary

from app.extensions import db
from app.models.note import Note

notes = Blueprint("notes", __name__)


def sanitize_for_pdf(text):
    """Remove characters that the PDF's core font (Latin-1) can't render,
    so PDF generation never crashes on emojis or special symbols."""
    if not text:
        return ""
    return text.encode("latin-1", errors="ignore").decode("latin-1")


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


@notes.route("/notes/<int:note_id>")
@login_required
def note_details(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "dashboard/note_details.html",
        note=note
    )


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


@notes.route("/notes/<int:note_id>/summarize", methods=["POST"])
@login_required
def summarize_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    note.summary = generate_summary(note.content)
    db.session.commit()

    flash("Summary generated successfully!", "success")

    return redirect(url_for("notes.note_details", note_id=note.id))


def wrap_long_words(text, max_word_length=60):
    """Insert a break inside any single 'word' that's too long to fit
    on one line, so fpdf2 never fails to render it."""
    if not text:
        return text

    words = text.split(" ")
    wrapped_words = []

    for word in words:
        if len(word) > max_word_length:
            chunks = [
                word[i:i + max_word_length]
                for i in range(0, len(word), max_word_length)
            ]
            wrapped_words.append(" ".join(chunks))
        else:
            wrapped_words.append(word)

    return " ".join(wrapped_words)


@notes.route("/notes/<int:note_id>/export")
@login_required
def export_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    title = wrap_long_words(sanitize_for_pdf(note.title)) or "Untitled Note"
    content = wrap_long_words(sanitize_for_pdf(note.content)) or " "
    summary = wrap_long_words(sanitize_for_pdf(note.summary)) if note.summary else ""

    pdf = FPDF()
    pdf.add_page()

    usable_width = pdf.epw

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(usable_width, 10, title, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 11)
    pdf.ln(4)
    pdf.multi_cell(usable_width, 8, f"Created: {note.created_at.strftime('%d %b %Y')}", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(usable_width, 8, content, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    if summary:
        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(usable_width, 8, "Summary", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(usable_width, 8, summary, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf_bytes = bytes(pdf.output())
    buffer = io.BytesIO(pdf_bytes)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{title}.pdf",
        mimetype="application/pdf"
    )