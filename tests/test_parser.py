"""ทดสอบการ Parse ข้อมูลจาก HTML จริงของประเภท 2 (กิจการขนาดเล็ก)."""
import sys
from pathlib import Path

# ดึง Path ของโฟลเดอร์โปรเจกต์
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ประกาศ FIXTURES_DIR ชี้ไปยังโฟลเดอร์ tests/fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures"

from custom_components.mea_thailand_grid_tariffs.parser import (
    RateBlock,
    parse_tariff_page,
)


def test_parse_small_business_html():
    """ทดสอบและพิมพ์ค่าที่ดึงได้จาก HTML ประเภท 2."""
    html_path = FIXTURES_DIR / "small_business.html"
    html_content = html_path.read_text(encoding="utf-8")

    blocks: list[RateBlock] = parse_tariff_page(html_content)

    print("\n" + "=" * 50)
    print("      PARSED RESULTS FROM SMALL BUSINESS HTML")
    print("=" * 50)

    for b in blocks:
        print(f"\n[Block Key]: {b.key}")
        print(f"  Title: {b.title}")
        if b.on_peak is not None:
            print(f"  On-Peak Rate  : {b.on_peak} THB/kWh")
            print(f"  Off-Peak Rate : {b.off_peak} THB/kWh")
        if b.service_charge is not None:
            print(f"  Service Charge: {b.service_charge} THB/month")
        if b.tiers:
            print("  Tiers:")
            for idx, t in enumerate(b.tiers, 1):
                print(f"    - Tier {idx} [{t.label}]: {t.rate} THB/kWh (Start: {t.start}, End: {t.end})")

    print("\n" + "=" * 50)

    block_dict = {b.key: b for b in blocks}

    # 1. ตรวจสอบประเภท 2.1.1 (12 - 24 kV)
    assert "sb_211" in block_dict
    assert block_dict["sb_211"].service_charge == 312.24
    assert block_dict["sb_211"].tiers[0].rate == 3.9086

    # 2. ตรวจสอบประเภท 2.1.2 (Below 12 kV)
    assert "sb_212" in block_dict
    assert block_dict["sb_212"].service_charge == 33.29
    assert len(block_dict["sb_212"].tiers) == 3
    assert block_dict["sb_212"].tiers[0].rate == 3.2484
    assert block_dict["sb_212"].tiers[1].rate == 4.2218
    assert block_dict["sb_212"].tiers[2].rate == 4.4217

    # 3. ตรวจสอบประเภท 2.2.2 (TOU)
    assert "sb_tou_222" in block_dict
    assert block_dict["sb_tou_222"].on_peak == 5.7982
    assert block_dict["sb_tou_222"].off_peak == 2.6369
    assert block_dict["sb_tou_222"].service_charge == 33.29