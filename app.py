from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = "clau_secreta_per_flash"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url.startswith("http"):
            flash("La URL no és vàlida. Ha de començar amb http o https.", "error")
            return redirect(url_for('index'))

        try:
            # Executem el crawler i li passem la URL com a argument
            subprocess.run(["python", "crawler.py", url], check=True)
            flash("Exploració completada correctament! Revisa l’arxiu errors.csv.", "success")
        except subprocess.CalledProcessError:
            flash("Hi ha hagut un error durant l'execució del crawler.", "error")

    return render_template("index.html")
