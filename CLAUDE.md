# CLAUDE.md

本文件為 Claude Code（claude.ai/code）在此儲存庫中運作時提供指引。

## 使用中文與我對話

## 專案概述

DataForge 是一套交通事故案件處理系統（Java 專案的 Python 移植版）。它透過 Tkinter GUI，處理包含事故案件資料的 Word 文件（`.doc`），並產生繁體中文格式的事故報告。

## 執行應用程式

```bash
pip install -r requirements.txt
python main.py
```

`main.py` 在匯入前會設定 `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1`（Windows 上執行 aspose.words 的必要設定），並啟動 Tkinter GUI。

本專案目前無測試套件、Linter 設定或建置腳本。

## 架構

處理流程依序通過以下各層：

```
UI（file_chooser_service.py）
  → ProcessingController          # 協調 檔案 → JSON → 案件 → 報告 的流程
      → DocExtractor              # aspose.words：從 .doc 表格欄位（以 \x07 分隔）提取案號與當事人資訊
      → JsonCaseParser            # JSON → AccidentCase 模型；偵測髒資料（缺少車牌/車種）
      → AccidentReportGenerator   # 協調資料豐富化服務
          → VehicleTypeConverter  # 依 vehicle-types.properties 正規化車種名稱
          → InjuryDeterminator    # 依車種判斷受傷當事人
          → ReportFormatter       # 格式化當事人資訊與傷亡說明文字
```

**模型**：`AccidentCase` 包含 `case_number` 與 `List[Person]`；`Person` 包含姓名、車牌號碼、車種、備註。

**基礎設施**：`ConfigManager` 載入 `config.properties`；`ErrorLogger` 將帶時間戳記的條目寫入 `error.log`。

## 設定檔

| 檔案 | 用途 |
|------|------|
| `config.properties` | 控制 JSON 輸出（啟用/停用、輸出目錄） |
| `vehicle-types.properties` | 將原始車種字串對應至正規化值（56 筆對應） |

## 主要相依套件

`aspose-words==26.3.0` — 唯一的外部相依套件，用於 `.doc` 文件解析。商業授權套件；正式環境使用需有效授權。
