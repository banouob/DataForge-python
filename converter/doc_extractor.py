"""
.doc 直接提取器（使用 aspose.words）

aspose.words 以 doc.get_text() 輸出文件全文，
其中表格儲存格以 \u0007 (\x07) 分隔。
案件編號與當事人資料皆可透過分割 \x07 取得。
"""
import os
import re
import json
from pathlib import Path

import aspose.words as aw

from infrastructure import error_logger

# 案件編號格式：5 位數字 + 2 大寫字母 + 至少 1 位數字（例：11504BT491B0082）
CASE_NUMBER_PATTERN = re.compile(r'^\d{5}[A-Z]{2}\d')


def extract_to_json(doc_file: str, target_directory: str = None) -> str:
    doc = aw.Document(doc_file)
    full_text = doc.get_text()

    # 以 \x07 分割所有儲存格，清除 \r / \n
    cells = [c.replace('\r', '').replace('\n', '').strip() for c in full_text.split('\x07')]
    error_logger.log_info(f"共 {len(cells)} 個 cell")

    case_number = _extract_case_number(cells)
    party_list = _extract_parties(cells)

    data = {"編號": case_number, "當事人車輛資訊": party_list}
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    error_logger.log_info(f"成功提取 JSON (長度: {len(json_str)} 字元)")
    error_logger.log_info(f"JSON 內容:\n{json_str}")

    if target_directory:
        Path(target_directory).mkdir(parents=True, exist_ok=True)
        base_name = Path(doc_file).stem
        json_path = Path(target_directory) / f"{base_name}.json"
        json_path.write_text(json_str, encoding='utf-8')
        error_logger.log_info(f"JSON 已保存: {json_path}")

    return json_str


def _extract_case_number(cells: list) -> str:
    for cell in cells:
        if CASE_NUMBER_PATTERN.match(cell):
            error_logger.log_info(f"提取到編號: {cell}")
            return cell
    error_logger.log_warning("未找到案件編號")
    return ""


def _extract_parties(cells: list) -> list:
    party_list = []
    i = 0
    while i < len(cells):
        seq = cells[i]
        # 遇到純數字（順序號）且後面還有至少 4 格
        if seq.isdigit() and i + 4 < len(cells):
            name    = cells[i + 1]
            plate   = cells[i + 2]
            vehicle = cells[i + 3]
            remark  = cells[i + 4]

            # 至少姓名或車牌有值才視為有效資料行
            if name or plate:
                party = {
                    "順序": seq,
                    "當事人姓名": name,
                    "車牌號碼": plate,
                    "車種": vehicle,
                    "備註": remark,
                }
                party_list.append(party)
                error_logger.log_info(
                    f"提取當事人: 順序=[{seq}], 姓名=[{name}], 車牌=[{plate}], "
                    f"車種=[{vehicle}], 備註=[{remark}]"
                )

                i += 5
                # 跳過列尾空格（Word 每列有額外一個列尾 cell）
                if i < len(cells) and not cells[i]:
                    i += 1
                continue
        i += 1

    if not party_list:
        error_logger.log_warning("未找到有效當事人資料")

    return party_list
