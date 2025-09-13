import secrets
import webbrowser
import cohere
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# ------------------- App setup -------------------
app = Flask(__name__, template_folder="templates")
app.secret_key = secrets.token_hex(16)


# ------------------- Form ------------------------
class CommandForm(FlaskForm):
    text = StringField("Enter text or speak", validators=[DataRequired()])
    submit = SubmitField("Submit")


# ------------------- Command handler -------------
def handle_command(text):
    """Decide an action based on the user input."""
    t = text.lower().strip()

    # ---- YouTube ----
    if "youtube" in t or "play" in t:
        song = (
            t.replace("play", "")
            .replace("on youtube", "")
            .replace("youtube", "")
            .strip()
        )
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return f"Playing {song} on YouTube"

    # ---- GitHub ----
    if "github" in t:
        webbrowser.open("https://github.com/Abhinav1901498")
        return "Opening GitHub profile"

    # ---- LinkedIn ----
    if "linkedin" in t:
        webbrowser.open("https://linkedin.com/in/abhinav-pandey-b499532b5")
        return "Opening LinkedIn profile"

    # ---- WhatsApp ----
    if "whatsapp" in t and "open" in t:
        webbrowser.open("https://wa.me/")
        return "Opening WhatsApp Web"

    if "whatsapp" in t and "message" in t:
        number = "919580363258"  # include country code
        msg = "Hello from my Flask app!"
        webbrowser.open(f"https://web.whatsapp.com/send?phone={number}&text={msg}")
        return f"Opening WhatsApp chat with {number}"

    # ---- E-commerce sites ----
    sites = {
        "flipkart": "https://www.flipkart.com/",
        "amazon": "https://www.amazon.in/",
        "myntra": "https://www.myntra.com/",
        "meesho": "https://www.meesho.com/",
    }
    if "open" in t:
        name = t.replace("open", "").strip()
        if name in sites:
            webbrowser.open_new_tab(sites[name])
            return f"Opening {name} in a new tab"
        return "Sorry, I can only open Flipkart, Amazon, Myntra, or Meesho."

    return None


# ------------------- Routes ----------------------
@app.route("/", methods=["GET", "POST"])
def home():
    form = CommandForm()
    output = None

    if form.validate_on_submit():
        user_text = form.text.data
        output = handle_command(user_text)

        # fallback to Cohere chatbot if nothing matched
        if not output:
            co = cohere.Client("QXVbgP0ZfNgeofnSRsQYMoXyB1LcHsPt7toOeEZg")
            resp = co.chat(model="command-nightly", message=user_text, max_tokens=250)
            output = resp.text

    return render_template("home.html", form=form, output=output)


# ------------------- Run app ---------------------
if __name__ == "__main__":
    app.run(debug=True)
