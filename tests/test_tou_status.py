"""ทดสอบการคำนวณช่วงเวลา TOU."""
from datetime import datetime
from freezegun import freeze_time
# สมมติฟังก์ชันเช็กเวลา TOU หรือใช้คลาส MeaTouStatusSensor

@freeze_time("2026-09-09 14:00:00")  # วันพุธ เวลา 14:00 น. (บ่าย)
def test_tou_status_on_peak():
    # โค้ดทดสอบ: ในเวลางานวันธรรมดา ต้องคืนค่า "On Peak"
    ...

@freeze_time("2026-09-09 23:00:00")  # วันพุธ เวลา 23:00 น. (กลางคืน)
def test_tou_status_off_peak_night():
    # โค้ดทดสอบ: นอกเวลางาน ต้องคืนค่า "Off Peak"
    ...