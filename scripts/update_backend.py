import re

def update_app_py():
    path = "backend/app.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'@app\.get\("/languages".*?def get_supported_languages\(\):.*?return \{.*?\}'
    replacement = '''@app.get("/languages", tags=["Languages"])
async def get_supported_languages():
    """Returns list of supported international languages (English, Hindi, Marathi) and sample greetings."""
    return {
        "supported_count": 3,
        "primary_languages": [
            {"code": "en", "name": "English", "native": "English", "greeting": "Ask anything. Get intelligent answers."},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी", "greeting": "कुछ भी पूछें। समझदार और सटीक उत्तर पाएं।"},
            {"code": "mr", "name": "Marathi", "native": "मराठी", "greeting": "काहीही विचारा. बुद्धिमान आणि अचूक उत्तरे मिळवा."}
        ]
    }'''
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("backend/app.py /languages endpoint updated successfully.")
    else:
        print("Warning: /languages pattern not matched in backend/app.py")

if __name__ == "__main__":
    update_app_py()
