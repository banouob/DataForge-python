from typing import List
from infrastructure.config_manager import ConfigManager
from converter import doc_extractor
from converter.json_case_parser import parse_json
from generator.accident_report_generator import AccidentReportGenerator
from infrastructure import error_logger


class ProcessingController:
    def __init__(self, config: ConfigManager):
        self._config = config
        self._generator = AccidentReportGenerator()

    def process_files(self, file_paths: List[str]) -> List[str]:
        results: List[str] = []
        for path in file_paths:
            result = self._process_file(path)
            results.append(result)
        return results

    def _process_file(self, file_path: str) -> str:
        try:
            error_logger.log_info(f"開始處理: {file_path}")

            # 步驟 A+B：.doc → JSON
            target_dir = None
            if self._config.is_json_output_enabled():
                target_dir = self._config.get_json_output_path()
            json_str = doc_extractor.extract_to_json(file_path, target_dir)

            # 步驟 C：JSON → AccidentCase
            case = parse_json(json_str)

            # 步驟 D：生成報告
            report = self._generator.generate_report(case)
            error_logger.log_info(f"處理完成: {file_path}")
            return report

        except Exception as e:
            msg = f"處理失敗 [{file_path}]: {e}"
            error_logger.log_error(msg, exc=e)
            return f"錯誤：{e}"
