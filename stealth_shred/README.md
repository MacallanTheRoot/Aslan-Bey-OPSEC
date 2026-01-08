<div align="center">
  <a href="#en">🇺🇸 English</a> | <a href="#tr">🇹🇷 Türkçe</a>
</div>

<a name="en"></a>
# 🛡️ ASLAN BEY v2.0
### High-Stakes Metadata Reconstruction & OPSEC Intelligence Tooling

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![Security Status](https://img.shields.io/badge/security-hardened-green?style=for-the-badge&logo=security)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

---

## 🛑 The "Why": The Aslan Bey Strategy

In the arena of high-stakes information warfare, standard "cleaning" is a liability. Conventional tools merely zero out known metadata tags, leaving behind structural artifacts, thumbnails, and version histories that forensic analysts exploit. To simply "delete" is to leave a scar.

**Aslan Bey** employs a strategy of **Total Reconstruction**. We do not scrub files; we redefine their existence. By decoding the payload and rebuilding the container from the ground up, the **Aslan Bey Strategy** ensures that no hidden data structures, incremental updates, or adversarial polyglot payloads survive. We enforce a zero-trust environment for your digital assets.

---

## ⚡ Aslan Bey Core Capabilities

The engine is built on expert-grade defensive libraries to handle files with forensic precision.

| Component | Technology | Defense Logic |
| :--- | :--- | :--- |
| **Deep Image Hygiene** | `Pillow` / `piexif` | **Reconstruction**: Unlike simple strip-tools, we decode the pixel matrix and write a fresh binary stream. Removes EXIF, IPTC, XMP, specific camera serials, and embedded thumbnails. |
| **PDF Flattening** | `pikepdf` | **Anti-Forensic**: Removes "Incremental Updates" (previous edits/versions), XML Metadata, Document Info dictionaries, and PieceInfo. Flattens the file structure to prevent reversion. |
| **Safe Office Scrub** | `defusedxml` | **XXE Hardening**: Parses modern Office (OpenXML) containers safely to strip `docProps/core.xml` (Author, Times) without executing malicious XML entities. |
| **Media Sanitization** | `mutagen` | **Tag Purge**: Aggressively strips ID3 headers (v1/v2), Vorbis comments, and unwanted container atoms from Audio/Video files. |
| **MIME Verification** | `python-magic` | **Anti-Spoofing**: Validates file types via Magic Numbers (binary signatures). A file named `invoice.pdf.exe` or a JPEG hiding a ZIP archive is detected and neutralized. |
| **Secure Shredding** | `DoD 5220.22-M` | **Data Destruction**: When `--force` is used, original files are overwritten with random bit-patterns before deletion to prevent disk recovery. |

---

## 🖥️ Operational Intelligence: The Dashboard

Aslan Bey v2.0 includes a professional GUI for command-level auditing and rapid intelligence assessment.

### 🛡️ Secure Upload Zone
- **Pre-Scan Analysis**: Instantly detects MIME type and assesses "Metadata Exposure Level" (Low/Medium/High) before processing.
- **Rapid Sterilization**: Drag & drop intake with immediate reconstruction and secure download workflow.

### 📊 Real-Time Audit Dashboard
- **Visual Analytics**: Interactive charts showing exactly which metadata categories are being neutralized across your dataset.
- **Live Progress**: Track directory walking and recursive sanitization in real-time.

To launch the dashboard:
```bash
streamlit run stealth_shred/gui_app.py
```

---

## 🔐 The Aslan Bey Doctrine: "Distrust & Verify"

1.  **Distrust Extensions**: Never trust the file extension. `image.jpg` might be an executable. We verify binary signatures.
2.  **Distrust Deletions**: `os.remove()` is insufficient. We overwrite data to defeat magnetic/SSD forensic recovery tools.
3.  **Distrust "Empty"**: An empty tag can still leak information (e.g., software version). We remove the tag structure entirely.

---

## 📦 Installation

Ensure you have a Python 3.8+ environment.

```bash
git clone https://github.com/MacallanTheRoot/aslan-bey.git
cd stealth_shred
pip install -r requirements.txt
```

*(Note: Windows users require `python-magic-bin`, which is handled automatically by our requirements.)*

---

## 🛠️ Usage Examples

### 1. Recursive Strategic Clean (Non-Destructive)
Scans `target_directory`, cleans files, and saves them with `_cleaned` suffix.

```bash
python main.py clean ./confidential_docs --recursive
```

### 2. Force Mode (Destructive Protocol)
**WARNING**: This mode overwrites original files with the sanitized version and securely shreds the source artifacts using DoD standards.

```bash
python main.py clean ./confidential_docs --force
```

### 3. Verbose Intelligence
Useful for verifying specific tag removals or debugging permission issues.

```bash
python main.py clean ./target -v
```

### GUI Usage (Web Interface)
Aslan Bey includes a professional Streamlit-based dashboard.

```bash
venv\Scripts\streamlit run stealth_shred/gui_app.py
```

Features:
- **Dark Mode Dashboard**: Real-time metrics and exposure levels.
- **Drag & Drop**: Secure single-file sanitization.
- **Directory Scanner**: Batch process local folders with visual progress.
- **Audit Visualization**: Interactive charts of removed metadata.

---

## 📋 Audit & Compliance

Aslan Bey generates immutable `JSONL` audit logs for every session, detailing forensic actions taken.

**Log Location**: `logs/stealth_shred_audit_<timestamp>.jsonl`

**Sample Output**:
```json
{
  "timestamp": "2024-01-08T14:02:11",
  "file": "C:\\Data\\Sector_7\\blueprints.pdf",
  "status": "CLEANED",
  "original_size": 2048512,
  "new_size": 1982100,
  "cleaned_fields": [
    "Document Info (Author, Title, etc.)",
    "XMP Metadata",
    "Incremental Updates (History)"
  ]
}
```

---

## ⚠️ Disclaimer

**Aslan Bey** is a defensive tool designed for legitimate privacy protection and OPSEC hardening. The authors are not responsible for data loss due to misuse of the securely shredding features. Always verify cleaned files against your specific threat model.

**Maintained by**: [MacallanTheRoot](https://github.com/MacallanTheRoot)

<br>
<br>
<br>

---

<a name="tr"></a>
# 🛡️ ASLAN BEY v2.0
### Yüksek Riskli Metadata Yeniden Yapılandırma & OPSEC İstihbarat Aracı

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![Security Status](https://img.shields.io/badge/security-hardened-green?style=for-the-badge&logo=security)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

---

## 🛑 Neden?: Aslan Bey Stratejisi

Yüksek riskli bilgi savaşı arenasında, standart "temizleme" araçları birer güvenlik açığıdır. Geleneksel araçlar yalnızca bilinen metadata etiketlerini sıfırlar, ancak adli bilişim analistlerinin istismar edebileceği yapısal artıkları, küçük resimleri (thumbnail) ve sürüm geçmişlerini geride bırakır. Sadece "silmek" iz bırakmaktır.

**Aslan Bey**, **Tam Yeniden Yapılandırma** stratejisini uygular. Dosyaları sadece temizlemeyiz; varlıklarını yeniden tanımlarız. Veri yükünü (payload) çözüp konteyneri sıfırdan inşa ederek, **Aslan Bey Stratejisi** hiçbir gizli veri yapısının, artımlı güncellemenin veya düşman poliglota (polyglot) yüklerinin hayatta kalmamasını sağlar. Dijital varlıklarınız için "sıfır güven" (zero-trust) ortamını zorunlu kılarız.

---

## ⚡ Aslan Bey Temel Yetenekleri

Motor, dosyaları adli hassasiyetle işlemek için uzman düzeyindeki savunma kütüphaneleri üzerine inşa edilmiştir.

| Bileşen | Teknoloji | Savunma Mantığı |
| :--- | :--- | :--- |
| **Derin Görüntü Hijyeni** | `Pillow` / `piexif` | **Yeniden Yapılandırma**: Basit silme araçlarının aksine, piksel matrisini çözer ve yepyeni bir ikili akış (binary stream) yazar. EXIF, IPTC, XMP, kamera seri numaraları ve gömülü küçük resimleri tamamen yok eder. |
| **PDF Düzleştirme** | `pikepdf` | **Anti-Forensic**: "Artımlı Güncellemeleri" (önceki düzenlemeler/sürümler), XML Metadatasını, Belge Bilgi sözlüklerini ve PieceInfo'yu kaldırır. Geri dönüşümü engellemek için dosya yapısını düzleştirir. |
| **Güvenli Ofis Temizliği** | `defusedxml` | **XXE Sertleştirme**: Modern Ofis (OpenXML) konteynerlerini, kötü amaçlı XML varlıklarını çalıştırmadan `docProps/core.xml` (Yazar, Zamanlar) verilerini temizlemek için güvenli bir şekilde ayrıştırır. |
| **Medya Sanitizasyonu** | `mutagen` | **Etiket İmhası**: Ses/Video dosyalarından ID3 başlıklarını (v1/v2), Vorbis yorumlarını ve istenmeyen kapsayıcı atomlarını agresif bir şekilde temizler. |
| **MIME Doğrulaması** | `python-magic` | **Anti-Spoofing**: Dosya türlerini Magic Numbers (ikili imzalar) ile doğrular. `fatura.pdf.exe` adında bir dosya veya içinde ZIP arşivi gizleyen bir JPEG tespit edilir ve etkisiz hale getirilir. |
| **Güvenli İmha** | `DoD 5220.22-M` | **Veri İmhası**: `--force` kullanıldığında, disk kurtarmayı önlemek için orijinal dosyalar silinmeden önce rastgele bit desenleriyle üzerine yazılır. |

---

## 🖥️ Operasyonel İstihbarat: Kontrol Paneli

Aslan Bey v2.0, komut seviyesinde denetim ve hızlı istihbarat değerlendirmesi için profesyonel bir GUI içerir.

### 🛡️ Güvenli Yükleme Bölgesi
- **Ön Tarama Analizi**: İşlemden önce MIME türünü anında tespit eder ve "Metadata Maruziyet Seviyesini" (Düşük/Orta/Yüksek) değerlendirir.
- **Hızlı Sterilizasyon**: Anında yeniden yapılandırma ve güvenli indirme iş akışı ile sürükle-bırak girişi.

### 📊 Gerçek Zamanlı Denetim Panosu
- **Görsel Analitikler**: Veri setinizde hangi metadata kategorilerinin etkisiz hale getirildiğini gösteren etkileşimli grafikler.
- **Canlı İlerleme**: Dizin tarama ve yinelemeli sanitizasyonu gerçek zamanlı olarak izleyin.

Paneli başlatmak için:
```bash
streamlit run stealth_shred/gui_app.py
```

---

## 🔐 Aslan Bey Doktrini: "Güvenme & Doğrula"

1.  **Uzantılara Güvenme**: Dosya uzantısına asla güvenmeyin. `image.jpg` bir çalıştırılabilir dosya olabilir. İkili imzaları doğrularız.
2.  **Silmelere Güvenme**: `os.remove()` yetersizdir. Manyetik/SSD adli kurtarma araçlarını yenmek için verilerin üzerine yazarız.
3.  **"Boş"a Güvenme**: Boş bir etiket bile bilgi sızdırabilir (örn. yazılım sürümü). Etiket yapısını tamamen kaldırırız.

---

## 📦 Kurulum

Python 3.8+ ortamına sahip olduğunuzdan emin olun.

```bash
git clone https://github.com/MacallanTheRoot/aslan-bey.git
cd stealth_shred
pip install -r requirements.txt
```

*(Not: Windows kullanıcıları `python-magic-bin` gerektirir, bu gereksinimlerimiz tarafından otomatik olarak işlenir.)*

---

## 🛠️ Kullanım Örnekleri

### 1. Yinelemeli Stratejik Temizlik (Yıkıcı Olmayan)
`hedef_dizin`i tarar, dosyaları temizler ve `_cleaned` son ekiyle kaydeder.

```bash
python main.py clean ./gizli_belgeler --recursive
```

### 2. Güç Modu (Yıkıcı Protokol)
**UYARI**: Bu mod, orijinal dosyaların üzerine temizlenmiş sürümü yazar ve kaynak kalıntılarını DoD standartlarını kullanarak güvenli bir şekilde imha eder.

```bash
python main.py clean ./gizli_belgeler --force
```

### 3. Ayrıntılı İstihbarat (Verbose)
Belirli etiket kaldırma işlemlerini doğrulamak veya izin sorunlarını ayıklamak için yararlıdır.

```bash
python main.py clean ./hedef -v
```

### GUI Kullanımı (Web Arayüzü)
Aslan Bey, profesyonel bir Streamlit tabanlı kontrol paneli içerir.

```bash
venv\Scripts\streamlit run stealth_shred/gui_app.py
```

Özellikler:
- **Karanlık Mod Paneli**: Gerçek zamanlı metrikler ve maruziyet seviyeleri.
- **Sürükle & Bırak**: Güvenli tek dosya sanitizasyonu.
- **Dizin Tarayıcı**: Yerel klasörleri görsel ilerleme ile toplu işleyin.
- **Denetim Görselleştirme**: Kaldırılan metadataların etkileşimli grafikleri.

---

## 📋 Denetim & Uyumluluk

Aslan Bey, her oturum için alınan adli aksiyonları detaylandıran değiştirilemez `JSONL` denetim günlükleri oluşturur.

**Günlük Konumu**: `logs/stealth_shred_audit_<zaman_damgası>.jsonl`

**Örnek Çıktı**:
```json
{
  "timestamp": "2024-01-08T14:02:11",
  "file": "C:\\Veri\\Bolge_7\\planlar.pdf",
  "status": "CLEANED",
  "original_size": 2048512,
  "new_size": 1982100,
  "cleaned_fields": [
    "Document Info (Author, Title, etc.)",
    "XMP Metadata",
    "Incremental Updates (History)"
  ]
}
```

---

## ⚠️ Yasal Uyarı

**Aslan Bey**, meşru gizlilik koruması ve OPSEC sertleştirme için tasarlanmış savunma amaçlı bir araçtır. Yazarlar, güvenli imha özelliklerinin yanlış kullanımı nedeniyle oluşacak veri kayıplarından sorumlu değildir. Temizlenmiş dosyaları her zaman kendi tehdit modelinize göre doğrulayın.

**Geliştirici**: [MacallanTheRoot](https://github.com/MacallanTheRoot)
