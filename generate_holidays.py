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

def generate():
    total_files = 0
    all_cats = getattr(holidays, 'ALL_CATEGORIES', None)

    for year in YEARS:
        year_dir = os.path.join(REPO_DIR, "holidays", str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        for country in COUNTRIES:
            holiday_dict = {}
            
            # 1. Запрашиваем общегосударственные праздники со всеми категориями
            try:
                if all_cats is not None:
                    base_hols = holidays.country_holidays(country, years=year, observed=True, categories=all_cats)
                else:
                    base_hols = holidays.country_holidays(country, years=year, observed=True)
                
                for h_date, h_name in base_hols.items():
                    d_str = h_date.isoformat()
                    holiday_dict[d_str] = {
                        "date": d_str,
                        "name": str(h_name),
                        "isPublic": True
                    }
            except Exception:
                pass
                
            # 2. Автоматически опрашиваем ВСЕ регионы, провинции и штаты страны
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
                            if d_str not in holiday_dict:
                                holiday_dict[d_str] = {
                                    "date": d_str,
                                    "name": str(h_name),
                                    "isPublic": False
                                }
                    except Exception:
                        continue
            except Exception:
                pass
            
            # Сортируем полученный список дат
            holiday_list = list(holiday_dict.values())
            holiday_list.sort(key=lambda x: x["date"])
            
            # Записываем чистый UTF-8 JSON без BOM
            file_path = os.path.join(year_dir, f"{country}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(holiday_list, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Готово! Все {total_files} файлов созданы строго через единый алгоритм (со всеми провинциями, штатами и категориями)!")

if __name__ == "__main__":
    generate()
