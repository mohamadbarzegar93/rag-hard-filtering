"""
Generates synthetic product catalogs for 4 fictitious providers with
deliberately overlapping products (same category/region, similar specs)
so that pure semantic search struggles to pick the right provider.

Providers (fictional, inspired by real-world archetypes but not real brands):
  - NordicTech      -> boutique EU electronics supplier
  - AlpineSupply    -> boutique EU electronics supplier (overlaps NordicTech)
  - BlitzMarkt      -> big-box electronics chain (MediaMarkt-style)
  - OmniHaul        -> broad online marketplace (Amazon-style)

Run:
    python generate_data.py
Output:
    data/products/<provider>_catalog.json  (one file per provider)
"""

import json
import os

OUTPUT_DIR = os.path.join("data", "products")

PROVIDERS = ["nordictech", "alpinesupply", "blitzmarkt", "omnihaul"]

CATALOGS = {
    "nordictech": [
        {
            "product_id": "NT-001",
            "provider": "NordicTech",
            "category": "laptops",
            "region": "EU",
            "name": "NordicBook Pro 14",
            "description": "14-inch business laptop, 16GB RAM, 512GB SSD, aluminum chassis, EU energy-efficiency certified. Designed for professionals who need reliable all-day performance.",
        },
        {
            "product_id": "NT-002",
            "provider": "NordicTech",
            "category": "laptops",
            "region": "EU",
            "name": "NordicBook Air 13",
            "description": "13-inch ultralight laptop, 8GB RAM, 256GB SSD. Built for mobile professionals who travel frequently between EU offices.",
        },
        {
            "product_id": "NT-003",
            "provider": "NordicTech",
            "category": "headphones",
            "region": "EU",
            "name": "NordicSound ANC Pro",
            "description": "Over-ear noise-cancelling headphones with 30-hour battery life, designed and manufactured in the EU.",
        },
        {
            "product_id": "NT-004",
            "provider": "NordicTech",
            "category": "monitors",
            "region": "EU",
            "name": "NordicView 27 4K",
            "description": "27-inch 4K IPS monitor with USB-C power delivery, aimed at hybrid office setups.",
        },
    ],
    "alpinesupply": [
        {
            "product_id": "AS-001",
            "provider": "AlpineSupply",
            "category": "laptops",
            "region": "EU",
            "name": "AlpineBook Business 14",
            "description": "14-inch business laptop, 16GB RAM, 512GB SSD, magnesium alloy body, EU energy-efficiency certified. Marketed toward professionals needing dependable daily performance.",
        },
        {
            "product_id": "AS-002",
            "provider": "AlpineSupply",
            "category": "laptops",
            "region": "EU",
            "name": "AlpineBook Ultralight 13",
            "description": "13-inch lightweight laptop, 8GB RAM, 256GB SSD, aimed at professionals who commute often within the EU.",
        },
        {
            "product_id": "AS-003",
            "provider": "AlpineSupply",
            "category": "headphones",
            "region": "EU",
            "name": "AlpineAudio Silence Pro",
            "description": "Over-ear ANC headphones, 28-hour battery, EU-manufactured, comparable feature set to competing EU audio brands.",
        },
        {
            "product_id": "AS-004",
            "provider": "AlpineSupply",
            "category": "keyboards",
            "region": "EU",
            "name": "AlpineType Mechanical",
            "description": "Compact mechanical keyboard with hot-swappable switches, targeted at EU-based developers and office workers.",
        },
    ],
    "blitzmarkt": [
        {
            "product_id": "BM-001",
            "provider": "BlitzMarkt",
            "category": "laptops",
            "region": "EU",
            "name": "BlitzBook 14 Business Edition",
            "description": "14-inch laptop, 16GB RAM, 512GB SSD, sold through BlitzMarkt's business electronics line across EU stores.",
        },
        {
            "product_id": "BM-002",
            "provider": "BlitzMarkt",
            "category": "tvs",
            "region": "EU",
            "name": "BlitzView 55 OLED",
            "description": "55-inch OLED television with HDR10+ support, popular in-store big-box electronics purchase.",
        },
        {
            "product_id": "BM-003",
            "provider": "BlitzMarkt",
            "category": "headphones",
            "region": "EU",
            "name": "BlitzAudio ANC 300",
            "description": "Noise-cancelling over-ear headphones, budget-to-midrange tier, sold in BlitzMarkt's audio department.",
        },
        {
            "product_id": "BM-004",
            "provider": "BlitzMarkt",
            "category": "monitors",
            "region": "EU",
            "name": "BlitzView Office 27",
            "description": "27-inch 4K monitor with USB-C, part of BlitzMarkt's office equipment range.",
        },
    ],
    "omnihaul": [
        {
            "product_id": "OH-001",
            "provider": "OmniHaul",
            "category": "laptops",
            "region": "Global",
            "name": "OmniHaul Marketplace Business Laptop 14-inch",
            "description": "Third-party seller listing: 14-inch business laptop, 16GB RAM, 512GB SSD, shipped globally via OmniHaul marketplace.",
        },
        {
            "product_id": "OH-002",
            "provider": "OmniHaul",
            "category": "headphones",
            "region": "Global",
            "name": "OmniHaul Choice ANC Headphones",
            "description": "Best-seller noise-cancelling headphones on OmniHaul marketplace, fulfilled by OmniHaul, ships worldwide.",
        },
        {
            "product_id": "OH-003",
            "provider": "OmniHaul",
            "category": "keyboards",
            "region": "Global",
            "name": "OmniHaul Basics Mechanical Keyboard",
            "description": "Budget mechanical keyboard, top-rated by OmniHaul marketplace customers globally.",
        },
        {
            "product_id": "OH-004",
            "provider": "OmniHaul",
            "category": "tvs",
            "region": "Global",
            "name": "OmniHaul Deals 55-inch OLED TV",
            "description": "Discounted 55-inch OLED TV, frequent lightning-deal item on OmniHaul marketplace.",
        },
    ],
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = 0
    for provider_key in PROVIDERS:
        records = CATALOGS[provider_key]
        out_path = os.path.join(OUTPUT_DIR, f"{provider_key}_catalog.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"Wrote {len(records)} products -> {out_path}")
        total += len(records)
    print(f"\nTotal products generated: {total}")


if __name__ == "__main__":
    main()
