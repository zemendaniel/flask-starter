from flask import redirect, url_for, abort, flash
from security.decorators import is_fully_authenticated, is_admin
from . import bp
from blueprints.categories.forms import CreateCategoryForm
from persistence.repository.language import LanguageRepository
from persistence.model.language import Language


@bp.route('/creaate')
@is_fully_authenticated
@is_admin
def create():
    form = CreateCategoryForm()

    if form.validate_on_submit():
        language = Language()
        language.name = form.name
        language.save()
        flash('Programnyelv sikeresen létrehozva!', 'success')

    return redirect(url_for('pages.home'))


@bp.route('delete/<int:language_id')
@is_fully_authenticated
@is_admin
def delete(language_id):
    language = LanguageRepository.find_by_id(language_id) or abort(404)
    language.delete()
    flash('Programnyelv sikeresen törölve!', 'success')

    return  redirect(url_for('categories.list_all'))


@bp.route('edit/<int:language_id', methods=['post'])
@is_fully_authenticated
@is_admin
def edit(language_id):
    language = LanguageRepository.find_by_id(language_id)
    form = CreateCategoryForm()

    if form.validate_on_submit():
        language.name = form.name
        language.save()
        flash('Programnyelv sikeresen módosítva!', 'success')

