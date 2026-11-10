"""ทดสอบการคำนวณช่วงเวลา TOU และ Day Type."""
import sys
from pathlib import Path

# ดึง Path ของโฟลเดอร์โปรเจกต์ (แบบเดียวกับ tests/test_parser.py)
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from freezegun import freeze_time
from homeassistant.util import dt as dt_util

from custom_components.mea_thailand_grid_tariffs.sensor import (
    _day_type_at,
    _tou_status_at,
)

# ชุดวันหยุดตัวอย่าง (ตรงกับรูปแบบ YYYY-MM-DD ใน holidays.txt)
HOLIDAYS = {"2026-01-01"}


# --- TOU On/Off-Peak status ---

@freeze_time("2026-09-09 14:00:00")  # วันพุธ 14:00 (เวลาทำงาน)
def test_tou_status_on_peak():
    assert _tou_status_at(dt_util.now(), HOLIDAYS) == "On Peak"


@freeze_time("2026-09-09 23:00:00")  # วันพุธ 23:00 (กลางคืน)
def test_tou_status_off_peak_night():
    assert _tou_status_at(dt_util.now(), HOLIDAYS) == "Off Peak"


@freeze_time("2026-09-12 14:00:00")  # วันเสาร์ 14:00
def test_tou_status_off_peak_weekend():
    assert _tou_status_at(dt_util.now(), HOLIDAYS) == "Off Peak"


@freeze_time("2026-01-01 14:00:00")  # วันหยุดราชการ 14:00
def test_tou_status_off_peak_holiday():
    assert _tou_status_at(dt_util.now(), HOLIDAYS) == "Off Peak"


# --- TOU Day Type ---

@freeze_time("2026-01-01 14:00:00")  # วันหยุดราชการ
def test_day_type_holiday():
    assert _day_type_at(dt_util.now(), HOLIDAYS) == "Holiday"


@freeze_time("2026-09-12 14:00:00")  # วันเสาร์
def test_day_type_weekend():
    assert _day_type_at(dt_util.now(), HOLIDAYS) == "Weekend"


@freeze_time("2026-09-09 14:00:00")  # วันพุธ
def test_day_type_weekday():
    assert _day_type_at(dt_util.now(), HOLIDAYS) == "Weekday"
