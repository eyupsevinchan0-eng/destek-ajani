import sys
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

gecmis = []

while True:
    kullanici_mesaji = input("Sen: ")
    if kullanici_mesaji == "çık":
        break

    gecmis.append({"role": "user", "content": kullanici_mesaji})

    cevap = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        messages=gecmis
    )

    claude_cevabi = ""
    for parca in cevap.content:
        if parca.type == "text":
            claude_cevabi += parca.text

    print("Claude:", claude_cevabi)

    gecmis.append({"role": "assistant", "content": claude_cevabi})
