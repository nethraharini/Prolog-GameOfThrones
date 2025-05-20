from flask import Flask, render_template, request
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()
prolog.consult("./got.pl")  # Make sure it's in the same directory

def get_character_info(name):
    info = {}
    name = name.lower().strip()

    # Parents
    parents = list(prolog.query(f"parent(X, {name})"))
    info['parents'] = [p['X'] for p in parents] if parents else []

    # Gender
    if list(prolog.query(f"male({name})")):
        info['gender'] = "Male"
    elif list(prolog.query(f"female({name})")):
        info['gender'] = "Female"
    else:
        info['gender'] = "Unknown"

    # Status
    status = list(prolog.query(f"status({name}, X)"))
    info['status'] = status[0]['X'].capitalize() if status else "Unknown"

    # concubine
    info['concubine'] = "Yes" if list(prolog.query(f"concubine({name})")) else "No"

    return info

@app.route("/", methods=["GET", "POST"])
def index():
    character_info = None
    if request.method == "POST":
        name = request.form["name"]
        character_info = get_character_info(name)
    return render_template("index.html", info=character_info)

if __name__ == "__main__":
    app.run(debug=True)
