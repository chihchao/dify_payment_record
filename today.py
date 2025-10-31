from datetime import datetime

def main():
    return {
        "today": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
