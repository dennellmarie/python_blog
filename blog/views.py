# setup the views for the blog

# first import the render_template method
from flask import render_template
from flask import request, redirect, url_for

# import the other modules of the app
from . import app
from .database import session, Entry

# to handle log-in
from flask import flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from .database import User
from flask_login import login_required
from flask_login import current_user

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

@app.route("/entry/<int:id>")
def single_entry(id):
    entry = session.query(Entry).filter_by(id=id).one()
    return render_template("single_entry.html", entry=entry, id=id)

@app.route("/entry/<int:id>/edit", methods=['GET', 'POST'])
def edit_entry(id):
    entryToEdit= session.query(Entry).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['title']:
            entryToEdit.title = request.form['title']
            entryToEdit.content = request.form['content']
            #entryToEdit.datetime = datetime.datetime.now()
            session.add(entryToEdit)
            session.commit()
        return redirect(url_for('entries'))
    else:
        return render_template('edit_entry.html', p=entryToEdit)

@app.route("/entry/<int:id>/delete", methods = ["GET", "POST"])
def delete_entry(id):
    entryToDelete = session.query(Entry).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(entryToDelete)
        session.commit()
        return redirect(url_for('entries'))
    else:
        return render_template('delete_entry.html', i=entryToDelete)







#{% if current_user.is_authenticated %}

