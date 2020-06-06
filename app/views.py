from app import app, db
from flask import render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SelectField, SelectMultipleField, IntegerField, TextAreaField, HiddenField, \
    SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired
from toolbox import db_util
from toolbox import cmSearch
from app.models import Card
import sys
from urllib.parse import unquote


# Forms

class SearchForm(FlaskForm):
    search = StringField('search')
    submit = SubmitField()


class ConfirmForm(FlaskForm):
    img = HiddenField('img', validators=[DataRequired()])
    idProduct = HiddenField('idProduct', validators=[DataRequired()])
    name = HiddenField('name', validators=[DataRequired()])
    id = HiddenField('id')
    idLanguage = SelectField('language', choices=[('1', 'English'), ('2', 'French'), ('3', 'German'), ('4', 'Spanish'),
                                                ('5', 'Italian'), ('6', 'Chinese (Simple)'), ('7', 'Japanese'),
                                                ('8', 'Portugese'), ('9', 'Russian'), ('10', 'Korean'),
                                                ('11', 'Chinese (Traditional)')])
    condition = SelectField('condition', choices=[('MT', 'Mint'), ('NM', 'Near Mint'), ('EX', 'Excellent'),
                                                  ('GD', 'Good'), ('LP', 'Light-played'), ('PL', 'Played'),
                                                  ('PO', 'Poor')])
    isFoil = RadioField('isFoil', choices=[('false', 'No'), ('true', 'Yes')], validators=[DataRequired()])
    count = IntegerField('quantity', validators=[DataRequired()])
    comments = TextAreaField('comments')
    submit = SubmitField()

class UpdateForm(FlaskForm):
    img = HiddenField('img', validators=[DataRequired()])
    idProduct = HiddenField('idProduct', validators=[DataRequired()])
    name = HiddenField('name', validators=[DataRequired()])
    id = HiddenField('id')
    idLanguage = SelectField('language', choices=[('1', 'English'), ('2', 'French'), ('3', 'German'), ('4', 'Spanish'),
                                                ('5', 'Italian'), ('6', 'Chinese (Simple)'), ('7', 'Japanese'),
                                                ('8', 'Portugese'), ('9', 'Russian'), ('10', 'Korean'),
                                                ('11', 'Chinese (Traditional)')])
    condition = SelectField('condition', choices=[('MT', 'Mint'), ('NM', 'Near Mint'), ('EX', 'Excellent'),
                                                  ('GD', 'Good'), ('LP', 'Light-played'), ('PL', 'Played'),
                                                  ('PO', 'Poor')])
    isFoil = RadioField('isFoil', choices=[('false', 'No'), ('true', 'Yes')], validators=[DataRequired()])
    delete = BooleanField('delete')
    count = IntegerField('quantity', validators=[DataRequired()])
    comments = TextAreaField('comments')
    submit = SubmitField()


class ResultsForm(FlaskForm):
    img = HiddenField('img', validators=[DataRequired()])
    name = HiddenField('name', validators=[DataRequired()])
    idProduct = HiddenField('idProduct', validators=[DataRequired()])
    submit = SubmitField()


class InventoryForm(FlaskForm):
    img = HiddenField('img', validators=[DataRequired()])
    name = HiddenField('name', validators=[DataRequired()])
    idProduct = HiddenField('idProduct', validators=[DataRequired()])
    id = HiddenField('id', validators=[DataRequired()])
    submit = SubmitField()


# Views

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home Page")


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results', search=form.search.data))

    return render_template('search.html', title="Search", form=form)


@app.route('/results/<string:search>', methods=['POST', 'GET'])
def results(search):
    cards = cmSearch.searcher(search)
    form = ResultsForm()

    if form.validate_on_submit():
        return redirect(
            url_for('confirm_listing', name=form.name.data, idProduct=form.idProduct.data, img=form.img.data))

    return render_template('results.html', title="Results for: {}".format(search), cards=cards, form=form)


@app.route('/confirm_listing/<int:idProduct>/<string:name>/<path:img>', methods=['POST', 'GET'])
def confirm_listing(name, idProduct, img):
    name = unquote(name)
    cardInfo = {'name': name, 'idProduct': idProduct, 'img': "//{}".format(img)}
    form = ConfirmForm()

    if form.validate_on_submit():
        db_util.add_card(form.data)
        return redirect(url_for('success'))
    else:
        print("FAIL", file=sys.stderr)

    return render_template('confirm_listing.html', title="Confirm Listing: {}".format(name), form=form,
                           cardInfo=cardInfo)


@app.route('/success', methods=['POST', 'GET'])
def success():
    return render_template('success.html', title="Success")


@app.route('/update', methods=['POST', 'GET'])
def update():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('inventory', search=form.search.data))
    return render_template('update.html', title="Update", form=form)

@app.route('/inventory/', methods=['POST', 'GET'])
@app.route('/inventory/<string:search>', methods=['POST', 'GET'])
def inventory(search = None):
    if not search:
        cards = db_util.query_card()
    else:
        cards = db_util.query_card(search)
    form = InventoryForm()
    if not cards:
        pass
    else:
        if form.validate_on_submit():
            return redirect(
                url_for('confirm_update', id=form.id.data))

    return render_template('inventory.html', title="Inventory results for: {}".format(search), cards=cards, form=form)


@app.route('/confirm_update/<int:id>', methods=['POST', 'GET'])
def confirm_update(id):
    cardInfo = Card.query.get(id)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.delete:
            db_util.delete_card(form.data)
        else:
            db_util.update_card(form.data)
        return redirect(url_for('success'))
    return render_template('confirm_update.html', title="Confirm Update", cardInfo=cardInfo, form=form, id=id)
