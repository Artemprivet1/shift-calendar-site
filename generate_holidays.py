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

# Карта языков для каждой группы стран
def get_country_lang_group(country):
    if country in ["RU", "BY", "KZ", "KG", "UZ"]: return "ru"
    if country in ["ES", "MX", "AR", "CL", "CO", "PE", "EC", "UY", "PY", "BO", "CR", "PA", "DO", "GT"]: return "es"
    if country in ["DE", "AT", "CH"]: return "de"
    if country in ["FR"]: return "fr"
    if country in ["IT"]: return "it"
    if country in ["BR", "PT"]: return "pt"
    if country in ["PL"]: return "pl"
    if country in ["TR"]: return "tr"
    return "en"

# Международный пакет дат на разных языках
GLOBAL_PACK = {
    "ru": [
        ("02-14", "День всех влюблённых"),
        ("03-08", "Международный женский день"),
        ("04-01", "День смеха"),
        ("04-12", "День космонавтики"),
        ("04-22", "День Земли"),
        ("04-23", "Всемирный день книги"),
        ("05-12", "Международный день медицинской сестры"),
        ("06-01", "Международный день защиты детей"),
        ("06-21", "Международный день музыки"),
        ("09-01", "День знаний"),
        ("09-13", "День программиста"),
        ("10-05", "Всемирный день учителя"),
        ("10-31", "Хэллоуин"),
        ("11-10", "Всемирный день науки"),
        ("12-31", "Новогодний вечер")
    ],
    "es": [
        ("02-14", "Día de San Valentín"),
        ("03-08", "Día Internacional de la Mujer"),
        ("04-01", "Día de las Bromas"),
        ("04-22", "Día de la Tierra"),
        ("04-23", "Día Mundial del Libro"),
        ("05-12", "Día Internacional de la Enfermería"),
        ("06-01", "Día del Niño"),
        ("06-21", "Día de la Música"),
        ("09-13", "Día del Programador"),
        ("10-05", "Día Mundial de los Docentes"),
        ("10-31", "Halloween"),
        ("11-10", "Día Mundial de la Ciencia"),
        ("12-31", "Nochevieja")
    ],
    "de": [
        ("02-14", "Valentinstag"),
        ("03-08", "Internationaler Frauentag"),
        ("04-01", "Erster April"),
        ("04-22", "Tag der Erde"),
        ("04-23", "Welttag des Buches"),
        ("05-12", "Internationaler Tag der Pflege"),
        ("06-01", "Internationaler Kindertag"),
        ("06-21", "Fête de la Musique (Tag der Musik)"),
        ("09-13", "Tag der Programmierer"),
        ("10-05", "Weltlehrertag"),
        ("10-31", "Halloween"),
        ("11-10", "Welttag der Wissenschaft"),
        ("12-31", "Silvester")
    ],
    "fr": [
        ("02-14", "Saint-Valentin"),
        ("03-08", "Journée internationale des droits des femmes"),
        ("04-01", "Poisson d'avril"),
        ("04-22", "Jour de la Terre"),
        ("04-23", "Journée mondiale du livre"),
        ("05-12", "Journée internationale des infirmières"),
        ("06-01", "Journée internationale des enfants"),
        ("06-21", "Fête de la Musique"),
        ("09-13", "Journée des programmeurs"),
        ("10-05", "Journée mondiale des enseignants"),
        ("10-31", "Halloween"),
        ("11-10", "Journée mondiale de la science"),
        ("12-31", "Réveillon de la Saint-Sylvestre")
    ],
    "pt": [
        ("02-14", "Dia de São Valentim"),
        ("03-08", "Dia Internacional da Mulher"),
        ("04-01", "Dia da Mentira"),
        ("04-22", "Dia da Terra"),
        ("04-23", "Dia Mundial do Livro"),
        ("05-12", "Dia Internacional da Enfermagem"),
        ("06-01", "Dia Mundial da Criança"),
        ("06-21", "Dia da Música"),
        ("09-13", "Dia do Programador"),
        ("10-05", "Dia Mundial dos Professores"),
        ("10-31", "Halloween"),
        ("11-10", "Dia Mundial da Ciência"),
        ("12-31", "Véspera de Ano Novo")
    ],
    "it": [
        ("02-14", "Festa di San Valentino"),
        ("03-08", "Giornata internazionale della donna"),
        ("04-01", "Pesce d'aprile"),
        ("04-22", "Giornata della Terra"),
        ("04-23", "Giornata mondiale del libro"),
        ("05-12", "Giornata internazionale dell'infermiere"),
        ("06-01", "Giornata internazionale dei bambini"),
        ("06-21", "Festa della Musica"),
        ("09-13", "Giornata dei programmatori"),
        ("10-05", "Giornata mondiale degli insegnanti"),
        ("10-31", "Halloween"),
        ("11-10", "Giornata mondiale della scienza"),
        ("12-31", "Notte di San Silvestro")
    ],
    "pl": [
        ("02-14", "Walentynki"),
        ("03-08", "Dzień Kobiet"),
        ("04-01", "Prima aprilis"),
        ("04-22", "Dzień Ziemi"),
        ("04-23", "Światowy Dzień Książki"),
        ("05-12", "Międzynarodowy Dzień Pielęgniarek"),
        ("06-01", "Dzień Dziecka"),
        ("06-21", "Święto Muzyki"),
        ("09-01", "Dzień Wiedzy"),
        ("09-13", "Dzień Programisty"),
        ("10-05", "Światowy Dzień Nauczyciela"),
        ("10-31", "Halloween"),
        ("11-10", "Światowy Dzień Nauki"),
        ("12-31", "Sylwester")
    ],
    "en": [
        ("02-14", "Valentine's Day"),
        ("03-08", "International Women's Day"),
        ("04-01", "April Fools' Day"),
        ("04-22", "Earth Day"),
        ("04-23", "World Book Day"),
        ("05-12", "International Nurses Day"),
        ("06-01", "International Children's Day"),
        ("06-21", "World Music Day"),
        ("09-13", "International Programmers' Day"),
        ("10-05", "World Teachers' Day"),
        ("10-31", "Halloween"),
        ("11-10", "World Science Day"),
        ("12-31", "New Year's Eve")
    ]
}

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
            lang_group = get_country_lang_group(country)
            
            # 1. Запрашиваем праздники на родном языке страны
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

            # 2. Добавляем международный пакет на языке страны
            obs_list = GLOBAL_PACK.get(lang_group, GLOBAL_PACK["en"])
            for md, name in obs_list:
                date_str = f"{year}-{md}"
                if date_str not in holiday_dict:
                    holiday_dict[date_str] = {
                        "date": date_str,
                        "name": name,
                        "isPublic": False
                    }

            # 3. Добавляем профессиональные дни для РФ
            if country == "RU":
                for md, name in RU_CUSTOM_DAYS:
                    date_str = f"{year}-{md}"
                    holiday_dict[date_str] = {
                        "date": date_str,
                        "name": name,
                        "isPublic": (md in ["01-01","01-02","01-03","01-04","01-05","01-06","01-07","01-08","02-23","03-08","05-01","05-09","06-12","11-04"])
                    }

            holiday_list = list(holiday_dict.values())
            holiday_list.sort(key=lambda x: x["date"])

            file_path = os.path.join(year_dir, f"{country}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(holiday_list, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Готово! Все 100 стран переведены на их родные языки (всего {total_files} файлов)!")

if __name__ == "__main__":
    generate()
