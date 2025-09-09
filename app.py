import cohere
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__, template_folder="templates")
app.secret_key = secrets.token_hex(16)

class Form(FlaskForm):
    text = StringField('Enter text', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET", "POST"])
def home():
    form = Form()
    co = cohere.Client("KKqmDXDL2DbcbKQGmUDvUO2dKWRiAmRp0jFwMUmq")  # अपनी Cohere API key यहाँ डालें
    output = None

    if form.validate_on_submit():
        user_input = form.text.data
        response = co.chat(
            model="command-nightly",
            message=user_input,  # एकल संदेश
            max_tokens=300,
            temperature=0.9
        )
        output = response.text  # उत्तर का टेक्स्ट प्राप्त करें
    return render_template("home.html", form=form, output=output)

if __name__ == "__main__":
    app.run(debug=True)
