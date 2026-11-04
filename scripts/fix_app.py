def fix_app_py():
    path = "backend/app.py"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cut_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('@app.get("/languages"'):
            cut_idx = i
            break

    if cut_idx != -1:
        new_lines = lines[:cut_idx]
        new_tail = '''@app.get("/languages", tags=["Languages"])
async def get_supported_languages():
    """Returns list of supported international languages (English, Hindi, Marathi) and sample greetings."""
    return {
        "supported_count": 3,
        "primary_languages": [
            {"code": "en", "name": "English", "native": "English", "greeting": "Ask anything. Get intelligent answers."},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी", "greeting": "कुछ भी पूछें। समझदार और सटीक उत्तर पाएं।"},
            {"code": "mr", "name": "Marathi", "native": "मराठी", "greeting": "काहीही विचारा. बुद्धिमान आणि अचूक उत्तरे मिळवा."}
        ]
    }


# ─── Run Server ─────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            f.write(new_tail)
        print("backend/app.py cleanly truncated and updated.")

if __name__ == "__main__":
    fix_app_py()
