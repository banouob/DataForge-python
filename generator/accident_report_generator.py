from models.accident_case import AccidentCase
from service.vehicle_type_converter import VehicleTypeConverter
from service.injury_determinator import InjuryDeterminator
from service.report_formatter import ReportFormatter
from infrastructure import error_logger


class AccidentReportGenerator:
    def __init__(self):
        self._converter = VehicleTypeConverter()
        self._determinator = InjuryDeterminator()
        self._formatter = ReportFormatter()
        error_logger.log_info(
            f"AccidentReportGenerator 初始化完成 (車種對應規則數量: {self._converter.mapping_count()})"
        )

    def generate_report(self, case: AccidentCase) -> str:
        if not case.is_valid():
            return "錯誤：案件資料無效"
        if not case.persons:
            return "錯誤：沒有當事人資料"

        # 步驟 1：轉換車種
        for person in case.persons:
            person.vehicle_type = self._converter.convert(person.vehicle_type)

        # 步驟 2：判斷傷者
        injured = self._determinator.determine_injured(case.persons)

        # 步驟 3：格式化文字
        persons_text = self._formatter.format_persons_text(case.persons)
        injured_text = self._formatter.format_injured_text(injured)

        # 步驟 4：組合報告
        report = (
            f"處理員警回報：本案乃{persons_text}，發生交通事故，"
            f"{injured_text}受傷，依A2交通事故處理。"
            f"交通事故案號：{case.case_number}。"
        )

        error_logger.log_info(f"報告生成成功（案號: {case.case_number}）")
        return report
