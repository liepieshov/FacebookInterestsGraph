from flask import Flask, render_template
app = Flask(__name__, static_folder="", template_folder="")

@app.route('/contacts')
def contacts():
    return app.send_static_file("contacts.html")
@app.route('/<path:path>')
def static_file(path):
    if path.endswith("chart"):
        return main(path)
    return app.send_static_file(path)


def main(chart):
    return render_template("index.html", conf=chart + "config.json")


@app.route("/")
def menu():
    return app.send_static_file("menu.html")


if __name__ == "__main__":
    app.run(debug=True)
