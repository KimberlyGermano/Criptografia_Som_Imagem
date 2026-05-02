from PIL import Image
import numpy as np
import hashlib


def gerar_chave_imagem(senha, tamanho):
    hash_senha = hashlib.sha256(senha.encode()).digest()
    seed = int.from_bytes(hash_senha[:8], "little")
    rng = np.random.default_rng(seed)

    chave = rng.integers(
        low=0,
        high=256,
        size=tamanho,
        dtype=np.uint8
    )

    return chave


def criptografar_imagem(caminho_entrada, caminho_saida, senha):
    imagem = Image.open(caminho_entrada).convert("RGB")
    dados = np.array(imagem, dtype=np.uint8)

    altura, largura, canais = dados.shape

    # Inverte a imagem verticalmente
    dados_invertidos = np.flipud(dados)

    dados_flat = dados_invertidos.flatten()

    chave = gerar_chave_imagem(senha, len(dados_flat))

    dados_codificados_flat = np.bitwise_xor(dados_flat, chave)

    dados_codificados = dados_codificados_flat.reshape((altura, largura, canais))

    imagem_codificada = Image.fromarray(dados_codificados.astype(np.uint8), "RGB")
    imagem_codificada.save(caminho_saida)


def descriptografar_imagem(caminho_entrada, caminho_saida, senha):
    imagem = Image.open(caminho_entrada).convert("RGB")
    dados_codificados = np.array(imagem, dtype=np.uint8)

    altura, largura, canais = dados_codificados.shape

    dados_flat = dados_codificados.flatten()

    chave = gerar_chave_imagem(senha, len(dados_flat))

    dados_decodificados_flat = np.bitwise_xor(dados_flat, chave)

    dados_decodificados = dados_decodificados_flat.reshape((altura, largura, canais))

    # Desfaz a inversão vertical
    dados_recuperados = np.flipud(dados_decodificados)

    imagem_recuperada = Image.fromarray(dados_recuperados.astype(np.uint8), "RGB")
    imagem_recuperada.save(caminho_saida)