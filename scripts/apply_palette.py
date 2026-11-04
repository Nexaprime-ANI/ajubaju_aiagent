import re

def update_style_css():
    css_path = 'c:/Users/Windows/Downloads/golo/frontend/style.css'
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    css = re.sub(r'(\.results-header\s*\{[^}]*background:\s*)#FAF8FF;', r'\g<1>#F8F6F2;', css)
    css = re.sub(r'(\.btn-copy-answer\s*\{[^}]*background:\s*)#4F46E5;', r'\g<1>#157A4F;', css)
    css = re.sub(r'(\.btn-copy-answer:hover\s*\{[^}]*background:\s*)#4338CA;', r'\g<1>#0E5E3B;', css)
    css = re.sub(r'(\.btn-back-nav:hover\s*\{[^}]*background:\s*)#F5F3FF;', r'\g<1>#E8F5EF;', css)
    css = re.sub(r'(\.btn-back-nav:hover\s*\{[^}]*border-color:\s*)var\(--color-purple-light\);', r'\g<1>#157A4F;', css)
    css = re.sub(r'(\.sidebar-history-item\.active\s*\{[^}]*background:\s*)#EDE9FE;', r'\g<1>#E8F5EF;', css)
    css = re.sub(r'(\.sidebar-history-item\.active\s*\{[^}]*border-color:\s*)#C7D2FE;', r'\g<1>#C1E4D4;', css)
    css = re.sub(r'(\.assistant-input-tray\s*\{[^}]*border-top:\s*1px\s+solid\s*)#EDE9FE;', r'\g<1>#E5E1D8;', css)
    css = re.sub(r'(\.upgrade-plan-card:hover\s*\{[^}]*background:\s*)#FAF8FF;', r'\g<1>#E8F5EF;', css)
    css = re.sub(r'(\.faq-pill-btn\.active,\s*\.faq-pill-btn:hover\s*\{[^}]*background:\s*)#4F46E5;', r'\g<1>#157A4F;', css)
    css = re.sub(r'#4F46E5', '#157A4F', css)
    css = re.sub(r'#4338CA', '#0E5E3B', css)
    css = re.sub(r'#6366F1', '#1E9E66', css)
    css = re.sub(r'#7C3AED', '#F5B849', css)
    css = re.sub(r'#EDE9FE', '#E5E1D8', css)
    css = re.sub(r'#F5F3FF', '#E8F5EF', css)
    css = re.sub(r'#FAF8FF', '#F8F6F2', css)
    css = re.sub(r'#EEF2FF', '#E8F5EF', css)
    css = re.sub(r'#C7D2FE', '#C1E4D4', css)

    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("style.css updated successfully.")

def update_script_js():
    js_path = 'c:/Users/Windows/Downloads/golo/frontend/script.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    js = js.replace('#EEF2FF', '#E8F5EF')
    js = js.replace('#4338CA', '#157A4F')
    js = js.replace('#4F46E5', '#157A4F')
    js = js.replace('#6366F1', '#157A4F')
    js = js.replace('#7C3AED', '#F5B849')
    js = js.replace('#EDE9FE', '#E5E1D8')
    js = js.replace('#F5F3FF', '#E8F5EF')
    js = js.replace('#FAF8FF', '#F8F6F2')

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("script.js updated successfully.")

def update_index_html():
    html_path = 'c:/Users/Windows/Downloads/golo/frontend/index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('stroke="#4F46E5"', 'stroke="#157A4F"')
    html = html.replace('stroke="#9333EA"', 'stroke="#F5B849"')
    html = html.replace('fill="#9333EA"', 'fill="#F5B849"')
    html = html.replace('stroke="#2563EB"', 'stroke="#4CAF50"')
    html = html.replace('fill="#4F46E5"', 'fill="#157A4F"')
    html = html.replace('color:#6366F1;', 'color:#157A4F;')
    html = html.replace('color: #6366F1;', 'color:#157A4F;')
    html = html.replace('background: #4F46E5;', 'background: #157A4F;')
    html = html.replace('color: #4F46E5;', 'color: #157A4F;')
    html = html.replace('color:#4F46E5;', 'color: #157A4F;')
    html = html.replace('border: 1px solid #EDE9FE;', 'border: 1px solid #E5E1D8;')
    html = html.replace('background: #3B82F6;', 'background: #157A4F;')
    html = html.replace('background: #EFF6FF; color: #2563EB;', 'background: #E8F5EF; color: #157A4F;')
    html = html.replace('background: #FEF3C7; color: #D97706;', 'background: #FEF8EC; color: #B87B10;')
    html = html.replace('background: #DCFCE7; color: #166534;', 'background: #E8F5E9; color: #2E7D32;')
    html = html.replace('color: #10B981;', 'color: #157A4F;')
    html = html.replace('color: #92400E;', 'color: #B87B10;')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated successfully.")

def update_legacy_robot():
    robot_path = 'c:/Users/Windows/Downloads/golo/legacy-v1-robot/index.html'
    try:
        with open(robot_path, 'r', encoding='utf-8') as f:
            robot = f.read()

        robot = robot.replace('--golo-blue: #2563EB;', '--golo-blue: #157A4F;')
        robot = robot.replace('--golo-blue-dark: #1D4ED8;', '--golo-blue-dark: #0E5E3B;')
        robot = robot.replace('--golo-yellow: #F5B849;', '--golo-yellow: #F5B849;')
        robot = robot.replace('--golo-green: #10B981;', '--golo-green: #4CAF50;')
        robot = robot.replace('--golo-red: #EF4444;', '--golo-red: #E04F4D;')
        robot = robot.replace('--bg-page: #F8FAFC;', '--bg-page: #F8F6F2;')

        with open(robot_path, 'w', encoding='utf-8') as f:
            f.write(robot)
        print("legacy-v1-robot index.html updated successfully.")
    except Exception as e:
        print("Warning updating robot index:", e)

if __name__ == '__main__':
    update_style_css()
    update_script_js()
    update_index_html()
    update_legacy_robot()
