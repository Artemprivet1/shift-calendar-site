import json
import os
from datetime import date, timedelta

REPO_DIR = r"C:\Users\dastl\shift-calendar-site"
YEAR_FROM = 2025
YEAR_TO = 2036

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}

def nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    """occurrence: 1,2,3.. for Nth weekday, or -1 for last."""
    if occurrence > 0:
        d = date(year, month, 1)
        offset = (weekday - d.weekday()) % 7
        return d + timedelta(days=offset + 7 * (occurrence - 1))
    else:
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        offset = (last_day.weekday() - weekday) % 7
        return last_day - timedelta(days=offset)

def day_of_year(year: int, n: int) -> date:
    return date(year, 1, 1) + timedelta(days=n - 1)

# ---------- ПРОФЕССИОНАЛЬНЫЕ ПРАЗДНИКИ ----------
PROFESSIONAL_FIXED = [
    (1, 12, "День работника прокуратуры"),
    (1, 13, "День российской печати"),
    (1, 21, "День инженерных войск"),
    (2, 8, "День российской науки"),
    (2, 9, "День работника гражданской авиации"),
    (2, 10, "День дипломатического работника"),
    (2, 27, "День Сил специальных операций"),
    (3, 11, "День работника органов наркоконтроля"),
    (3, 19, "День моряка-подводника"),
    (3, 23, "День работников гидрометеорологической службы"),
    (3, 25, "День работника культуры"),
    (3, 27, "День войск национальной гвардии (Росгвардия)"),
    (3, 29, "День специалиста юридической службы ВС РФ"),
    (4, 8, "День сотрудников военных комиссариатов"),
    (4, 12, "День космонавтики"),
    (4, 15, "День специалиста по радиоэлектронной борьбе"),
    (4, 19, "День российской полиграфии"),
    (4, 28, "День скорой медицинской помощи"),
    (4, 30, "День пожарной охраны"),
    (5, 7, "День радио"),
    (5, 21, "День полярника"),
    (5, 26, "День российского предпринимательства"),
    (5, 28, "День пограничника"),
    (6, 5, "День эколога"),
    (6, 8, "День социального работника"),
    (6, 14, "День работника миграционной службы"),
    (6, 25, "День работника статистики"),
    (6, 27, "День молодёжи"),
    (7, 3, "День ГИБДД (ГАИ)"),
    (8, 2, "День ВДВ"),
    (8, 12, "День ВВС"),
    (9, 1, "День знаний"),
    (9, 4, "День специалиста по ядерному обеспечению"),
    (9, 8, "День финансиста"),
    (9, 19, "День оружейника"),
    (10, 4, "День Космических войск"),
    (10, 5, "День учителя"),
    (10, 20, "День военного связиста"),
    (10, 25, "День таможенника РФ"),
    (11, 1, "День судебного пристава"),
    (11, 5, "День военного разведчика"),
    (11, 10, "День сотрудника органов внутренних дел РФ"),
    (11, 11, "День экономиста"),
    (11, 19, "День ракетных войск и артиллерии"),
    (11, 21, "День работника налоговых органов РФ"),
    (12, 3, "День юриста"),
    (12, 17, "День РВСН"),
    (12, 20, "День работника органов безопасности РФ (ФСБ)"),
    (12, 22, "День энергетика"),
    (12, 27, "День спасателя РФ (МЧС)")
]

PROFESSIONAL_FLOATING = [
    (3, "sunday", 2, "День работников геодезии и картографии"),
    (3, "sunday", 3, "День работников торговли, бытового обслуживания и ЖКХ"),
    (4, "sunday", 1, "День геолога"),
    (5, "sunday", -1, "День химика"),
    (6, "sunday", 2, "День работников лёгкой промышленности"),
    (6, "sunday", 3, "День медицинского работника"),
    (6, "saturday", -1, "День изобретателя и рационализатора"),
    (7, "sunday", 1, "День работников морского и речного флота"),
    (7, "sunday", 2, "День рыбака"),
    (7, "sunday", 3, "День металлурга"),
    (7, "saturday", 4, "День работника торговли"),
    (7, "sunday", -1, "День Военно-Морского Флота (День ВМФ)"),
    (8, "sunday", 1, "День железнодорожника"),
    (8, "saturday", 2, "День физкультурника"),
    (8, "sunday", 2, "День строителя"),
    (8, "sunday", -1, "День шахтёра"),
    (9, "sunday", 1, "День работников нефтяной и газовой промышленности"),
    (9, "sunday", 2, "День танкиста"),
    (9, "sunday", 3, "День работников леса"),
    (9, "sunday", -1, "День машиностроителя"),
    (10, "sunday", 2, "День работника сельского хозяйства"),
    (10, "sunday", 3, "День работников дорожного хозяйства"),
    (10, "sunday", -1, "День работника автомобильного и городского транспорта"),
    (11, "sunday", -1, "День матери"),
]

# ---------- ДНИ ВОИНСКОЙ СЛАВЫ (ФЗ №32-ФЗ ст. 1) ----------
MILITARY_GLORY_FIXED = [
    (1, 27, "Освобождение Ленинграда от блокады"),
    (2, 2, "Разгром немецких войск в Сталинградской битве"),
    (2, 23, "День защитника Отечества"),
    (4, 18, "Ледовое побоище (Победа на Чудском озере)"),
    (5, 9, "День Победы"),
    (5, 12, "Завершение Крымской наступательной операции"),
    (7, 7, "Победа русского флота в Чесменском сражении"),
    (7, 10, "Полтавская битва"),
    (8, 9, "Победа при Гангуте & Окончание Ленинградской битвы"),
    (8, 23, "Разгром немецких войск в Курской битве"),
    (9, 3, "Победа над Японией, окончание Второй мировой войны"),
    (9, 8, "Бородинское сражение"),
    (9, 11, "Победа у мыса Тендра"),
    (9, 21, "Куликовская битва"),
    (10, 9, "Разгром немецких войск в битве за Кавказ"),
    (11, 4, "День народного единства"),
    (11, 7, "Парад на Красной площади 1941 года"),
    (12, 1, "Победа при Синопе"),
    (12, 5, "Начало контрнаступления под Москвой"),
    (12, 24, "Взятие турецкой крепости Измаил"),
]

# ---------- ПАМЯТНЫЕ ДАТЫ РОССИИ (ФЗ №32-ФЗ ст. 1.1) ----------
MEMORABLE_DATES_FIXED = [
    (1, 25, "Татьянин день (День российского студенчества)"),
    (2, 15, "День памяти о россиянах, исполнявших служебный долг за пределами Отечества"),
    (3, 18, "День воссоединения Крыма с Россией"),
    (4, 9, "Штурм и взятие Кёнигсберга"),
    (4, 19, "День памяти жертв геноцида советского народа"),
    (4, 27, "День российского парламентаризма"),
    (6, 12, "День России"),
    (6, 22, "День памяти и скорби"),
    (6, 29, "День партизан и подпольщиков"),
    (7, 8, "День семьи, любви и верности"),
    (7, 28, "День Крещения Руси"),
    (8, 1, "День памяти российских воинов Первой мировой войны"),
    (9, 3, "День солидарности в борьбе с терроризмом"),
    (9, 30, "День воссоединения новых регионов с Россией"),
    (11, 7, "День Октябрьской революции 1917 года"),
    (11, 21, "День Военной присяги"),
    (12, 3, "День Неизвестного Солдата"),
    (12, 9, "День Героев Отечества"),
    (12, 12, "День Конституции РФ"),
]

def build_professional(year: int):
    entries = []
    for month, day, name in PROFESSIONAL_FIXED:
        entries.append((date(year, month, day), name))
    for month, weekday, occurrence, name in PROFESSIONAL_FLOATING:
        entries.append((nth_weekday(year, month, WEEKDAYS[weekday], occurrence), name))
    entries.append((day_of_year(year, 256), "День программиста"))
    return entries

def build_military_glory(year: int):
    return [(date(year, m, d), name) for m, d, name in MILITARY_GLORY_FIXED]

def build_memorable_dates(year: int):
    return [(date(year, m, d), name) for m, d, name in MEMORABLE_DATES_FIXED]

def write_category_file(folder: str, year: int, entries):
    entries.sort(key=lambda e: e[0])
    payload = [
        {"date": d.isoformat(), "name": name, "isPublic": False}
        for d, name in entries
    ]
    out_dir = os.path.join(REPO_DIR, folder, str(year))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "dates.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def generate():
    for year in range(YEAR_FROM, YEAR_TO + 1):
        prof = build_professional(year)
        mil = build_military_glory(year)
        mem = build_memorable_dates(year)

        # 1. Сохраняем по отдельным категориям для каталога
        write_category_file("professional", year, prof)
        write_category_file("military-glory", year, mil)
        write_category_file("memorable-dates", year, mem)

        # 2. Объединяем ВСЁ в единый быстрый файл holidays/YYYY/RU.json для Android!
        unified_map = {}
        for d, name in prof + mil + mem:
            d_str = d.isoformat()
            if d_str not in unified_map:
                unified_map[d_str] = []
            if name not in unified_map[d_str]:
                unified_map[d_str].append(name)

        unified_payload = []
        for d_str, names in sorted(unified_map.items()):
            for n in names:
                unified_payload.append({
                    "date": d_str,
                    "name": n,
                    "isPublic": False
                })

        ru_dir = os.path.join(REPO_DIR, "holidays", str(year))
        os.makedirs(ru_dir, exist_ok=True)
        ru_path = os.path.join(ru_dir, "RU.json")

        with open(ru_path, "w", encoding="utf-8") as f:
            json.dump(unified_payload, f, ensure_ascii=False, indent=2)

        print(f"Готово: {year} -> RU.json содержит {len(unified_payload)} памятных, военных и профессиональных дат!")

if __name__ == "__main__":
    generate()
