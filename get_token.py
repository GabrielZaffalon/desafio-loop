import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


def get_token():

    print("Fazendo login do usuário.\n")

    base = os.getenv("BASE")
    limit_time = os.getenv("LIMIT_TIME")
    email = os.getenv("API_EMAIL")
    password = os.getenv("API_SENHA")
    missing = [nome for nome, value in [("BASE", base), ("LIMIT_TIME", limit_time), ("API_EMAIL", email), ("API_SENHA", password)] if not value]
    if missing:
        print("Erro: defina " + " e ".join(missing) + " no .env antes de executar.\n")
        sys.exit(1)

    try:
        limit_time = float(limit_time)
    except ValueError:
        print(f"Erro: LIMIT_TIME deve ser um número (recebido: {limit_time!r}).\n")
        sys.exit(1)

    credentials = {"email": email, "password": password}
    response = requests.post(f"{base}/auth/login", json=credentials, timeout=limit_time)
    response.raise_for_status()

    data = response.json()
    token = data["token"]

    print("Login feito com sucesso!\n")
    return token
