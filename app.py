import cohere
import webbrowser
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__, template_folder="templates")
app.secret_key = secrets.token_hex(16)

# ---- WTForms ----
class CommandForm(FlaskForm):
    text = StringField("Enter text or speak", validators=[DataRequired()])
    submit = SubmitField("Submit")

def handle_command(text):
    """Decide action for user text"""
    text_l = text.lower().strip()

    # --- YouTube ---
    if "youtube" in text_l:
        song = text_l.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return f"Playing {song} on YouTube"

    # --- GitHub ---
    if "github" in text_l:
        webbrowser.open("https://github.com/Abhinav1901498")
        return "Opening GitHub profile"

    # --- LinkedIn ---
    if "linkedin" in text_l:
        webbrowser.open("https://linkedin.com/in/abhinav-pandey-b499532b5")
        return "Opening LinkedIn"

    # --- WhatsApp Web (open only) ---
    if "whatsapp" in text_l and "open" in text_l:
        webbrowser.open("https://wa.me/")
        return "Opening WhatsApp Web"

    # --- WhatsApp send message ---
    if "whatsapp" in text_l and "message" in text_l:
        number = "9580363258"  # ← अपना नंबर डालें (country code के साथ)
        message = "Hello from my Flask app!"
        url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        webbrowser.open(url)
        return f"Opening WhatsApp chat with {number}"

    # --- Dynamic e-commerce sites ---
    allowed_sites = {
        "flipkart": "https://www.flipkart.com/",
        "amazon": "https://www.amazon.com/",
        "myntra": "https://www.myntra.com/",
        "meesho": "https://www.meesho.com/"
    }

    if "open" in text_l:
        site_name = text_l.replace("open", "").strip().lower()
        if site_name in allowed_sites:
            url = allowed_sites[site_name]
            webbrowser.open_new_tab(url)
            return f"Opening {site_name} in a new tab: {url}"
        else:
            return "Sorry, I can only open Flipkart, Amazon, Myntra, or Meesho."

    return None

@app.route("/", methods=["GET", "POST"])
def home():
    form = CommandForm()
    output = None

    if form.validate_on_submit():
        user_text = form.text.data
        output = handle_command(user_text)

        # Fallback: Cohere chatbot
        if not output:
            co = cohere.Client("KKqmDXDL2DbcbKQGmUDvUO2dKWRiAmRp0jFwMUmq")
            resp = co.chat(model="command-nightly", message=user_text, max_tokens=250)
            output = resp.text

    return render_template("home.html", form=form, output=output)


if __name__ == "__main__":
    app.run(debug=True)
