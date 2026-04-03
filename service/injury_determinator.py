from typing import List
from models.person import Person
from infrastructure import error_logger


class InjuryDeterminator:
    """
    判斷傷者優先順序：
    A. 乘客（備註含「乘客」）
    B. 弱勢方（機車、慢車、人）
    C. 不確定方（機動車駕駛）→ 加入「(自行填寫)」
    D. 忽略（髒資料）
    """

    def determine_injured(self, persons: List[Person]) -> List[str]:
        injured: List[str] = []

        for person in persons:
            # D. 髒資料忽略
            if person.is_dirty_data():
                error_logger.log_info(f"忽略髒資料（不加入傷者）: {person.vehicle_type}")
                continue

            remarks = person.remarks or ""
            vehicle_type = person.vehicle_type or ""

            # A. 乘客
            if "乘客" in remarks:
                injured.append(person.name)
                error_logger.log_info(f"判定為傷者（乘客）: {person.name}")
                continue

            # B. 弱勢方
            if self._is_vulnerable(vehicle_type):
                injured.append(person.name)
                error_logger.log_info(f"判定為傷者（弱勢方）: {person.name} [{vehicle_type}]")
                continue

            # C. 機動車駕駛
            if self._is_motor_vehicle(vehicle_type):
                injured.append("(自行填寫)")
                error_logger.log_info(f"判定為不確定傷者（機動車駕駛）: {person.name} [{vehicle_type}]")

        return injured

    def _is_vulnerable(self, vehicle_type: str) -> bool:
        if not vehicle_type:
            return False
        if "機車" in vehicle_type or "重機" in vehicle_type:
            return True
        if ("腳踏" in vehicle_type or "自行車" in vehicle_type
                or "電動二輪" in vehicle_type or "電動輔助" in vehicle_type):
            return True
        if "行人" in vehicle_type or "代步" in vehicle_type:
            return True
        return False

    def _is_motor_vehicle(self, vehicle_type: str) -> bool:
        if not vehicle_type:
            return False
        if "客" in vehicle_type and "乘客" not in vehicle_type:
            return True
        if "貨" in vehicle_type:
            return True
        if "曳引" in vehicle_type:
            return True
        if "聯結" in vehicle_type:
            return True
        return False
