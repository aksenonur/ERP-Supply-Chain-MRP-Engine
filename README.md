![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20SQL-green?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed%20PoC-orange?style=for-the-badge)
# ERP Supply Chain & Material Requirements Planning (MRP) Engine

## Proje Kapsamı ve Kurumsal Mimari
Karmaşık savunma sanayii ve imalat ERP projelerinde en kritik süreçlerden biri, nihai ürün talebine karşılık alt bileşenlerin, hammaddelerin ve yarı mamullerin zamanında ve doğru miktarda tedarik edilmesidir.

Bu proje; kurumsal bir ERP sisteminde **Ürün Ağacı (Bill of Materials - BOM)** hiyerarşisini ayrıştıran (BOM Explosion) ve mevcut stok seviyelerini düşerek net malzeme ihtiyacını hesaplayan bir **Material Requirements Planning (MRP) Engine** çalışmasıdır.

### Öne Çıkan ERP Özellikleri
- **Multi-Level BOM Explosion:** Ana mamulden (Örn: İHA / Zırhlı Araç) başlayıp en alt hammaddeye kadar inen çok kademeli ürün ağacı çözümlemesi.
- **Net Requirement Calculation:** Brüt ihtiyaçtan eldeki stok (On-Hand) ve yoldaki siparişleri (On-Order) düşerek net eksiği hesaplama.
- **Automated Purchase Requisitions:** Stok açığı oluşan parçalar için tedarik sürelerini (Lead Time) dikkate alarak otomatik Satın Alma Talebi (PR) oluşturma.
- **Inventory Ledger Ingestion:** Üretim planlama sonuçlarının ERP SQLite veritabanı şemasına aktarımı.

### Kullanılan Teknolojiler
- **Dil:** Python 3.x
- **Kütüphaneler:** Pandas, JSON, Logging, SQLite
