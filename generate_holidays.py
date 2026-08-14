import os
import json
import holidays

REPO_DIR = r"C:\Users\dastl\shift-calendar-site"
YEARS = range(2025, 2032) # 2025–2031 годы

# Список 100 стран для генерации
COUNTRIES = [
    "RU", "BY", "KZ", "UZ", "KG", "AM", "GE", "AZ",
    "US", "CA", "MX", "BR", "AR", "CL", "CO", "PE", "EC", "UY", "PY", "BO", "CR", "PA", "DO", "GT", "JM",
    "DE", "FR", "GB", "IT", "ES", "PL", "CH", "AT", "NL", "BE", "SE", "NO", "FI", "DK", "PT", "CZ", "SK", "HU", "RO", "IE", "LU", "IS", "GR", "HR", "SI", "RS", "BG", "EE", "LV", "LT", "CY", "MT",
    "JP", "KR", "VN", "TH", "PH", "MY", "ID", "IN", "TR", "SA", "AE", "IR", "TW", "HK", "SG", "AU", "NZ", "QA", "KW", "OM", "BH", "IL", "JO", "EG", "DZ", "MA", "IQ", "PK", "BD", "LK", "NP", "MM", "KH", "LA", "MN", "FJ", "PG", "MO",
    "ZA", "NG", "KE", "GH", "ET"
]

# Профессиональные и памятные дни для РФ
RU_CUSTOM_DAYS = [
    ("01-12", "День работника прокуратуры"),
    ("01-13", "День российской печати"),
    ("01-21", "День инженерных войск"),
    ("01-25", "Татьянин день (День студента)"),
    ("02-08", "День российской науки"),
    ("02-09", "День гражданской авиации"),
    ("02-10", "День дипломатического работника"),
    ("02-14", "День всех влюблённых"),
    ("02-15", "День памяти воинов-интернационалистов"),
    ("02-27", "День Сил специальных операций"),
    ("03-18", "День воссоединения Крыма с Россией"),
    ("03-19", "День моряка-подводника"),
    ("03-25", "День работника культуры"),
    ("03-27", "День войск национальной гвардии (Росгвардия)"),
    ("04-12", "День космонавтики"),
    ("04-19", "День российской полиграфии"),
    ("04-28", "День скорой медицинской помощи"),
    ("04-30", "День пожарной охраны"),
    ("05-07", "День радио"),
    ("05-26", "День российского предпринимательства"),
    ("05-28", "День пограничника"),
    ("06-05", "День эколога"),
    ("06-08", "День социального работника"),
    ("06-22", "День памяти и скорби"),
    ("07-03", "День ГИБДД (ГАИ)"),
    ("07-08", "День семьи, любви и верности"),
    ("08-02", "День ВДВ"),
    ("08-12", "День ВВС"),
    ("09-01", "День знаний"),
    ("09-19", "День оружейника"),
    ("09-30", "День воссоединения новых регионов"),
    ("10-04", "День Космических войск"),
    ("10-05", "День учителя"),
    ("10-25", "День таможенника РФ"),
    ("11-10", "День полиции"),
    ("11-11", "День экономиста"),
    ("11-19", "День ракетных войск и артиллерии"),
    ("11-21", "День работника налоговых органов"),
    ("12-03", "День юриста"),
    ("12-17", "День РВСН"),
    ("12-20", "День работника органов безопасности (ФСБ)"),
    ("12-22", "День энергетика"),
    ("12-27", "День спасателя РФ (МЧС)")
]

# Профессиональные и памятные дни для США
US_CUSTOM_DAYS = [
    ("01-09", "National Law Enforcement Appreciation Day"),
    ("02-02", "Groundhog Day"),
    ("02-14", "Valentine's Day"),
    ("03-02", "Texas Independence Day"),
    ("03-17", "St. Patrick's Day"),
    ("03-30", "National Doctors' Day"),
    ("03-31", "César Chávez Day"),
    ("04-15", "Tax Day"),
    ("04-22", "Earth Day"),
    ("05-04", "International Firefighters' Day"),
    ("05-05", "Cinco de Mayo"),
    ("05-06", "National Nurses Day"),
    ("05-15", "Peace Officers Memorial Day"),
    ("06-14", "Flag Day & US Army Birthday"),
    ("07-24", "Pioneer Day (Utah)"),
    ("08-04", "US Coast Guard Day"),
    ("09-09", "California Admission Day"),
    ("09-11", "Patriot Day (9/11 Remembrance)"),
    ("09-15", "Beginning of National Hispanic Heritage Month"),
    ("09-18", "US Air Force Birthday & Tradesmen Day"),
    ("10-13", "US Navy Birthday"),
    ("10-16", "Boss's Day"),
    ("10-28", "National First Responders Day"),
    ("10-31", "Halloween"),
    ("11-01", "Day of the Dead (Día de los Muertos)"),
    ("11-10", "US Marine Corps Birthday"),
    ("12-07", "Pearl Harbor Remembrance Day"),
    ("12-12", "Day of the Virgin of Guadalupe"),
    ("12-31", "New Year's Eve")
]

def generate():
    total_files = 0
    for year in YEARS:
        year_dir = os.path.join(REPO_DIR, "holidays", str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        for country in COUNTRIES:
            holiday_list = []
            
            # 1. Получаем официальные государственные праздники из библиотеки holidays
            try:
                country_holidays = holidays.country_holidays(country, years=year, observed=True)
                for h_date, h_name in sorted(country_holidays.items()):
                    holiday_list.append({
                        "date": h_date.isoformat(),
                        "name": str(h_name),
                        "isPublic": True
                    })
            except Exception:
                pass

            # 2. Добавляем памятные дни для РФ
            if country == "RU":
                for md, name in RU_CUSTOM_DAYS:
                    date_str = f"{year}-{md}"
                    if not any(h["date"] == date_str and h["name"] == name for h in holiday_list):
                        holiday_list.append({
                            "date": date_str,
                            "name": name,
                            "isPublic": False
                        })

            # 3. Добавляем памятные дни для США
            if country == "US":
                for md, name in US_CUSTOM_DAYS:
                    date_str = f"{year}-{md}"
                    if not any(h["date"] == date_str and h["name"] == name for h in holiday_list):
                        holiday_list.append({
                            "date": date_str,
                            "name": name,
                            "isPublic": False
                        })

            holiday_list.sort(key=lambda x: x["date"])

            # Записываем чистый JSON без BOM
            file_path = os.path.join(year_dir, f"{country}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(holiday_list, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Успех! Сгенерировано {total_files} файлов для всех 100 стран на 2025–2031 годы!")

if __name__ == "__main__":
    generate()
