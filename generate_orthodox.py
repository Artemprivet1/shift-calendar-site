import json
import os
from datetime import date, timedelta

REPO_DIR = r"C:\Users\dastl\shift-calendar-site"
YEAR_FROM = 2025
YEAR_TO = 2036

def orthodox_easter(year: int) -> date:
    """Дата православной Пасхи в григорианском календаре (Гаусс-Мееус)."""
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = (d + e + 114) % 31 + 1
    julian_date = date(year, month, day)
    return julian_date + timedelta(days=13)

# Фиксированные непереходящие праздники
FIXED_FEASTS = [
    (1, 7, "Рождество Христово"),
    (1, 19, "Крещение Господне (Богоявление)"),
    (2, 15, "Сретение Господне"),
    (4, 7, "Благовещение Пресвятой Богородицы"),
    (8, 2, "Ильин день"),
    (8, 14, "Медовый Спас"),
    (8, 19, "Яблочный Спас (Преображение Господне)"),
    (8, 28, "Успение Пресвятой Богородицы"),
    (8, 29, "Ореховый (Хлебный) Спас"),
    (9, 21, "Рождество Пресвятой Богородицы"),
    (9, 27, "Воздвижение Креста Господня"),
    (10, 14, "Покров Пресвятой Богородицы"),
    (12, 4, "Введение во храм Пресвятой Богородицы"),
    (12, 19, "День святителя Николая Чудотворца")
]

# Переходящие праздники (смещение от Пасхи)
EASTER_OFFSET_FEASTS = [
    (-55, "Масленица (начало Сырной седмицы)"),
    (-49, "Прощёное воскресенье"),
    (-48, "Чистый понедельник (начало Великого поста)"),
    (-7, "Вербное воскресенье (Вход Господень в Иерусалим)"),
    (0, "Пасха Христова (Светлое Христово Воскресение)"),
    (9, "Радоница (День поминовения усопших)"),
    (39, "Вознесение Господне"),
    (48, "Троицкая родительская суббота"),
    (49, "День Святой Троицы (Пятидесятница)"),
]

def build_year(year: int):
    entries = []
    for month, day, name in FIXED_FEASTS:
        entries.append((date(year, month, day), name))

    easter = orthodox_easter(year)
    for offset, name in EASTER_OFFSET_FEASTS:
        entries.append((easter + timedelta(days=offset), name))

    entries.sort(key=lambda e: e[0])
    return [
        {"date": d.isoformat(), "name": name, "isPublic": False, "isReligious": True}
        for d, name in entries
    ]

def generate():
    for year in range(YEAR_FROM, YEAR_TO + 1):
        out_dir = os.path.join(REPO_DIR, "holidays", "religious", str(year))
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "orthodox.json")
        
        payload = build_year(year)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Готово: {year} -> {len(payload)} праздников")

if __name__ == "__main__":
    generate()
