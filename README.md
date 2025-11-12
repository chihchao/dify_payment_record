# dify_payment_record

## Prompt

### Payment Record

- [payment.md](payment.md)

## Code

### Google 試算表 API

```
/**
 * 這是 Google Apps Script 專案的腳本檔案。
 * 用於處理 POST 請求，將 JSON 資料寫入 Google 試算表。
 *
 * 部署步驟：
 * 1. 儲存腳本。
 * 2. 點擊「部署」 -> 「新增部署作業」。
 * 3. 選擇類型為「網路應用程式」。
 * 4. 執行身分選擇「我」。
 * 5. 存取權限設定為「任何人」。
 * 6. 點擊「部署」，並授予必要的權限。
 * 7. 複製產生的網址，這就是您的 API Endpoint。
 */

// 定義目標工作表的名稱
const SHEET_NAME = "紀錄";

/**
 * 處理 POST 請求。
 * 接收 JSON 資料並將其新增到試算表中。
 *
 * 預期 JSON 格式：
 * {
 * "Amount": 75,
 * "Item": "咖啡",
 * "Date": "2025-10-30",
 * "Payment": "Line Pay",
 * "Category": "食",
 * "Store": "星巴克",
 * "Memo": ""
 * }
 *
 * @param {Object} e 包含 POST 請求資料的事件物件
 * @returns {GoogleAppsScript.Content.TextOutput} JSON 格式的回覆
 */
function doPost(e) {
  // 設定回覆內容的類型為 JSON
  const responseHeaders = {
    'Content-Type': 'application/json'
  };

  try {
    // 檢查是否有傳入資料
    if (!e || !e.postData) {
      return createJsonResponse({
        success: false,
        message: "錯誤：未提供 POST 請求資料。"
      });
    }

    // 解析傳入的 JSON 字串
    const data = JSON.parse(e.postData.contents);

    // 驗證必要的欄位是否存在
    const requiredFields = ["Amount", "Item", "Date", "Payment", "Category", "Store", "Memo"];
    for (let field of requiredFields) {
      if (!(field in data)) {
        return createJsonResponse({
          success: false,
          message: `錯誤：JSON 缺少必要欄位 "${field}"。`
        });
      }
    }

    // 取得試算表和目標工作表
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME);

    if (!sheet) {
      return createJsonResponse({
        success: false,
        message: `錯誤：找不到名為 "${SHEET_NAME}" 的工作表。請檢查工作表名稱是否正確。`
      });
    }

    // 依照試算表欄位的順序，建立要寫入的資料列
    // 假設試算表的欄位順序為：日期, 品項, 金額, 付款方式, 類別, 商店, 備註
    const newRow = [
      data.Date,
      data.Item,
      data.Amount,
      data.Payment,
      data.Category,
      data.Store,
      data.Memo
    ];

    // 將資料新增到工作表的新的一行
    sheet.appendRow(newRow);

    // 成功回覆
    return createJsonResponse({
      success: true,
      message: "資料已成功寫入試算表。",
      data: data
    });

  } catch (error) {
    // 處理錯誤，例如 JSON 解析失敗、寫入錯誤等
    Logger.log("執行 doPost 時發生錯誤：" + error.toString());
    return createJsonResponse({
      success: false,
      message: "處理請求時發生系統錯誤。",
      error: error.message
    });
  }
}

/**
 * 輔助函數：建立 JSON 格式的回覆物件。
 * @param {Object} obj 要轉換成 JSON 的物件
 * @returns {GoogleAppsScript.Content.TextOutput}
 */
function createJsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### Get Today

```python
from datetime import datetime

def main():
    return {
        "today": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
```

### Extract JSON

```python
import re
import json

def extract_json_from_response(response_text):
    # 正規表達式來尋找 JSON 程式碼區塊。
    # re.DOTALL 確保 '.' 能匹配換行符，以便處理多行 JSON。
    # (.*?) 是非貪婪匹配，用於捕捉 ```json 和 ``` 之間的所有內容。
    json_block_pattern = re.compile(r"```json\s*\n(.*?)\n\s*```", re.DOTALL)
    
    match = json_block_pattern.search(response_text)
    
    if match:
        json_string = match.group(1).strip()
        try:
            # 嘗試將提取的字串解析為 JSON 物件
            parsed_json = json.loads(json_string)
            # 將物件轉為 JSON 字串並回傳
            return json.dumps(parsed_json, ensure_ascii=False)
        except json.JSONDecodeError as e:
            # 如果解析失敗，表示雖然找到標記，但內容不是有效的 JSON
            return None
    else:
        # 如果沒有找到匹配的 JSON 程式碼區塊
        return None


def main(arg1: str):
    return {
        "result": extract_json_from_response(arg1),
    }

```


