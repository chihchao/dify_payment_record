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
