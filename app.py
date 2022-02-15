from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, validators, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SECRET_KEY']='thisisatopsecretsforme'
db = SQLAlchemy(app)

class courses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.String(length=30), nullable=False,unique=False)
    name = db.Column(db.String(length=30), nullable=False,unique=False)

    def __repr__(self):
        return '[courses {}]'.format(self.num)

class reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.String(length=30), nullable=True,unique=False)
    review = db.Column(db.String(length=30), nullable=False,unique=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))

def choice_query():
    return courses.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='num')

@app.route('/',methods=['GET', 'POST'])
def home_page():
    form_selection = ChoiceForm()
    if form_selection.validate_on_submit():
        # return '<html><h1>{}</h1></html>'.format(form_selection.opts.data)
        return render_template('home.html', form_selection=form_selection)
    return render_template('home.html')

@app.route('/courses')
def courses_page():
    courselists = courses.query.all()
    return render_template('courses.html', courselists = courselists)

@app.route('/currencyConvert')
def currency_convert():
    return render_template('currencyConvert.html')

@app.route('/course/<string:id>')
def course_page(id):
    results = courses.query.get(id)
    crn = str(results.num)
    all_reviews = reviews.query.filter(reviews.num == crn).all()
    course_name = all_reviews[0].num
    return render_template('course.html', all_reviews = all_reviews, id = id,course_name = course_name)

class PostForm(Form):
    course_num = StringField(label='Title:')
    content = TextAreaField('Content', [validators.DataRequired()])

class Form(Form):
    course_num = StringField(label='Title:')
    content = TextAreaField('Content', [validators.DataRequired()])

@app.route('/search',methods=['GET','POST'])
def search():
    if  request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = courses.query.filter(courses.num.like(search)).all()
        return render_template('home.html',results = results)

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = PostForm(request.form)
    if request.method == "POST":
        post = reviews(num = form.course_num.data,review=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Your review has been added ','success')
        return redirect(url_for('courses_page'))
    return render_template('add_review.html',form=form)

@app.route('/delete_review/<string:id>', methods=['POST'])
def delete_review(id):
    review = reviews.query.get_or_404(id)
    db.session.delete(review)
    flash('Review Deleted', 'success')
    db.session.commit()
    return redirect(url_for('courses_page'))

@app.route('/course/edit_review/<string:id>', methods=['POST','GET'])
def edit_review(id):
    results = reviews.query.get_or_404(id)
    form = PostForm(request.form)
    form.course_num.data = results.num
    form.content.data = results.review
    if request.method == "POST":
        results.num = form.course_num.data
        results.review = form.content.data
        flash('Review has been updated', 'success')
        db.session.commit()
        return redirect(url_for('courses_page'))
    return render_template('edit_review.html', form=form,results=results)

if __name__ == '__main__':
    app.run(debug=True)