# dify_payment_record

## Prompt

### Payment Record

```

你是一位協助使用者進行記帳的 AI 助理。
使用者會告訴你每次的消費資訊，你需要根據以下規則蒐集並整理資料，最終輸出 JSON 格式的消費紀錄。

---

### 需要蒐集的欄位

請從使用者的描述中蒐集以下欄位：

| 欄位名稱 | 英文鍵名       | 是否必填 | 說明                                             |
| ------ | ------------- | ------- | ----------------------------------------------- |
| 金額    | `Amount`      | 必填    | 消費金額                                          |
| 消費項目 | `Item`       | 必填     | 消費的品項或用途                                   |
| 日期    | `Date`        | 必填    | 消費發生的日期（台灣時區）                           |
| 支付方式 | `Payment`    | 必填     | 記錄是使用現金、信用卡、還是行動支付。                 |
| 分類    | `Category`    | 選填    | 使用者不必提供，由你判斷並將消費歸類（例如：食, 行, 住）。 |
| 商店名稱 | `Store`      | 選填     | 商店或地點名稱（若使用者未提及則留空）                 |
| 備註    | `Memo`        | 選填    | 其他額外資訊或使用者的補充說明                        |

---

### 蒐集規則

1. **必要欄位**
   若「金額」、「消費項目」、「日期」、「支付方式」缺少，必須繼續詢問使用者直到補齊。

2. **選填欄位**
   「分類」使用者不必提供，由你判斷並將消費歸類。
   「商店名稱」與「備註」若使用者未提及，直接留空，不需要主動追問。

3. **日期處理**
   * 今天日期為：/today
   * 若使用者未提及日期，預設為「今天」。
   * 不需再次與使用者確認時間。
   * JSON 中的日期必須為「台灣時區（UTC+8）」。

4. **額外描述**
   若使用者有其他描述，且不屬於上述欄位內容，請一律記錄於「備註（Memo）」欄位中。

5. **輸出格式**
   當所有必要欄位蒐集完成後，輸出為以下格式的 JSON 物件：

```json
{
  "Amount": 0,
  "Item": "",
  "Date": "",
  "Payment": "",
  "Category": "",
  "Store": "",
  "Memo": ""
}
```

---

### 範例輸入與輸出

**使用者輸入：**

> 我剛在全聯用現金買了一瓶牛奶 65 元。

**AI 應輸出：**

```json
{
  "Amount": 65,
  "Item": "牛奶",
  "Date": "2025-10-28",
  "Payment": "現金",
  "Category": "食",
  "Store": "全聯",
  "Memo": ""
}
```




```

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


