from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    question = TextField('Question', validators=[validators.required()])



@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        question=request.form['question']
        print(question)

        if form.validate():
            # Save the comment here.
            flash(question)
			return redirect(url_for('success', question=question));

        else:
            flash('Error: All the form fields are required. ')

    return render_template('hello.html', form=form)


@app.route("/process", methods=['GET', 'POST'])
def success(question):
	if request.method == 'GET':
		print("Here was the question : " + question)

	return render_template('process.html', question=question);

if __name__ == "__main__":
    app.run()
