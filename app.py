from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from audio_process import criptografar_audio, descriptografar_audio
from email_sender import enviar_email
from image_process import criptografar_imagem, descriptografar_imagem

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/criptografar-audio", methods=["POST"])
def criptografar_audio_rota():
    arquivo = request.files["audio"]
    senha_audio = request.form["senha_audio"]

    email_remetente = request.form.get("email_remetente")
    senha_email = request.form.get("senha_email")
    email_destinatario = request.form.get("email_destinatario")

    nome_seguro = secure_filename(arquivo.filename)
    caminho_entrada = os.path.join(UPLOAD_FOLDER, nome_seguro)
    caminho_saida = os.path.join(OUTPUT_FOLDER, "audio_codificado.wav")

    arquivo.save(caminho_entrada)

    criptografar_audio(caminho_entrada, caminho_saida, senha_audio)

    if email_remetente and senha_email and email_destinatario:
        enviar_email(
            email_remetente,
            senha_email,
            email_destinatario,
            caminho_saida
        )

    return send_file(caminho_saida, as_attachment=True)


@app.route("/descriptografar-audio", methods=["POST"])
def descriptografar_audio_rota():
    arquivo = request.files["audio"]
    senha_audio = request.form["senha_audio"]

    nome_seguro = secure_filename(arquivo.filename)
    caminho_entrada = os.path.join(UPLOAD_FOLDER, nome_seguro)
    caminho_saida = os.path.join(OUTPUT_FOLDER, "audio_recuperado.wav")

    arquivo.save(caminho_entrada)

    descriptografar_audio(caminho_entrada, caminho_saida, senha_audio)

    return send_file(caminho_saida, as_attachment=True)

@app.route("/criptografar-imagem", methods=["POST"])
def criptografar_imagem_rota():
    arquivo = request.files["imagem"]
    senha_imagem = request.form["senha_imagem"]

    email_remetente = request.form.get("email_remetente")
    senha_email = request.form.get("senha_email")
    email_destinatario = request.form.get("email_destinatario")

    nome_seguro = secure_filename(arquivo.filename)
    caminho_entrada = os.path.join(UPLOAD_FOLDER, nome_seguro)
    caminho_saida = os.path.join(OUTPUT_FOLDER, "imagem_codificada.png")

    arquivo.save(caminho_entrada)

    criptografar_imagem(caminho_entrada, caminho_saida, senha_imagem)

    if email_remetente and senha_email and email_destinatario:
        enviar_email(
            email_remetente,
            senha_email,
            email_destinatario,
            caminho_saida
        )

    return send_file(caminho_saida, as_attachment=True)


@app.route("/descriptografar-imagem", methods=["POST"])
def descriptografar_imagem_rota():
    arquivo = request.files["imagem"]
    senha_imagem = request.form["senha_imagem"]

    nome_seguro = secure_filename(arquivo.filename)
    caminho_entrada = os.path.join(UPLOAD_FOLDER, nome_seguro)
    caminho_saida = os.path.join(OUTPUT_FOLDER, "imagem_recuperada.png")

    arquivo.save(caminho_entrada)

    descriptografar_imagem(caminho_entrada, caminho_saida, senha_imagem)

    return send_file(caminho_saida, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)