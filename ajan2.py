import sys
sys.stdout.reconfigure(encoding="utf-8")

import random
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

def toplama_yap(a, b):
    return a + b

def zar_at():
    return random.randint(1, 6)

def not_al(icerik):
    with open("notlar.txt", "a", encoding="utf-8") as f:
        f.write(icerik + "\n")
    return "Not kaydedildi."

def notlari_oku():
    try:
        with open("notlar.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Hiç not yok."

araclar = [
    {
        "name": "toplama_yap",
        "description": "Iki sayiyi toplar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "zar_at",
        "description": "1 ile 6 arasinda rastgele bir zar atar.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "not_al",
        "description": "Bir notu dosyaya kalici olarak kaydeder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "icerik": {"type": "string"}
            },
            "required": ["icerik"]
        }
    },
    {
        "name": "notlari_oku",
        "description": "Daha once kaydedilmis tum notlari okur.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

def araci_calistir(isim, girdi):
    if isim == "toplama_yap":
        return toplama_yap(girdi["a"], girdi["b"])
    if isim == "zar_at":
        return zar_at()
    if isim == "not_al":
        return not_al(girdi["icerik"])
    if isim == "notlari_oku":
        return notlari_oku()

mesajlar = [{"role": "user", "content": "Notlarımda ne var?"}]


cevap = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=500,
    tools=araclar,
    messages=mesajlar
)

for parca in cevap.content:
    if parca.type == "tool_use":
        sonuc = araci_calistir(parca.name, parca.input)
        print("Python çalıştı:", parca.name, "->", sonuc)

        mesajlar.append({"role": "assistant", "content": cevap.content})
        mesajlar.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": parca.id, "content": str(sonuc)}]
        })

        son_cevap = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=500,
            tools=araclar,
            messages=mesajlar
        )
        print("Claude:", son_cevap.content[0].text)
