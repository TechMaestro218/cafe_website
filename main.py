import pprint
from flask import Flask, render_template,url_for,flash,redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import URL
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location (Google Map URL)', validators=[DataRequired(),URL()])
    opening_time = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating',choices=["✘","☕️","☕️☕️","☕️☕️☕️","☕️☕️☕️☕️","☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi_rating = SelectField(label='Wifi Strength',choices=["✘","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"], validators=[DataRequired()])
    power_socket = SelectField(label='Power Socket Availability',choices=["✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField(id="form_submit_button",label='Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Process form submission
        with open('cafe-data.csv', mode="a", newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([form.cafe.data, form.location.data, form.opening_time.data, form.closing_time.data,
                                 form.coffee_rating.data, form.wifi_rating.data, form.power_socket.data+"\n"])
        flash("Cafe added successfully", "success")
        # Redirect back to the add_cafe route to clear the form fields
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv',mode="r", newline='',encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(len(list_of_rows))
        pprint.pprint(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
