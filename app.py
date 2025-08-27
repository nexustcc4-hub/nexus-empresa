from flask import Flask, render_template, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

app = Flask(__name__)

# 👉 Substitua pelo seu CLIENT_ID do Google
CLIENT_ID = "SEU_CLIENT_ID_DO_GOOGLE"

@app.route('/', methods=['GET', 'POST'])
def entrar():
    return render_template('Entrar.html')

@app.route('/continuarGoogle', methods=['GET', 'POST'])
def continuarGoogle():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Aqui entraria a lógica de login tradicional
        return render_template('continuarGoogle.html', email=email, senha=senha)
    return render_template('Index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Aqui entraria a lógica de cadastro no banco
        return render_template('cadastro.html', email=email, senha=senha)
    return render_template('Cadastro.html')

# 🚀 Nova rota para validar login com Google
@app.route('/auth/google', methods=['POST'])
def auth_google():
    try:
        token = request.json.get("token")
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)

        return jsonify({
            "status": "success",
            "user": {
                "name": idinfo.get("name"),
                "email": idinfo.get("email"),
                "picture": idinfo.get("picture")
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
