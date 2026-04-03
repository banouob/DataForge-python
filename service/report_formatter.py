from typing import List
from models.person import Person
from infrastructure import error_logger


class ReportFormatter:
    """
    格式化規則：
    - 髒資料（name 空）    → vehicle_type
    - 髒資料（name 有值）  → name + vehicle_type
    - 行人 / 醫療代步車    → name + vehicle_type（不加「駕駛」）
    - 無車牌               → name駕駛vehicle_type
    - 有車牌               → name駕駛license_plate號vehicle_type
    多人用「與」連接；傷者用「、」連接
    """

    def format_persons_text(self, persons: List[Person]) -> str:
        parts: List[str] = []

        for person in persons:
            vtype = person.vehicle_type

            if person.is_dirty_data():
                if not person.name:
                    formatted = vtype
                else:
                    formatted = person.name + vtype
                error_logger.log_info(f"格式化髒資料: {formatted}")

            elif vtype in ("行人", "醫療代步車"):
                formatted = f"{person.name}{vtype}"
                error_logger.log_info(f"格式化當事人（行人/代步車）: {formatted}")

            elif person.has_no_license_plate():
                formatted = f"{person.name}駕駛{vtype}"
                error_logger.log_info(f"格式化當事人（無車牌）: {formatted}")

            else:
                formatted = f"{person.name}駕駛{person.license_plate}號{vtype}"
                error_logger.log_info(f"格式化當事人（有車牌）: {formatted}")

            parts.append(formatted)

        return "與".join(parts)

    def format_injured_text(self, injured: List[str]) -> str:
        if not injured:
            return "(無傷者)"
        return "、".join(injured)
