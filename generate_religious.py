import os
import json
import datetime

REPO_DIR = r"C:\Users\dastl\shift-calendar-site"
YEARS = range(2025, 2032) # 2025–2031

# 1. Алгоритм расчета Православной Пасхи (Александрийская пасхалия)
def get_orthodox_easter(year):
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    julian_date = datetime.date(year, month, day)
    # Поправка юлианского календаря для XX-XXI веков (+13 дней)
    return julian_date + datetime.timedelta(days=13)

# 2. Алгоритм расчета Католической Пасхи (Григорианский календарь)
def get_catholic_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

# 3. Астрономический календарь исламских праздников (2025–2031)
ISLAMIC_DATA = {
    2025: [
        ("2025-03-01", "Начало священного месяца Рамадан"),
        ("2025-03-26", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2025-03-30", "Ураза-байрам (Ид аль-Фитр)"),
        ("2025-06-05", "День Арафат"),
        ("2025-06-06", "Курбан-байрам (Ид аль-Адха)"),
        ("2025-06-26", "Мусульманский Новый год (1 Мухаррам)"),
        ("2025-07-05", "День Ашура"),
        ("2025-09-04", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2026: [
        ("2026-02-18", "Начало священного месяца Рамадан"),
        ("2026-03-15", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2026-03-20", "Ураза-байрам (Ид аль-Фитр)"),
        ("2026-05-26", "День Арафат"),
        ("2026-05-27", "Курбан-байрам (Ид аль-Адха)"),
        ("2026-06-16", "Мусульманский Новый год (1 Мухаррам)"),
        ("2026-06-25", "День Ашура"),
        ("2026-08-25", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2027: [
        ("2027-02-08", "Начало священного месяца Рамадан"),
        ("2027-03-05", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2027-03-10", "Ураза-байрам (Ид аль-Фитр)"),
        ("2027-05-15", "День Арафат"),
        ("2027-05-16", "Курбан-байрам (Ид аль-Адха)"),
        ("2027-06-06", "Мусульманский Новый год (1 Мухаррам)"),
        ("2027-06-15", "День Ашура"),
        ("2027-08-14", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2028: [
        ("2028-01-28", "Начало священного месяца Рамадан"),
        ("2028-02-23", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2028-02-27", "Ураза-байрам (Ид аль-Фитр)"),
        ("2028-05-04", "День Арафат"),
        ("2028-05-05", "Курбан-байрам (Ид аль-Адха)"),
        ("2028-05-25", "Мусульманский Новый год (1 Мухаррам)"),
        ("2028-06-03", "День Ашура"),
        ("2028-08-02", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2029: [
        ("2029-01-16", "Начало священного месяца Рамадан"),
        ("2029-02-11", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2029-02-15", "Ураза-байрам (Ид аль-Фитр)"),
        ("2029-04-23", "День Арафат"),
        ("2029-04-24", "Курбан-байрам (Ид аль-Адха)"),
        ("2029-05-14", "Мусульманский Новый год (1 Мухаррам)"),
        ("2029-05-23", "День Ашура"),
        ("2029-07-23", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2030: [
        ("2030-01-06", "Начало священного месяца Рамадан"),
        ("2030-02-01", "Ночь Предопределения (Ляйлят аль-Кадр)"),
        ("2030-02-05", "Ураза-байрам (Ид аль-Фитр)"),
        ("2030-04-12", "День Арафат"),
        ("2030-04-13", "Курбан-байрам (Ид аль-Адха)"),
        ("2030-05-03", "Мусульманский Новый год (1 Мухаррам)"),
        ("2030-05-12", "День Ашура"),
        ("2030-07-12", "Мавлид ан-Наби (Рождение Пророка)")
    ],
    2031: [
        ("2031-01-25", "Ураза-байрам (Ид аль-Фитр)"),
        ("2031-04-01", "День Арафат"),
        ("2031-04-02", "Курбан-байрам (Ид аль-Адха)"),
        ("2031-04-23", "Мусульманский Новый год (1 Мухаррам)"),
        ("2031-05-02", "День Ашура"),
        ("2031-07-02", "Мавлид ан-Наби (Рождение Пророка)"),
        ("2031-12-16", "Начало священного месяца Рамадан")
    ]
}

def generate_orthodox(year):
    easter = get_orthodox_easter(year)
    items = [
        # Плавающие праздники пасхального цикла
        (easter - datetime.timedelta(days=7), "Вход Господень в Иерусалим (Вербное воскресенье)"),
        (easter - datetime.timedelta(days=3), "Великий (Чистый) четверг"),
        (easter - datetime.timedelta(days=2), "Великая (Страстная) пятница"),
        (easter, "Пасха Христова (Светлое Христово Воскресение)"),
        (easter + datetime.timedelta(days=9), "Радоница (День поминовения усопших)"),
        (easter + datetime.timedelta(days=39), "Вознесение Господне"),
        (easter + datetime.timedelta(days=49), "День Святой Троицы (Пятидесятница)"),
        (easter + datetime.timedelta(days=50), "День Святого Духа"),
        
        # Непереходящие великие и двунадесятые праздники
        (datetime.date(year, 1, 7), "Рождество Христово"),
        (datetime.date(year, 1, 14), "Обрезание Господне"),
        (datetime.date(year, 1, 19), "Крещение Господне (Богоявление)"),
        (datetime.date(year, 2, 15), "Сретение Господне"),
        (datetime.date(year, 4, 7), "Благовещение Пресвятой Богородицы"),
        (datetime.date(year, 5, 22), "День памяти святителя Николая Чудотворца (весенний)"),
        (datetime.date(year, 7, 12), "День святых апостолов Петра и Павла"),
        (datetime.date(year, 8, 19), "Преображение Господне (Яблочный Спас)"),
        (datetime.date(year, 8, 28), "Успение Пресвятой Богородицы"),
        (datetime.date(year, 9, 11), "Усекновение главы Иоанна Предтечи"),
        (datetime.date(year, 9, 21), "Рождество Пресвятой Богородицы"),
        (datetime.date(year, 9, 27), "Воздвижение Креста Господня"),
        (datetime.date(year, 10, 14), "Покров Пресвятой Богородицы"),
        (datetime.date(year, 12, 4), "Введение во храм Пресвятой Богородицы"),
        (datetime.date(year, 12, 19), "День святителя Николая Чудотворца (зимний)")
    ]
    
    result = [{"date": d.isoformat(), "name": name, "isPublic": False} for d, name in items]
    result.sort(key=lambda x: x["date"])
    return result

def generate_catholic(year):
    easter = get_catholic_easter(year)
    items = [
        (easter - datetime.timedelta(days=46), "Пепельная среда"),
        (easter - datetime.timedelta(days=7), "Пальмовое (Вербное) воскресенье"),
        (easter - datetime.timedelta(days=2), "Страстная пятница"),
        (easter, "Пасха (Воскресение Господне)"),
        (easter + datetime.timedelta(days=1), "Пасхальный понедельник"),
        (easter + datetime.timedelta(days=39), "Вознесение Господне"),
        (easter + datetime.timedelta(days=49), "Пятидесятница (Сошествие Святого Духа)"),
        (easter + datetime.timedelta(days=60), "Праздник Тела и Крови Христовых"),
        (datetime.date(year, 8, 15), "Успение Пресвятой Богородицы"),
        (datetime.date(year, 11, 1), "День всех святых"),
        (datetime.date(year, 12, 8), "Торжество Непорочного Зачатия Девы Марии"),
        (datetime.date(year, 12, 25), "Рождество Христово (католическое)"),
        (datetime.date(year, 12, 26), "День святого Стефана")
    ]
    result = [{"date": d.isoformat(), "name": name, "isPublic": False} for d, name in items]
    result.sort(key=lambda x: x["date"])
    return result

def generate_islamic(year):
    items = ISLAMIC_DATA.get(year, [])
    result = [{"date": d_str, "name": name, "isPublic": False} for d_str, name in items]
    result.sort(key=lambda x: x["date"])
    return result

def main():
    rel_dir = os.path.join(REPO_DIR, "holidays", "religious")
    os.makedirs(rel_dir, exist_ok=True)
    
    total = 0
    for year in YEARS:
        year_sub_dir = os.path.join(rel_dir, str(year))
        os.makedirs(year_sub_dir, exist_ok=True)
        
        orth = generate_orthodox(year)
        cath = generate_catholic(year)
        islam = generate_islamic(year)
        
        # 1. Записываем структурированные файлы по конфессиям
        for name, data in [("orthodox", orth), ("catholic", cath), ("islamic", islam)]:
            # Формат: holidays/religious/2026/orthodox.json
            with open(os.path.join(year_sub_dir, f"{name}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # Формат: holidays/religious/orthodox_2026.json (для универсальной совместимости)
            with open(os.path.join(rel_dir, f"{name}_{year}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            total += 2
            
        # 2. Формат по умолчанию: holidays/religious/2026.json (Православие)
        with open(os.path.join(rel_dir, f"{year}.json"), "w", encoding="utf-8") as f:
            json.dump(orth, f, ensure_ascii=False, indent=2)
        total += 1

    print(f"Готово! Сгенерировано {total} файлов религиозных праздников на 2025–2031 годы!")

if __name__ == "__main__":
    main()
