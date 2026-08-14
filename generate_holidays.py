import os
import json
import holidays

REPO_DIR = r"C:\Users\dastl\shift-calendar-site"
YEARS = range(2025, 2032) # 2025–2031

COUNTRIES = [
    "RU", "BY", "KZ", "UZ", "KG", "AM", "GE", "AZ",
    "US", "CA", "MX", "BR", "AR", "CL", "CO", "PE", "EC", "UY", "PY", "BO", "CR", "PA", "DO", "GT", "JM",
    "DE", "FR", "GB", "IT", "ES", "PL", "CH", "AT", "NL", "BE", "SE", "NO", "FI", "DK", "PT", "CZ", "SK", "HU", "RO", "IE", "LU", "IS", "GR", "HR", "SI", "RS", "BG", "EE", "LV", "LT", "CY", "MT",
    "JP", "KR", "VN", "TH", "PH", "MY", "ID", "IN", "TR", "SA", "AE", "IR", "TW", "HK", "SG", "AU", "NZ", "QA", "KW", "OM", "BH", "IL", "JO", "EG", "DZ", "MA", "IQ", "PK", "BD", "LK", "NP", "MM", "KH", "LA", "MN", "FJ", "PG", "MO",
    "ZA", "NG", "KE", "GH", "ET"
]

# Универсальный международный пакет дат для ВСЕХ 100 стран
GLOBAL_OBSERVANCES = [
    ("01-01", "New Year's Day"),
    ("01-24", "International Day of Education"),
    ("02-11", "International Day of Women and Girls in Science"),
    ("02-14", "Valentine's Day"),
    ("03-08", "International Women's Day"),
    ("03-20", "International Day of Happiness / Spring Equinox"),
    ("03-21", "World Poetry Day / Forest Day"),
    ("03-22", "World Water Day"),
    ("04-07", "World Health Day"),
    ("04-12", "International Day of Human Space Flight"),
    ("04-22", "Earth Day"),
    ("04-23", "World Book and Copyright Day"),
    ("04-28", "World Day for Safety and Health at Work"),
    ("05-01", "International Workers' Day"),
    ("05-03", "World Press Freedom Day"),
    ("05-08", "Time of Remembrance and Reconciliation (WWII)"),
    ("05-12", "International Nurses Day"),
    ("05-15", "International Day of Families"),
    ("05-21", "World Day for Cultural Diversity"),
    ("05-22", "International Day for Biological Diversity"),
    ("06-01", "Global Day of Parents & Children's Day"),
    ("06-05", "World Environment Day"),
    ("06-08", "World Oceans Day"),
    ("06-21", "World Music Day (Fête de la Musique)"),
    ("06-23", "United Nations Public Service Day"),
    ("07-11", "World Population Day"),
    ("07-15", "World Youth Skills Day"),
    ("07-30", "International Day of Friendship"),
    ("08-12", "International Youth Day"),
    ("08-19", "World Humanitarian Day & Photography Day"),
    ("09-08", "International Literacy Day"),
    ("09-13", "International Programmers' Day"),
    ("09-15", "International Day of Democracy"),
    ("09-21", "International Day of Peace"),
    ("09-27", "World Tourism Day"),
    ("10-01", "International Day of Older Persons"),
    ("10-05", "World Teachers' Day"),
    ("10-10", "World Mental Health Day"),
    ("10-16", "World Food Day"),
    ("10-24", "United Nations Day"),
    ("10-28", "International Animation Day"),
    ("10-31", "Halloween / World Cities Day"),
    ("11-10", "World Science Day for Peace and Development"),
    ("11-20", "World Children's Day"),
    ("11-21", "World Television Day & Philosophy Day"),
    ("12-03", "International Day of Persons with Disabilities"),
    ("12-05", "International Volunteer Day"),
    ("12-07", "International Civil Aviation Day"),
    ("12-10", "Human Rights Day"),
    ("12-24", "Christmas Eve"),
    ("12-25", "Christmas Day"),
    ("12-31", "New Year's Eve")
]

# Кастомные даты для России
RU_CUSTOM_DAYS = [
    ("01-12", "День работника прокуратуры"),
    ("01-13", "День российской печати"),
    ("01-21", "День инженерных войск"),
    ("01-25", "Татьянин день (День студента)"),
    ("02-08", "День российской науки"),
    ("02-09", "День гражданской авиации"),
    ("02-10", "День дипломатического работника"),
    ("02-15", "День памяти воинов-интернационалистов"),
    ("02-23", "День защитника Отечества"),
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
    ("05-09", "День Победы"),
    ("05-26", "День российского предпринимательства"),
    ("05-28", "День пограничника"),
    ("06-05", "День эколога"),
    ("06-08", "День социального работника"),
    ("06-12", "День России"),
    ("06-22", "День памяти и скорби"),
    ("07-03", "День ГИБДД (ГАИ)"),
    ("07-08", "День семьи, любви и верности"),
    ("08-02", "День ВДВ"),
    ("08-12", "День ВВС"),
    ("09-01", "День знаний"),
    ("09-19", "День оружейника"),
    ("09-30", "День воссоединения новых регионов"),
    ("10-04", "День Космических войск"),
    ("10-25", "День таможенника РФ"),
    ("11-04", "День народного единства"),
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

def generate():
    total_files = 0
    for year in YEARS:
        year_dir = os.path.join(REPO_DIR, "holidays", str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        for country in COUNTRIES:
            holiday_dict = {}
            
            # 1. Запрашиваем ВСЕ категории из библиотеки Python Holidays (не только public!)
            try:
                all_cats = getattr(holidays, 'ALL_CATEGORIES', None)
                if all_cats is not None:
                    country_hols = holidays.country_holidays(country, years=year, observed=True, categories=all_cats)
                else:
                    country_hols = holidays.country_holidays(country, years=year, observed=True)
                    
                for h_date, h_name in country_hols.items():
                    d_str = h_date.isoformat()
                    holiday_dict[d_str] = {
                        "date": d_str,
                        "name": str(h_name),
                        "isPublic": True
                    }
            except Exception:
                pass

            # 2. Добавляем универсальный международный пакет (ООН, экология, культура, профессии)
            for md, name in GLOBAL_OBSERVANCES:
                date_str = f"{year}-{md}"
                if date_str not in holiday_dict:
                    holiday_dict[date_str] = {
                        "date": date_str,
                        "name": name,
                        "isPublic": False
                    }

            # 3. Добавляем специфические профессиональные дни для РФ
            if country == "RU":
                for md, name in RU_CUSTOM_DAYS:
                    date_str = f"{year}-{md}"
                    holiday_dict[date_str] = {
                        "date": date_str,
                        "name": name,
                        "isPublic": (md in ["01-01","01-02","01-03","01-04","01-05","01-06","01-07","01-08","02-23","03-08","05-01","05-09","06-12","11-04"])
                    }

            # Превращаем в отсортированный список
            holiday_list = list(holiday_dict.values())
            holiday_list.sort(key=lambda x: x["date"])

            # Записываем чистый JSON без BOM
            file_path = os.path.join(year_dir, f"{country}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(holiday_list, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Успех! Сгенерировано {total_files} насыщенных файлов (в среднем по 40–60 дат на страну)!")

if __name__ == "__main__":
    generate()
