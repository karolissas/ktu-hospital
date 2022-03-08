from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Pagrindinis puslapis"

@app.route("/prisijungimas")
def login():
    return "Prisijungimo puslapis"

@app.route("/registracija")
def register():
    return "Registracijos puslapis"

@app.route("/manopaskyra")
def logged_in():
    return "Kliento paskyros puslapis"

@app.route("/evaldzia")
def gov_gateway():
    return "Elektroniniai valdžios vartai"

if __name__ == "__main__":
    app.run()