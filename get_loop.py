import os
import sys
import time
import logging
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_loop(token, interations, retries=3):

  base = os.getenv("BASE")
  missing = [nome for nome, value in [("BASE", base)] if not value]
  if missing:
      print("Erro: defina " + " e ".join(missing) + " no .env antes de executar.\n")
      sys.exit(1)

  limit_time = float(os.getenv("LIMIT_TIME", 10))

  url = f"{base}/challenges/loop"

  payload = json.dumps({
    "maxIterations": interations
  })
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }

  attempt = 1

  while True:
    start = time.monotonic()

    try:
      response = requests.request("POST", url, headers=headers, data=payload, timeout=limit_time)
      break
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
      logging.warning(f"Falha de rede na tentativa {attempt} de {retries + 1}: {error}")

    if attempt > retries:
      logging.error("Limite de tentativas atingido. Encerrando.")
      sys.exit(1)

    attempt += 1
    time.sleep(1)

  latency = round(time.monotonic() - start, 3)

  logging.debug(f"HTTP {response.status_code} em {latency}s: {response.text}")

  return response.text, latency
