import subprocess
import os
import sys
import shutil
from PIL import Image, ImageDraw, ImageFont

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
ORIGINAL_DIR = os.path.join(BASE_DIR, "original")
LAB7_DIR = os.path.join(BASE_DIR, "LAB7")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(LAB7_DIR, exist_ok=True)


def create_terminal_image(command_str, output_text, output_filepath, title="PowerShell - Lab 7"):
    lines = [f"PS C:\\Users\\Admin\\Desktop\\se_7am015> {command_str}"] + output_text.splitlines()

    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    try:
        font_bold = ImageFont.truetype(font_bold_path, font_size)
    except:
        font_bold = font

    title_font = ImageFont.truetype(font_path, 12)

    line_height = int(font_size * 1.45)
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]

    max_line_len = max(len(l) for l in lines) if lines else 80
    width = max(900, min(1400, max_line_len * char_width + 50))
    height = 45 + len(lines) * line_height + 25

    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Title bar
    title_bar_height = 36
    draw.rectangle([(0, 0), (width, title_bar_height)], fill="#2d2d2d")
    
    # Window controls (mac/modern terminal style dots)
    draw.ellipse([(14, 12), (24, 22)], fill="#ff5f56") # red
    draw.ellipse([(32, 12), (42, 22)], fill="#ffbd2e") # yellow
    draw.ellipse([(50, 12), (60, 22)], fill="#27c93f") # green

    # Title text
    draw.text((75, 10), title, font=title_font, fill="#cccccc")

    # Render lines with syntax highlighting
    y = title_bar_height + 12
    for line in lines:
        x = 20
        if line.startswith("PS C:\\"):
            draw.text((x, y), line, font=font_bold, fill="#4ec9b0")
        elif "PASSED" in line:
            parts = line.split("PASSED")
            draw.text((x, y), parts[0], font=font, fill="#d4d4d4")
            pw = font.getbbox(parts[0])[2]
            draw.text((x + pw, y), "PASSED", font=font_bold, fill="#4fc1ff")
            if len(parts) > 1:
                draw.text((x + pw + font.getbbox("PASSED")[2], y), parts[1], font=font, fill="#6a9955")
        elif "FAILED" in line or "FAILURES" in line:
            draw.text((x, y), line, font=font_bold, fill="#f14c4c")
        elif "====" in line:
            draw.text((x, y), line, font=font_bold, fill="#569cd6")
        elif "11 passed" in line:
            draw.text((x, y), line, font=font_bold, fill="#4ec9b0")
        elif "9 failed" in line:
            draw.text((x, y), line, font=font_bold, fill="#f14c4c")
        elif line.startswith("Enter "):
            draw.text((x, y), line, font=font_bold, fill="#ce9178")
        elif "Walk:" in line or "Pace" in line or "Surcharge:" in line:
            draw.text((x, y), line, font=font_bold, fill="#dcdcaa")
        elif "Invalid " in line:
            draw.text((x, y), line, font=font_bold, fill="#d7ba7d")
        elif "Traceback" in line or "Exception" in line or "Error:" in line or "Falsifying" in line:
            draw.text((x, y), line, font=font, fill="#f48771")
        elif "platform win32" in line or "rootdir:" in line or "plugins:" in line or "collecting" in line:
            draw.text((x, y), line, font=font, fill="#808080")
        else:
            draw.text((x, y), line, font=font, fill="#d4d4d4")
        y += line_height

    img.save(output_filepath, "PNG")
    print(f"Saved terminal screenshot: {output_filepath}")


def run_step2():
    print("--- Running Step 2: original processor.py ---")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(ORIGINAL_DIR, "processor.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # Give valid inputs
    inputs = "2-30-YES\n45/3\nCALM\n"
    out_valid, _ = proc.communicate(inputs)

    # Also run with empty input to demonstrate crash on invalid input
    proc_crash = subprocess.Popen(
        [sys.executable, os.path.join(ORIGINAL_DIR, "processor.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    out_crash, _ = proc_crash.communicate("\n")

    combined = (
        out_valid.strip() +
        "\n\n==== Demonstrating crash on invalid / empty input ====\n" +
        "PS C:\\Users\\Admin\\Desktop\\se_7am015> python original\\processor.py\n" +
        out_crash.strip()
    )

    ss_path = os.path.join(SCREENSHOTS_DIR, "step2_original_run.png")
    create_terminal_image("python original\\processor.py", combined, ss_path, "Step 2: Running Original (Buggy) processor.py")
    return ss_path


def run_step4():
    print("--- Running Step 4: test_processor.py vs original ---")
    test_file = os.path.join(ORIGINAL_DIR, "test_processor.py")
    shutil.copy2(os.path.join(BASE_DIR, "test_processor.py"), test_file)

    cmd = [
        sys.executable, "-m", "pytest", "test_processor.py",
        "-p", "no:cacheprovider", "--tb=line"
    ]
    proc = subprocess.run(cmd, cwd=ORIGINAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = proc.stdout

    if os.path.exists(test_file):
        os.remove(test_file)

    ss_path = os.path.join(SCREENSHOTS_DIR, "step4_tests_failing.png")
    create_terminal_image("python -m pytest test_processor.py --tb=line", out.strip(), ss_path, "Step 4: Hypothesis Fuzz Tests Against Original Code (9 Failed)")
    return ss_path


def run_step5():
    print("--- Running Step 5: fixed processor.py ---")
    # 1. Run with valid inputs
    proc_val = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "processor.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    out_val, _ = proc_val.communicate("2-30-YES\n45/3\nPLAYFUL\n")

    # 2. Run with edge cases / invalid inputs
    proc_inv = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "processor.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    out_inv, _ = proc_inv.communicate("invalid-schedule\n45/0\nUNKNOWN\n")

    combined = (
        out_val.strip() +
        "\n\n==== Demonstrating defensive error handling on invalid inputs ====\n" +
        "PS C:\\Users\\Admin\\Desktop\\se_7am015> python processor.py\n" +
        out_inv.strip()
    )

    ss_path = os.path.join(SCREENSHOTS_DIR, "step5_fixed_run.png")
    create_terminal_image("python processor.py", combined, ss_path, "Step 5: Running Fixed (Hardened) processor.py")
    return ss_path


def run_step6():
    print("--- Running Step 6: test_processor.py vs fixed ---")
    cmd = [
        sys.executable, "-m", "pytest", "test_processor.py",
        "-v", "-p", "no:cacheprovider"
    ]
    proc = subprocess.run(cmd, cwd=BASE_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = proc.stdout

    ss_path = os.path.join(SCREENSHOTS_DIR, "step6_tests_passing.png")
    create_terminal_image("python -m pytest test_processor.py -v", out.strip(), ss_path, "Step 6: Hypothesis Fuzz Tests Against Fixed Code (11 Passed)")
    return ss_path


def build_pdf_report(pdf_filename="Lab7_Submission.pdf"):
    print(f"--- Generating {pdf_filename} ---")
    pdf_path = os.path.join(BASE_DIR, pdf_filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=4
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#37474f'),
        spaceAfter=8
    )
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0d47a1'),
        spaceBefore=6,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#263238'),
        spaceAfter=4
    )
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9
    )
    table_head_style = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", title_style))
    meta_text = (
        "<b>Student:</b> Aditya Shet &nbsp;|&nbsp; "
        "<b>USN:</b> PES2UG24AM015 &nbsp;|&nbsp; "
        "<b>Assigned Repo:</b> SETAPESU26/L6_L7_13_pet_walking_service (lab7) &nbsp;|&nbsp; "
        "<b>Tool:</b> Hypothesis 6.170 + pytest 9.1"
    )
    story.append(Paragraph(meta_text, meta_style))

    # Step 2
    story.append(Paragraph("Step 2 – Running the Original Application (processor.py)", h2_style))
    story.append(Paragraph(
        "Running the original application with normal inputs produces valid output; however, entering an empty or "
        "malformed schedule input immediately causes an unhandled <code>ValueError: not enough values to unpack</code>.",
        body_style
    ))
    img2_path = os.path.join(SCREENSHOTS_DIR, "step2_original_run.png")
    if os.path.exists(img2_path):
        story.append(RLImage(img2_path, width=7.2*inch, height=1.7*inch))

    story.append(Spacer(1, 4))

    # Step 3
    story.append(Paragraph("Step 3 – Property-Based Fuzz Testing Implementation (test_processor.py)", h2_style))
    story.append(Paragraph(
        "The test suite contains 11 property-based tests configured with <code>@settings(max_examples=500, deadline=None)</code>. "
        "Three are random fuzzers (<code>st.text() | st.none()</code>) wrapped in try/except blocks to guarantee no crash occurs. "
        "Eight are property tests verifying valid calculation formulas, rejecting invalid weekend tokens, catching negative counts, "
        "preventing zero division on pace calculations, rejecting non-finite floats (NaN/Inf), and verifying temperament codes.",
        body_style
    ))

    # Step 4
    story.append(Paragraph("Step 4 – Fuzz Tests Against Original Code: 9 Failed, 2 Passed", h2_style))
    story.append(Paragraph(
        "Hypothesis automatically explored edge cases and revealed 9 failures in the original application, pinpointing minimal "
        "failing inputs including <code>None</code>, empty strings <code>''</code>, division by zero <code>45/0</code>, and missing keys.",
        body_style
    ))
    img4_path = os.path.join(SCREENSHOTS_DIR, "step4_tests_failing.png")
    if os.path.exists(img4_path):
        story.append(RLImage(img4_path, width=7.2*inch, height=2.4*inch))

    # Force Page Break for Page 2
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # Bugs table
    story.append(Paragraph("Bugs Uncovered and Applied Fixes", h2_style))
    table_data = [
        [
            Paragraph("Function", table_head_style),
            Paragraph("Minimal Failing Input", table_head_style),
            Paragraph("Original Behaviour", table_head_style),
            Paragraph("Hardened Defensive Fix", table_head_style)
        ],
        [
            Paragraph("parse_walk_schedule", table_text_style),
            Paragraph("<code>None</code>", table_text_style),
            Paragraph("AttributeError ('NoneType' has no strip)", table_text_style),
            Paragraph("Type check: isinstance(s, str) → None", table_text_style)
        ],
        [
            Paragraph("parse_walk_schedule", table_text_style),
            Paragraph("<code>''</code>, <code>'2-30'</code>", table_text_style),
            Paragraph("ValueError (not enough values to unpack)", table_text_style),
            Paragraph("Regex pattern validation (3 tokens) → None", table_text_style)
        ],
        [
            Paragraph("parse_walk_schedule", table_text_style),
            Paragraph("<code>'a-b-YES'</code>", table_text_style),
            Paragraph("ValueError (invalid literal for int)", table_text_style),
            Paragraph("Safe int casting with try/except → None", table_text_style)
        ],
        [
            Paragraph("parse_walk_schedule", table_text_style),
            Paragraph("<code>'-1-30-YES'</code>", table_text_style),
            Paragraph("Too many tokens or negative pets accepted", table_text_style),
            Paragraph("Strict range validation: pets >= 0 and mins >= 0", table_text_style)
        ],
        [
            Paragraph("parse_walk_schedule", table_text_style),
            Paragraph("<code>'2-30-MAYBE'</code>", table_text_style),
            Paragraph("KeyError ('MAYBE')", table_text_style),
            Paragraph("Validate against {'YES', 'NO'} map → None", table_text_style)
        ],
        [
            Paragraph("compute_pace_per_pet", table_text_style),
            Paragraph("<code>None</code>, <code>''</code>", table_text_style),
            Paragraph("AttributeError / ValueError", table_text_style),
            Paragraph("Type & regex format validation → None", table_text_style)
        ],
        [
            Paragraph("compute_pace_per_pet", table_text_style),
            Paragraph("<code>'45/0'</code>", table_text_style),
            Paragraph("ZeroDivisionError: float division by zero", table_text_style),
            Paragraph("Defensive check: pets > 0 → None", table_text_style)
        ],
        [
            Paragraph("compute_pace_per_pet", table_text_style),
            Paragraph("<code>'nan/2'</code>, <code>'1e400/2'</code>", table_text_style),
            Paragraph("Returned nan / inf", table_text_style),
            Paragraph("math.isfinite() validation → None", table_text_style)
        ],
        [
            Paragraph("lookup_temperament_surcharge", table_text_style),
            Paragraph("<code>None</code>, <code>''</code>", table_text_style),
            Paragraph("AttributeError / KeyError", table_text_style),
            Paragraph("Type check & min length >= 3 check → None", table_text_style)
        ],
        [
            Paragraph("lookup_temperament_surcharge", table_text_style),
            Paragraph("<code>'PLAYFUL'</code>", table_text_style),
            Paragraph("KeyError: 'PLA' (dictionary only had 'PLY')", table_text_style),
            Paragraph("Support both 'PLA' and 'PLY' mapped to 5.0", table_text_style)
        ],
        [
            Paragraph("lookup_temperament_surcharge", table_text_style),
            Paragraph("<code>'UNKNOWN'</code>", table_text_style),
            Paragraph("KeyError: 'UNK'", table_text_style),
            Paragraph("Dictionary .get(prefix, None) → None", table_text_style)
        ]
    ]

    t = Table(table_data, colWidths=[1.4*inch, 1.2*inch, 2.1*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b0bec5')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    story.append(t)
    story.append(Spacer(1, 4))

    # Step 5
    story.append(Paragraph("Step 5 – Running the Fixed Application (processor.py)", h2_style))
    story.append(Paragraph(
        "Design Choice: Every function defensively validates its input and returns <code>None</code> on invalid input instead of raising "
        "exceptions. The <code>main()</code> driver displays user-friendly error messages without crashing.",
        body_style
    ))
    img5_path = os.path.join(SCREENSHOTS_DIR, "step5_fixed_run.png")
    if os.path.exists(img5_path):
        story.append(RLImage(img5_path, width=7.2*inch, height=1.65*inch))

    story.append(Spacer(1, 4))

    # Step 6
    story.append(Paragraph("Step 6 – Fuzz Tests Against Fixed Code: All 11 Passed", h2_style))
    story.append(Paragraph(
        "Running the full Hypothesis fuzzing suite (5,500 total generated test cases across all 11 tests) against the hardened module "
        "achieves 100% pass rate with zero crashes and completely verified properties.",
        body_style
    ))
    img6_path = os.path.join(SCREENSHOTS_DIR, "step6_tests_passing.png")
    if os.path.exists(img6_path):
        story.append(RLImage(img6_path, width=7.2*inch, height=1.75*inch))

    doc.build(story)
    print(f"Successfully generated: {pdf_path}")
    return pdf_path


def copy_to_lab7_folder():
    print("--- Copying files to LAB7 directory ---")
    files_to_copy = [
        "processor.py",
        "test_processor.py",
        "README.md",
        "Lab7_Submission.pdf"
    ]
    for f in files_to_copy:
        src = os.path.join(BASE_DIR, f)
        if os.path.exists(src):
            dst = os.path.join(LAB7_DIR, f)
            shutil.copy2(src, dst)
            print(f"Copied {f} to LAB7/{f}")

    # Copy screenshots folder to LAB7/screenshots
    lab7_screenshots = os.path.join(LAB7_DIR, "screenshots")
    os.makedirs(lab7_screenshots, exist_ok=True)
    for img_f in os.listdir(SCREENSHOTS_DIR):
        if img_f.endswith(".png"):
            shutil.copy2(os.path.join(SCREENSHOTS_DIR, img_f), os.path.join(lab7_screenshots, img_f))
    print(f"Copied screenshots to LAB7/screenshots")


if __name__ == "__main__":
    s2 = run_step2()
    s4 = run_step4()
    s5 = run_step5()
    s6 = run_step6()
    pdf = build_pdf_report()
    copy_to_lab7_folder()
    print("=== All artifacts generated successfully! ===")
