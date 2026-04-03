import json
from models.accident_case import AccidentCase
from models.person import Person
from infrastructure import error_logger


def parse_json(json_str: str) -> AccidentCase:
    case = AccidentCase()
    data = json.loads(json_str)

    case.case_number = data.get("編號", "").strip()
    if not case.case_number:
        error_logger.log_warning("JSON 中未找到案件編號")

    party_array = data.get("當事人車輛資訊", [])
    for item in party_array:
        name    = item.get("當事人姓名", "").strip()
        plate   = item.get("車牌號碼", "").strip()
        vehicle = item.get("車種", "").strip()
        remark  = item.get("備註", "").strip()

        person = Person(name=name, license_plate=plate, vehicle_type=vehicle, remarks=remark)

        # 髒資料偵測：車牌和車種都為空時，name 移至 vehicle_type
        if not plate and not vehicle:
            person.vehicle_type = name
            person.name = ""
            person.set_dirty_data(True)
            error_logger.log_warning(f"偵測到髒資料: {name}")
        else:
            error_logger.log_info(f"解析當事人: {name} [{vehicle}] {plate}")

        case.add_person(person)

    return case
