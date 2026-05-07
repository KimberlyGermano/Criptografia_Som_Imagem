import wave
import numpy as np
import hashlib


def gerar_chave(senha, tamanho, unsigned_dtype):
    hash_senha = hashlib.sha256(senha.encode()).digest()
    seed = int.from_bytes(hash_senha[:8], "little")
    rng = np.random.default_rng(seed)

    chave = rng.integers(
        low=0,
        high=np.iinfo(unsigned_dtype).max,
        size=tamanho,
        dtype=unsigned_dtype
    )

    return chave


def analisar_frequencia_audio(caminho_audio):
    with wave.open(caminho_audio, "rb") as audio:
        n_channels = audio.getnchannels()
        sampwidth = audio.getsampwidth()
        framerate = audio.getframerate()
        n_frames = audio.getnframes()
        frames = audio.readframes(n_frames)

    if sampwidth == 1:
        dtype = np.uint8
    elif sampwidth == 2:
        dtype = np.int16
    else:
        raise ValueError("Use WAV de 8 ou 16 bits.")

    dados = np.frombuffer(frames, dtype=dtype).copy()

    if n_channels > 1:
        dados = dados.reshape(-1, n_channels)
        dados = dados.mean(axis=1)

    dados = dados - np.mean(dados)

    fft = np.fft.fft(dados)
    frequencias = np.fft.fftfreq(len(dados), d=1 / framerate)

    magnitudes = np.abs(fft)

    metade = len(frequencias) // 2
    frequencias_positivas = frequencias[:metade]
    magnitudes_positivas = magnitudes[:metade]

    indice_pico = np.argmax(magnitudes_positivas)
    frequencia_dominante = frequencias_positivas[indice_pico]

    return round(float(frequencia_dominante), 2)


def criptografar_audio(caminho_entrada, caminho_saida, senha):
    with wave.open(caminho_entrada, "rb") as audio:
        n_channels = audio.getnchannels()
        sampwidth = audio.getsampwidth()
        framerate = audio.getframerate()
        n_frames = audio.getnframes()
        frames = audio.readframes(n_frames)

    if sampwidth == 1:
        dtype = np.uint8
        unsigned_dtype = np.uint8
    elif sampwidth == 2:
        dtype = np.int16
        unsigned_dtype = np.uint16
    else:
        raise ValueError("Use WAV de 8 ou 16 bits.")

    dados = np.frombuffer(frames, dtype=dtype).copy()

    dados_frames = dados.reshape(-1, n_channels)
    dados_invertidos = np.flipud(dados_frames).reshape(-1)

    dados_unsigned = dados_invertidos.view(unsigned_dtype)

    chave = gerar_chave(senha, len(dados_unsigned), unsigned_dtype)

    dados_codificados_unsigned = np.bitwise_xor(dados_unsigned, chave)
    dados_codificados = dados_codificados_unsigned.view(dtype)

    with wave.open(caminho_saida, "wb") as audio_out:
        audio_out.setnchannels(n_channels)
        audio_out.setsampwidth(sampwidth)
        audio_out.setframerate(framerate)
        audio_out.writeframes(dados_codificados.tobytes())


def descriptografar_audio(caminho_entrada, caminho_saida, senha):
    with wave.open(caminho_entrada, "rb") as audio:
        n_channels = audio.getnchannels()
        sampwidth = audio.getsampwidth()
        framerate = audio.getframerate()
        n_frames = audio.getnframes()
        frames = audio.readframes(n_frames)

    if sampwidth == 1:
        dtype = np.uint8
        unsigned_dtype = np.uint8
    elif sampwidth == 2:
        dtype = np.int16
        unsigned_dtype = np.uint16
    else:
        raise ValueError("Use WAV de 8 ou 16 bits.")

    dados_codificados = np.frombuffer(frames, dtype=dtype).copy()

    dados_unsigned = dados_codificados.view(unsigned_dtype)

    chave = gerar_chave(senha, len(dados_unsigned), unsigned_dtype)

    dados_invertidos_unsigned = np.bitwise_xor(dados_unsigned, chave)
    dados_invertidos = dados_invertidos_unsigned.view(dtype)

    dados_frames = dados_invertidos.reshape(-1, n_channels)
    dados_recuperados = np.flipud(dados_frames).reshape(-1)

    with wave.open(caminho_saida, "wb") as audio_rec:
        audio_rec.setnchannels(n_channels)
        audio_rec.setsampwidth(sampwidth)
        audio_rec.setframerate(framerate)
        audio_rec.writeframes(dados_recuperados.tobytes())