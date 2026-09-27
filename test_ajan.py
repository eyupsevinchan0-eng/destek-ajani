import ajan3


def test_toplama_yap():
    assert ajan3.toplama_yap(2, 3) == 5
    assert ajan3.toplama_yap(-1, 1) == 0


def test_zar_at_araligi():
    for _ in range(50):
        sonuc = ajan3.zar_at()
        assert 1 <= sonuc <= 6


def test_hesapla_dort_islem():
    assert ajan3.hesapla("topla", 2, 3) == 5
    assert ajan3.hesapla("cikar", 5, 2) == 3
    assert ajan3.hesapla("carp", 4, 3) == 12
    assert ajan3.hesapla("bol", 10, 2) == 5


def test_hesapla_sifira_bolme():
    assert ajan3.hesapla("bol", 5, 0) == "Sıfıra bölünemez."


def test_hesapla_bilinmeyen_islem():
    assert ajan3.hesapla("kokalma", 1, 2) == "Bilinmeyen işlem."


def test_sadelestir_turkce_karakterler():
    assert ajan3._sadelestir("AÇIK") == "acik"
    assert ajan3._sadelestir("Kapalı") == "kapali"
    assert ajan3._sadelestir("acik") == ajan3._sadelestir("AÇIK")


def test_talep_olustur_ve_listele():
    sonuc = ajan3.talep_olustur("Test Musteri", "Test sorunu - pytest")
    assert "olusturuldu" in sonuc

    liste = ajan3.talepleri_listele()
    assert "Test Musteri" in liste

    import re
    talep_id = int(re.search(r"#(\d+)", sonuc).group(1))
    ajan3.talep_durumu_guncelle(talep_id, "kapali")

    kapali_liste = ajan3.talepleri_listele("kapali")
    assert f"#{talep_id}" in kapali_liste


def test_talep_durumu_guncelle_olmayan_talep():
    sonuc = ajan3.talep_durumu_guncelle(999999, "kapali")
    assert "bulunamadi" in sonuc


def test_yetkilendirme_kritik_arac_engellenir():
    sonuc = ajan3.araci_calistir("sunucu_baslat", {"vmid": 100}, yetkili=False)
    assert "yetkili" in sonuc.lower()


def test_yetkilendirme_zararsiz_arac_engellenmez():
    sonuc = ajan3.araci_calistir("toplama_yap", {"a": 2, "b": 2}, yetkili=False)
    assert sonuc == 4
