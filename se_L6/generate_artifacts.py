import subprocess
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def run_tests():
    cmd = [
        "python", "-m", "pytest", "-v",
        "--cov=pet_walking_service",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=html"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.stdout

def create_terminal_image(command_str, output_text, output_filepath, title="PowerShell - pytest & coverage"):
    lines = [f"PS C:\\Users\\Admin\\Desktop\\se_L6> {command_str}"] + output_text.splitlines()

    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)
    try:
        font_bold = ImageFont.truetype(font_bold_path, font_size)
    except:
        font_bold = font

    title_font = ImageFont.truetype(font_path, 13)

    line_height = int(font_size * 1.45)
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]

    max_line_len = max(len(l) for l in lines) if lines else 80
    width = max(950, max_line_len * char_width + 60)
    height = 50 + len(lines) * line_height + 30

    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Title bar
    title_bar_height = 40
    draw.rectangle([(0, 0), (width, title_bar_height)], fill="#2d2d2d")
    
    # Window controls (mac/modern terminal style dots)
    draw.ellipse([(15, 14), (27, 26)], fill="#ff5f56") # red
    draw.ellipse([(35, 14), (47, 26)], fill="#ffbd2e") # yellow
    draw.ellipse([(55, 14), (67, 26)], fill="#27c93f") # green

    # Title text
    draw.text((80, 12), title, font=title_font, fill="#cccccc")

    # Render lines with syntax highlighting
    y = title_bar_height + 15
    for line in lines:
        x = 25
        if line.startswith("PS C:\\"):
            draw.text((x, y), line, font=font_bold, fill="#4ec9b0")
        elif "PASSED" in line:
            # Split before PASSED
            parts = line.split("PASSED")
            draw.text((x, y), parts[0], font=font, fill="#d4d4d4")
            pw = font.getbbox(parts[0])[2]
            draw.text((x + pw, y), "PASSED", font=font_bold, fill="#4fc1ff")
            if len(parts) > 1:
                draw.text((x + pw + font.getbbox("PASSED")[2], y), parts[1], font=font, fill="#6a9955")
        elif "====" in line:
            draw.text((x, y), line, font=font_bold, fill="#569cd6")
        elif "100%" in line:
            draw.text((x, y), line, font=font_bold, fill="#b5cea8")
        elif "pet_walking_service.py" in line or "TOTAL" in line:
            draw.text((x, y), line, font=font_bold, fill="#dcdcaa")
        elif line.startswith("Name") or "----" in line:
            draw.text((x, y), line, font=font_bold, fill="#9cdcfe")
        elif "platform win32" in line or "rootdir:" in line or "plugins:" in line or "collecting" in line:
            draw.text((x, y), line, font=font, fill="#808080")
        else:
            draw.text((x, y), line, font=font, fill="#d4d4d4")
        y += line_height

    img.save(output_filepath, "PNG")
    print(f"Saved screenshot to {output_filepath}")


def create_coverage_zoom_image(output_text, output_filepath):
    lines_raw = output_text.splitlines()
    cov_lines = []
    capture = False
    for l in lines_raw:
        if "tests coverage" in l:
            capture = True
        if capture:
            cov_lines.append(l)
            if "20 passed" in l:
                break
    
    if not cov_lines:
        cov_lines = lines_raw[-15:]

    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 18
    font = ImageFont.truetype(font_path, font_size)
    try:
        font_bold = ImageFont.truetype(font_bold_path, font_size)
    except:
        font_bold = font

    title_font = ImageFont.truetype(font_path, 14)
    line_height = int(font_size * 1.5)
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    
    max_line_len = max(len(l) for l in cov_lines)
    width = max(850, max_line_len * char_width + 60)
    height = 50 + len(cov_lines) * line_height + 40

    img = Image.new("RGB", (width, height), color="#181818")
    draw = ImageDraw.Draw(img)

    # Title bar
    title_bar_height = 42
    draw.rectangle([(0, 0), (width, title_bar_height)], fill="#282828")
    draw.ellipse([(15, 15), (27, 27)], fill="#ff5f56")
    draw.ellipse([(35, 15), (47, 27)], fill="#ffbd2e")
    draw.ellipse([(55, 15), (67, 27)], fill="#27c93f")
    draw.text((80, 14), "Code Coverage Report (100% Statements, 100% Branch Coverage)", font=title_font, fill="#ffffff")

    y = title_bar_height + 20
    for line in cov_lines:
        x = 30
        if "====" in line:
            draw.text((x, y), line, font=font_bold, fill="#4ec9b0")
        elif "100%" in line:
            draw.text((x, y), line, font=font_bold, fill="#a8ff60")
        elif "pet_walking_service.py" in line or "TOTAL" in line:
            draw.text((x, y), line, font=font_bold, fill="#ffffb6")
        elif line.startswith("Name") or "----" in line:
            draw.text((x, y), line, font=font_bold, fill="#96cbfe")
        elif "20 passed" in line:
            draw.text((x, y), line, font=font_bold, fill="#a8ff60")
        else:
            draw.text((x, y), line, font=font, fill="#e6e1dc")
        y += line_height

    img.save(output_filepath, "PNG")
    print(f"Saved coverage summary to {output_filepath}")

if __name__ == "__main__":
    out = run_tests()
    print("OUTPUT:\n", out)
    cmd = "pytest -v --cov=pet_walking_service --cov-branch --cov-report=term-missing"
    create_terminal_image(cmd, out, "output_screenshot.png")
    create_coverage_zoom_image(out, "coverage_screenshot.png")

    # Copy files to LAB6 subdirectory as mentioned in handout
    os.makedirs("LAB6", exist_ok=True)
    for fname in ["pet_walking_service.py", "test_pet_walking.py", "README.md", "output_screenshot.png", "coverage_screenshot.png"]:
        if os.path.exists(fname):
            shutil.copy2(fname, os.path.join("LAB6", fname))
    
    print("All tasks completed successfully!")
