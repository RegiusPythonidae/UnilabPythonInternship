from flask import Blueprint, render_template, redirect, url_for
from os import path
from uuid import uuid4
from flask_login import login_required, current_user

from src.extensions import db
from src.views.films.forms import UploadFilm
from src.views.main.forms import EmptyForm
from src.models.film import Film, UserFilm
from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIRECTORY, "templates", "films")
film_bp = Blueprint("films", __name__, template_folder=TEMPLATES_FOLDER)


@film_bp.route('/upload_film', methods=['GET', 'POST'])
def upload_film():
    form = UploadFilm()
    if form.validate_on_submit():
        cover = form.cover.data
        filename, file_extension = path.splitext(cover.filename)
        filename = str(uuid4())
        directory = path.join(Config.UPLOAD_PATH, f"{filename}{file_extension}")
        cover.save(directory)
        film = Film(title=form.title.data, director=form.director.data, genre=form.genre.data, release_date=form.release_date.data, cover=filename)
        db.session.add(film)
        db.session.commit()
    return render_template('upload_film.html', form=form)


@film_bp.route('/like_film/<int:id>', methods=['GET', 'POST'])
@login_required
def like_film(id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_film = UserFilm(user_id=current_user.id, film_id=id)
        user_film.create()
    return redirect(url_for('main.home'))


@film_bp.route('/<user>/liked', methods=['GET', 'POST'])
@login_required
def liked_films(user):
    return render_template('liked_films.html')