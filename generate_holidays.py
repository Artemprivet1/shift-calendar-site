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

def add_holiday(holiday_map, d_str, name, is_public):
    if not name:
        return
    clean_name = str(name).strip()
    
    if d_str not in holiday_map:
        holiday_map[d_str] = {
            "date": d_str,
            "names": [clean_name],
            "isPublic": is_public
        }
    else:
        # Объединяем названия без дубликатов
        if clean_name not in holiday_map[d_str]["names"]:
            holiday_map[d_str]["names"].append(clean_name)
        # Если хотя бы один праздник на эту дату официальный — статус True сохраняется
        if is_public:
            holiday_map[d_str]["isPublic"] = True

def generate():
    total_files = 0
    all_cats = getattr(holidays, 'ALL_CATEGORIES', None)

    for year in YEARS:
        year_dir = os.path.join(REPO_DIR, "holidays", str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        for country in COUNTRIES:
            holiday_map = {}
            
            # 1. Сначала извлекаем официальные государственные праздники (isPublic = True)
            try:
                base_public = holidays.country_holidays(country, years=year, observed=True)
                for h_date, h_name in base_public.items():
                    d_str = h_date.isoformat()
                    add_holiday(holiday_map, d_str, h_name, is_public=True)
            except Exception:
                pass

            # 2. Извлекаем ВСЕ категории (памятные даты, обычаи, банк. дни)
            try:
                if all_cats is not None:
                    base_all = holidays.country_holidays(country, years=year, observed=True, categories=all_cats)
                    for h_date, h_name in base_all.items():
                        d_str = h_date.isoformat()
                        add_holiday(holiday_map, d_str, h_name, is_public=False)
            except Exception:
                pass
                
            # 3. Извлекаем праздники ВСЕХ регионов/субъектов/провинций (subdivisions)
            try:
                country_obj = holidays.country_holidays(country)
                subdivs = getattr(country_obj, 'subdivisions', []) or []
                
                for s in subdivs:
                    try:
                        if all_cats is not None:
                            sub_hols = holidays.country_holidays(country, subdiv=s, years=year, observed=True, categories=all_cats)
                        else:
                            sub_hols = holidays.country_holidays(country, subdiv=s, years=year, observed=True)
                        
                        for h_date, h_name in sub_hols.items():
                            d_str = h_date.isoformat()
                            add_holiday(holiday_map, d_str, h_name, is_public=False)
                    except Exception:
                        continue
            except Exception:
                pass
            
            # Формируем финальный список с объединенными названиями через " / "
            holiday_list = []
            for item in holiday_map.values():
                holiday_list.append({
                    "date": item["date"],
                    "name": " / ".join(item["names"]),
                    "isPublic": item["isPublic"]
                })
            
            # Сортируем по возрастанию даты
            holiday_list.sort(key=lambda x: x["date"])
            
            # Записываем чистый UTF-8 JSON без BOM
            file_path = os.path.join(year_dir, f"{country}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(holiday_list, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Успешно сгенерировано {total_files} файлов со слиянием дат и регионами!")

if __name__ == "__main__":
    generate()
