import json
import time
import logging
import argparse

from get_token import get_token
from get_loop import get_loop

# Interface de linha de comando
parser = argparse.ArgumentParser(description="Desafio de Loop")
parser.add_argument("-m", "--max-iteracoes", type=int, help="número máximo de iterações (se omitido, o script pergunta)")
parser.add_argument("--margem", type=float, default=0.2, help="segundos somados à espera para não chegar cedo demais (padrão: 0.2)")
parser.add_argument("--tentativas", type=int, default=3, help="novas tentativas quando a rede falha (padrão: 3)")
parser.add_argument("-v", "--verbose", action="store_true", help="mostra as mensagens de debug")
args = parser.parse_args()

logging.basicConfig(
  level=logging.DEBUG if args.verbose else logging.INFO,
  format="{asctime} [{levelname}] {message}",
  style="{",
  datefmt="%H:%M:%S",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)

token = get_token()

print("=" * 30)
print("Início do desafio de Loop!")
print("=" * 30 + "\n")

max_interation = args.max_iteracoes

if max_interation is None:
  print("Por favor, informe o número máximo de interações: ")

  while True:
    try:
      max_interation = int(input())
    except ValueError:
      print("\nPor favor, digite um número válido para começarmos o desafio!")
      continue

    if max_interation <= 1:
      print("\nPor favor, digite um número maior que um!")
      continue

    break


while True:
  response, latency = get_loop(token, max_interation, args.tentativas)

  data = json.loads(response)

  progress = data.get("progress")
  status = data.get("status")
  message = data.get("message")

  if status == "START" or status == "CONTINUE":
    nextWaitTimeInSeconds = int(data.get("nextWaitTimeInSeconds"))

    sleep_time = round(max(0, nextWaitTimeInSeconds - latency + args.margem), 3)

    logging.info(f"[{status}] {message} (progresso: {progress})")
    logging.info(f"Latência: {latency}s | espera pedida: {nextWaitTimeInSeconds}s | espera real: {sleep_time}s")

    time.sleep(sleep_time)
    continue
  else:
    logging.info(f"[{status}] {message}")
    break
