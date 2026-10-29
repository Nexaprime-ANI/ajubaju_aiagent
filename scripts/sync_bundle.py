import os
import re

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
frontend_dir = os.path.join(repo_root, "frontend")
dest_file = os.path.join(frontend_dir, "bundled.html")

with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

with open(os.path.join(frontend_dir, "style.css"), "r", encoding="utf-8") as f:
    css = f.read()

with open(os.path.join(frontend_dir, "script.js"), "r", encoding="utf-8") as f:
    js = f.read()

# Replace stylesheet link tag using lambda to avoid regex escape errors
bundled = re.sub(
    r'<link\s+rel="stylesheet"\s+href="style\.css[^"]*"\s*>',
    lambda m: f"<style>\n{css}\n</style>",
    html,
    flags=re.IGNORECASE
)

# Replace script tag using lambda to avoid regex escape errors
bundled = re.sub(
    r'<script\s+src="script\.js[^"]*"\s*>\s*</script>',
    lambda m: f"<script>\n{js}\n</script>",
    bundled,
    flags=re.IGNORECASE
)

with open(dest_file, "w", encoding="utf-8") as f:
    f.write(bundled)

print(f"Bundled successfully into {dest_file}. Total size: {len(bundled)} bytes.")
