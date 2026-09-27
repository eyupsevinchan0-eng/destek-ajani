# Destek Ajanı

Anthropic Claude API ile geliştirilmiş, VDS/hosting/domain müşteri desteği verebilen, araç
kullanabilen (tool use) bir yapay zeka ajanı. Terminalden veya Telegram üzerinden (telefondan)
kullanılabilir.

## Özellikler

- **Doğal dilde araç kullanımı**: Claude, kullanıcının isteğine göre gerekli fonksiyonları
  kendisi seçip çalıştırır ve sonuçları birden fazla adımda zincirleyebilir.
- **Sunucu yönetimi**: Proxmox VDS panelindeki bir sunucunun durumunu, kaynak kullanımını
  (CPU/RAM/disk/ağ) ve loglarını sorgulayabilir, başlatıp durdurabilir.
- **Destek talebi (ticket) sistemi**: Müşteri bir sorun bildirdiğinde SQLite veritabanına
  otomatik kayıt açılır, durumu (açık/işlemde/kapalı) takip edilebilir.
- **Otomatik şirket bildirimi**: Yeni bir talep açıldığında yöneticiye Telegram üzerinden
  anında bildirim gider.
- **Yetkilendirme**: Sunucu başlatma/durdurma gibi kritik işlemler sadece admin tarafından
  yapılabilir; yetkisiz denemeler engellenip yöneticiye bildirilir.
- **Kalıcı hafıza**: Konuşma geçmişi dosyaya kaydedilir, program yeniden başlasa bile
  konuşmanın bağlamı korunur.
- **Hız sınırlama**: Kişi başı dakikada belirli sayıda mesajla sınırlandırılarak kötüye
  kullanım ve gereksiz API maliyeti önlenir.
- **7/24 çalışma**: Telegram botu bir VPS üzerinde systemd servisi olarak çalışır, yeniden
  başlatılsa bile otomatik ayağa kalkar.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `ajan1.py`, `ajan2.py` | Öğrenme sürecindeki ilk, basit ajan denemeleri |
| `ajan3.py` | Terminalden çalışan tam özellikli destek ajanı |
| `ajan_telefon.py` | Aynı ajanın Telegram (telefon) üzerinden çalışan sürümü |
| `test_ajan.py` | pytest ile yazılmış otomatik testler |

## Kurulum

```bash
pip install -r requirements.txt
```

Proje kök dizininde bir `.env` dosyası oluşturup şunları doldurun:

```
ANTHROPIC_API_KEY=...
TELEGRAM_BOT_TOKEN=...   # sadece ajan_telefon.py icin gerekli
PVE_TOKEN=...            # sadece Proxmox araclarini kullanacaksaniz gerekli
```

## Çalıştırma

```bash
python ajan3.py           # terminalden sohbet
python ajan_telefon.py    # Telegram botu olarak calistir
```

## Test

```bash
python -m pytest test_ajan.py -v
```

## Mimari notu

`ajan_telefon.py`, 7/24 çalışacak şekilde bir VPS'te systemd servisi olarak barındırılır.
Proxmox tabanlı sunucu araçları (`sunucu_durumu`,
`sunucu_baslat` vb.) yerel ağdaki bir eğitim panelini hedeflediği için, bot VPS'ten
çalıştığında bu araçlar yalnızca ilgili panel de erişilebilir olduğunda gerçek veri döner;
aksi halde hatayı düzgün şekilde bildirip çökmeden devam eder.
