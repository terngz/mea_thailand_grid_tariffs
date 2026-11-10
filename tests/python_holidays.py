from datetime import datetime, timedelta

# ดิกชันนารีจับคู่วันที่กับชื่อวันหยุดประจำปี 2027
holidays_dict = {
    '2027-01-01': "New Year's Day",
    '2027-02-21': "Makha Bucha Day",
    '2027-02-22': "Substitution for Makha Bucha Day",
    '2027-04-06': "Chakri Memorial Day",
    '2027-04-13': "Songkran Festival",
    '2027-04-14': "Songkran Festival",
    '2027-04-15': "Songkran Festival",
    '2027-05-01': "National Labour Day",
    '2027-05-03': "Substitution for National Labour Day",
    '2027-05-04': "Coronation Day",
    '2027-05-20': "Visakha Bucha Day",
    '2027-06-03': "H.M. Queen Suthida's Birthday",
    '2027-07-17': "Asarnha Bucha Day",
    '2027-07-18': "Buddhist Lent Day",
    '2027-07-19': "Substitution for Asarnha Bucha Day",
    '2027-07-28': "H.M. King Maha Vajiralongkorn's Birthday",
    '2027-08-12': "H.M. Queen Sirikit The Queen Mother's Birthday / Mother's Day",
    '2027-10-13': "H.M. King Bhumibol Adulyadej The Great Memorial Day",
    '2027-10-23': "King Chulalongkorn Day (Piyamaharaj Day)",
    '2027-10-25': "Substitution for King Chulalongkorn Day",
    '2027-12-05': "H.M. King Bhumibol Adulyadej's Birthday / Father's Day",
    '2027-12-06': "Substitution for Father's Day",
    '2027-12-10': "Constitution Day",
    '2027-12-31': "New Year's Eve"
}

ics_content = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//MEA Thailand Grid Tariffs//Holidays//TH",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH"
]

for date_str, summary in holidays_dict.items():
    dt_start = datetime.strptime(date_str, '%Y-%m-%d')
    dt_end = dt_start + timedelta(days=1)
    
    start_str = dt_start.strftime('%Y%m%d')
    end_str = dt_end.strftime('%Y%m%d')
    
    ics_content.extend([
        "BEGIN:VEVENT",
        f"SUMMARY:{summary}",
        f"DTSTART;VALUE=DATE:{start_str}",
        f"DTEND;VALUE=DATE:{end_str}",
        "END:VEVENT"
    ])

ics_content.append("END:VCALENDAR")

with open('holidays.ics', 'w', encoding='utf-8') as f:
    f.write("\n".join(ics_content))

print("สร้างไฟล์ holidays.ics พร้อมชื่อวันหยุดเรียบร้อยแล้ว!")