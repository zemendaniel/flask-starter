from flask import redirect, url_for, abort, flash, render_template
from security.decorators import is_fully_authenticated, is_admin
from . import bp
from blueprints.categories.forms import CreateCategoryForm
from persistence.repository.category import CategoryRepository
from persistence.model.category import Category


@bp.route('/create', methods=['post', 'get'])
@is_fully_authenticated
@is_admin
def create():
    form = CreateCategoryForm()

    if form.validate_on_submit():
        category = Category()
        category.name = form.name.data.strip()
        category.save()
        flash('Kategória sikeresen létrehozva!', 'success')
        return redirect(url_for('categories.list_all'))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('categories/form.html', form=form, create=True)


@bp.route('delete/<int:category_id>', methods=['post'])
@is_fully_authenticated
@is_admin
def delete(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    if category.teams:
        flash('A kategória nem törölhető, mert valaki használja!', 'error')
        return redirect(url_for('categories.list_all'))

    category.delete()
    flash('Kategória sikeresen törölve!', 'success')

    return redirect(url_for('categories.list_all'))


@bp.route('edit/<int:category_id>', methods=['post', 'get'])
@is_fully_authenticated
@is_admin
def edit(category_id):
    category = CategoryRepository.find_by_id(category_id)
    form = CreateCategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data.strip()
        category.save()
        flash('Kategória sikeresen módosítva!', 'success')
        return redirect(url_for('categories.edit', category_id=category_id))
    elif form.errors:
        [flash(error, 'error') for field, errors in form.errors.items() for error in errors]

    return render_template('categories/form.html', form=form, category=category, create=False)


@bp.route('/')
@is_fully_authenticated
@is_admin
def list_all():
    categories = CategoryRepository.find_all()

    return render_template("categories/list.html", categories=categories)
