import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = 'Lab2_Submission.pdf'
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=19,
    textColor=colors.HexColor('#172B4D'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=12.5,
    textColor=colors.HexColor('#505F79'),
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'Heading1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#172B4D'),
    spaceBefore=6,
    spaceAfter=5
)

body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#172B4D'),
    spaceAfter=5
)

table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#172B4D')
)

table_body_style = ParagraphStyle(
    'TableBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#172B4D')
)

caption_style = ParagraphStyle(
    'Caption',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#42526E'),
    spaceBefore=4,
    spaceAfter=8
)

story = []

# Page 1: Header
story.append(Paragraph('Lab 2 \u2013 Agile Backlog Creation &amp; Sprint Simulation in Jira', title_style))
subtitle_text = 'Problem Statement #29 \u2013 Municipal Infrastructure Damage Reporting App \u00b7 <b>Aditya Shet</b> \u00b7 <b>PES2UG24AM015</b> \u00b7 Jira space \u201cDamage Reporting App\u201d (DRA)'
story.append(Paragraph(subtitle_text, subtitle_style))

story.append(Paragraph('Backlog summary', h1_style))

table_data = [
    [
        Paragraph('Epic', table_header_style),
        Paragraph('User stories (story points)', table_header_style),
        Paragraph('From Lab 1', table_header_style)
    ],
    [
        Paragraph('EPIC1 Damage Reporting', table_body_style),
        Paragraph('Auto-detect report location (5), Choose damage type and attach photo (3), Submit report offline (8)', table_body_style),
        Paragraph('FR-001, FR-002,<br/>NFR-001', table_body_style)
    ],
    [
        Paragraph('EPIC2 Automated Screening', table_body_style),
        Paragraph('Flag duplicate reports (8), Reject incomplete or out-of-city reports (3)', table_body_style),
        Paragraph('FR-003', table_body_style)
    ],
    [
        Paragraph('EPIC3 Routing and Resolution', table_body_style),
        Paragraph('Route valid report to department (5), Assign engineer and update status (3), Audit log of status changes (5)', table_body_style),
        Paragraph('FR-004, NFR-002', table_body_style)
    ],
    [
        Paragraph('EPIC4 Status Tracking and Notifications', table_body_style),
        Paragraph('Track report status (2), Notify on status change (3)', table_body_style),
        Paragraph('FR-005', table_body_style)
    ]
]

col_widths = [135, 290, 90]
t = Table(table_data, colWidths=col_widths)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F4F5F7')),
    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#C1C7D0')),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DFE1E6')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 6))

summary_text = 'Total 45 story points on the Fibonacci scale. <b>Sprint 1 (24 pts, 5 stories, all High priority):</b> a citizen can submit a located, photographed report that is screened and routed. <b>Sprint 2 (21 pts, 5 stories):</b> offline submission, officer workflow with audit trail, citizen status tracking and notifications. Each sprint was 1 week (12\u201319 Nov 2026).'
story.append(Paragraph(summary_text, body_style))
story.append(Spacer(1, 4))

story.append(Paragraph('Reflection', h1_style))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#C1C7D0'), spaceBefore=1, spaceAfter=5))

reflections = [
    (
        '1. Did your estimations reflect the actual effort?',
        'Not in a way the sprint could measure. The points were set by relative complexity and uncertainty: offline sync and duplicate detection got 8 because of sync conflicts and deciding when two reports describe the same damage, and status tracking got 2. Because the sprint was simulated, every story moved to Done within minutes, so a 2-point and an 8-point story took the same real time. The relative ordering still seems sound, but checking it would need real development time, for example by comparing hours logged per point across sprints.'
    ),
    (
        '2. Was your backlog well-prioritized?',
        'Mostly. Sprint 1 held the High-priority stories that form the core flow (locate, describe, screen and route a report), so it delivers something usable on its own. Sprint 2 held the stories that depend on that flow, plus the two Medium-priority citizen-feedback stories. One weakness: \u201cSubmit report offline\u201d is High priority (NFR-001), but it was deferred to Sprint 2 because it was the largest and riskiest story and builds on the submission flow. In hindsight it could have been split, for example local saving in Sprint 1 and auto-sync in Sprint 2, so that part of a High-priority item shipped earlier.'
    ),
    (
        '3. How did your simulated sprint align with your plan?',
        'Scope matched the plan exactly. Both sprints completed all committed stories (24/24 and 21/21 points, 100% done), with no carry-over or scope change, and every epic reached 100%. The timing didn\u2019t match: work planned for a week finished on day one, because cards were moved rather than built.'
    ),
    (
        '4. What insights did the burndown chart give about your team\u2019s capacity?',
        'In both sprints the remaining-work line dropped straight to 0% on the first day, far below the grey guideline, which falls linearly to 19 Nov. Read literally, the chart says the team finished early and under-committed, so it could take on more work. It also shows the \u201csharp drop\u201d pattern, which signals that stories were not tracked incrementally. In a real sprint, the line should step down as each story is finished, and staying close to the guideline would confirm a velocity of roughly 21\u201324 points per week for planning future sprints.'
    )
]

for q, a in reflections:
    p_text = f'<b>{q}</b> {a}'
    story.append(Paragraph(p_text, body_style))
    story.append(Spacer(1, 2))

# Page 2: Deliverables & Figures 1 and 2
story.append(PageBreak())
story.append(Paragraph('Deliverables', h1_style))
story.append(Spacer(1, 4))

fig1_path = os.path.join('screenshots', '1_backlog_epics_story_points.png')
fig2_path = os.path.join('screenshots', '2_sprint1_active_board.png')

img_w = 515
img1_h = img_w * (930.0 / 1917.0)
img2_h = img_w * (927.0 / 1917.0)

story.append(RLImage(fig1_path, width=img_w, height=img1_h))
story.append(Paragraph('Figure 1 \u2013 Backlog with the Epic panel, all 10 user stories, priorities and story points (45 total)', caption_style))
story.append(Spacer(1, 10))

story.append(RLImage(fig2_path, width=img_w, height=img2_h))
story.append(Paragraph('Figure 2 \u2013 Sprint 1 active sprint board at start (5 stories, To Do)', caption_style))

# Page 3: Figures 3 and 4
story.append(PageBreak())

fig3_path = os.path.join('screenshots', '3_sprint1_burndown.png')
fig4_path = os.path.join('screenshots', '4_sprint2_burndown.png')

img3_h = img_w * (927.0 / 1915.0)
img4_h = img_w * (957.0 / 1919.0)

story.append(RLImage(fig3_path, width=img_w, height=img3_h))
story.append(Paragraph('Figure 3 \u2013 Sprint 1 board (all Done) with sprint insights burndown: 24 points done, 0 to go', caption_style))
story.append(Spacer(1, 10))

story.append(RLImage(fig4_path, width=img_w, height=img4_h))
story.append(Paragraph('Figure 4 \u2013 Sprint 2 board (all Done) with burndown: 21 points done; all epics at 100%', caption_style))

doc.build(story)
print('Lab2_Submission.pdf generated successfully!')
