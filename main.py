import json
import sqlite3
import logging
import pandas as pd

# Log Yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ERPMRPEngine:
    def __init__(self, data_file='bom_and_inventory.json', db_path='erp_mrp.db'):
        self.data_file = data_file
        self.db_path = db_path

    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def run_mrp_calculation(self, target_product_code, demand_quantity):
        logging.info(f"MRP Hesaplaması Başlatıldı: Target Product={target_product_code}, Demand Qty={demand_quantity}")
        data = self.load_data()
        
        # 1. Ürünü Bul
        product = next((p for p in data['products'] if p['product_code'] == target_product_code), None)
        if not product:
            logging.error(f"HATA: Ürün Kodu '{target_product_code}' ERP Ürün Ağacında (BOM) Bulunamadı!")
            return

        inventory = data['inventory']
        purchase_requisitions = []

        # 2. BOM Explosion ve Stok Düşümü (Gross to Net Requirements)
        for item in product['bom']:
            code = item['component_code']
            qty_needed_per_unit = item['qty_per_unit']
            gross_requirement = qty_needed_per_unit * demand_quantity
            
            inv_info = inventory.get(code, {"on_hand": 0, "lead_time_days": 7, "unit_cost": 0.0})
            on_hand = inv_info['on_hand']
            
            # Net İhtiyaç Hesaplama
            net_requirement = gross_requirement - on_hand

            if net_requirement > 0:
                total_cost = net_requirement * inv_info['unit_cost']
                logging.warning(
                    f"STOK AÇIĞI TESPİT EDİLDİ [{code} - {item['description']}]: "
                    f"Brüt İhtiyaç: {gross_requirement} | Stok: {on_hand} | Net İhtiyaç: {net_requirement}"
                )
                
                purchase_requisitions.append({
                    'pr_number': f"PR-MRP-{code}",
                    'component_code': code,
                    'description': item['description'],
                    'required_qty': net_requirement,
                    'estimated_unit_cost': inv_info['unit_cost'],
                    'total_estimated_cost': total_cost,
                    'lead_time_days': inv_info['lead_time_days'],
                    'status': 'REQUISITION_GENERATED'
                })
            else:
                logging.info(
                    f"STOK YETERLİ [{code} - {item['description']}]: "
                    f"Brüt İhtiyaç: {gross_requirement} | Stok: {on_hand} (Satın alma gerekmiyor)."
                )

        # 3. Sonuçları Veritabanına Yaz
        self.save_mrp_results(purchase_requisitions)

    def save_mrp_results(self, requisitions):
        if not requisitions:
            logging.info("Tüm stoklar yeterli. Satın alma talebi oluşturulmadı.")
            return

        conn = sqlite3.connect(self.db_path)
        df_pr = pd.DataFrame(requisitions)
        df_pr.to_sql('mrp_purchase_requisitions', conn, if_exists='replace', index=False)
        conn.close()
        
        logging.info(f"Oluşturulan {len(requisitions)} adet Satın Alma Talebi ERP Veritabanına ('mrp_purchase_requisitions') Aktarıldı.")

if __name__ == "__main__":
    mrp = ERPMRPEngine()
    # Senaryo: 10 Adet DEF-DRONE-X1 Üretimi İçin Malzeme İhtiyaç Planlamasını Çalıştır
    mrp.run_mrp_calculation(target_product_code="DEF-DRONE-X1", demand_quantity=10)
