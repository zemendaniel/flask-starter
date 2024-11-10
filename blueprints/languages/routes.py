from flask import redirect, url_for, abort, flash, render_template
from security.decorators import is_fully_authenticated, is_admin
from . import bp
from persistence.repository.language import LanguageRepository
from persistence.model.language import Language
from .forms import CreateLanguageForm


@bp.route('/create', methods=['GET', 'POST'])
@is_fully_authenticated
@is_admin
def create():
    form = CreateLanguageForm()

    if form.validate_on_submit():
        language = Language()
        language.name = form.name.data.strip()
        language.save()
        flash('Programnyelv sikeresen hozzáadva!', 'success')
        return redirect(url_for('languages.list_all'))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('languages/form.html', form=form, create=True)


@bp.route('delete/<int:language_id>', methods=['post'])
@is_fully_authenticated
@is_admin
def delete(language_id):
    language = LanguageRepository.find_by_id(language_id) or abort(404)
    language.delete()
    flash('Programnyelv sikeresen törölve!', 'success')

    return redirect(url_for('languages.list_all'))


@bp.route('edit/<int:language_id>', methods=['post', 'get'])
@is_fully_authenticated
@is_admin
def edit(language_id):
    language = LanguageRepository.find_by_id(language_id) or abort(404)
    form = CreateLanguageForm(obj=language)

    if form.validate_on_submit():
        language.name = form.name.data.strip()
        language.save()
        flash('Programnyelv sikeresen módosítva!', 'success')
        return redirect(url_for('languages.edit', language_id=language_id))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('languages/form.html', form=form, create=False, language=language)


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    languages = LanguageRepository.find_all()

    return render_template('languages/list.html', languages=languages)
