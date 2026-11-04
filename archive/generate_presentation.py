import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Emu(9144000)
prs.slide_height = Emu(5143500)
blank_layout = prs.slide_layouts[6]

HEADER_IMG = "/Users/mittal/Downloads/ExtremeEventWarning/somaiya_header.png"
FONT_NAME = "Times New Roman"
COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_MAROON = RGBColor(163, 38, 56)
COLOR_GRAY = RGBColor(70, 70, 70)
COLOR_LIGHT_BG = RGBColor(245, 245, 245)

def add_header_banner(slide):
    if os.path.exists(HEADER_IMG):
        slide.shapes.add_picture(HEADER_IMG, 0, 0, Emu(9144000), Emu(1332186))

def add_slide_heading(slide, title_text):
    add_header_banner(slide)
    
    title_box = slide.shapes.add_textbox(Emu(500000), Emu(1350000), Emu(8144000), Emu(450000))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = FONT_NAME
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    
    # Separator line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Emu(500000), Emu(1780000), Emu(8144000), Emu(20000)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(200, 200, 200)
    line.line.color.rgb = RGBColor(200, 200, 200)

def add_footer(slide, slide_num):
    box = slide.shapes.add_textbox(Emu(500000), Emu(4850000), Emu(8144000), Emu(250000))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"Department of AI&DS, KJSIT  |  Group 11  |  Slide {slide_num}"
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(120, 120, 120)

# ==================== SLIDE 1: TITLE SLIDE ====================
slide1 = prs.slides.add_slide(blank_layout)
add_header_banner(slide1)

t_box = slide1.shapes.add_textbox(Emu(500000), Emu(1480000), Emu(8144000), Emu(3250000))
tf1 = t_box.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

p = tf1.paragraphs[0]
p.text = "Department of Artificial Intelligence & Data Science"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_GRAY
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(4)

p = tf1.add_paragraph()
p.text = "T.Y. Mini Project / Project-Based Learning (PBL) Presentation"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(14)

p = tf1.add_paragraph()
p.text = "AI-Powered Early Warning System for Compound Extreme Events"
p.font.name = FONT_NAME
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER

p = tf1.add_paragraph()
p.text = "(Heatwaves & Droughts) using Multi-Variate Anomaly Detection"
p.font.name = FONT_NAME
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(18)

p = tf1.add_paragraph()
p.text = "Project Guide: Mrs. Sheetal Jagtap        |        Group No: 11"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(14)

p = tf1.add_paragraph()
p.text = "Presented By:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER

p = tf1.add_paragraph()
p.text = "Hetvi Mehta (Roll No. 33)   •   Jahnvi Patel (Roll No. 44)   •   Mittal Patel (Roll No. 46)"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(10)

p = tf1.add_paragraph()
p.text = "K.J. Somaiya Institute of Technology, Sion, Mumbai - 400022"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.color.rgb = COLOR_GRAY
p.alignment = PP_ALIGN.CENTER

add_footer(slide1, 1)

# ==================== SLIDE 2: TABLE OF CONTENTS ====================
slide2 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide2, "Table of Contents")

rows, cols = 6, 2
tbl2 = slide2.shapes.add_table(rows, cols, Emu(800000), Emu(1950000), Emu(7544000), Emu(2500000)).table
tbl2.columns[0].width = Emu(3772000)
tbl2.columns[1].width = Emu(3772000)

agenda_items = [
    ("1. Introduction", "7. Objectives"),
    ("2. Literature Review", "8. Methodology & Architecture"),
    ("3. Motivation", "9. Results & Discussion"),
    ("4. Problem Statement", "10. Conclusion & Future Work"),
    ("5. Dataset & Feature Engineering", "11. References"),
    ("6. Machine Learning Models", "12. Thank You & Q&A")
]

for r_idx, (c1, c2) in enumerate(agenda_items):
    for c_idx, val in enumerate([c1, c2]):
        cell = tbl2.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLACK
        cell.text_frame.margin_left = Emu(150000)

add_footer(slide2, 2)

# ==================== SLIDE 3: INTRODUCTION ====================
slide3 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide3, "1. Introduction")

tf3 = slide3.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf3.word_wrap = True

intro_points = [
    ("Climate Context & Vulnerability:", "India experiences frequent severe heatwaves and erratic rainfall regimes, significantly influenced by large-scale oceanic-atmospheric teleconnections such as ENSO (El Niño-Southern Oscillation)."),
    ("Compound Extreme Events:", "When extreme heat and meteorological drought co-occur simultaneously or sequentially, their combined impact on agriculture, water reservoirs, power grids, and human health is exponentially more destructive than isolated single hazards."),
    ("Need for Early Warning:", "Traditional disaster response is reactive. Developing a reliable 7-day advance forecasting window provides actionable lead time for public health authorities, water resource managers, and farmers."),
    ("Project Focus:", "An end-to-end early warning system across 12 major Indian cities utilizing 27 years of daily meteorological and oceanic observations with supervised machine learning and multivariate anomaly detection.")
]

for title, desc in intro_points:
    p = tf3.add_paragraph() if tf3.paragraphs[0].text else tf3.paragraphs[0]
    p.text = f"• {title} "
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_NAME
    run.font.size = Pt(14)
    run.font.bold = False
    run.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(10)

add_footer(slide3, 3)

# ==================== SLIDE 4: LITERATURE REVIEW ====================
slide4 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide4, "2. Literature Review")

tbl4 = slide4.shapes.add_table(4, 3, Emu(600000), Emu(2000000), Emu(7944000), Emu(2500000)).table
tbl4.columns[0].width = Emu(2300000)
tbl4.columns[1].width = Emu(2900000)
tbl4.columns[2].width = Emu(2744000)

headers4 = ["Author & Year", "Key Contribution", "Identified Research Gap"]
for c_idx, h in enumerate(headers4):
    cell = tbl4.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_MAROON
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

lit_data = [
    ("Xie et al. (2026)\nClimate Dynamics", "Global compound heatwave–drought analysis and spatiotemporal teleconnections with ENSO.", "Global-scale analysis without a localized 7-day operational warning system for Indian climate zones."),
    ("Qureshi et al. (2025)\nScientific Reports", "Seasonally-adjusted ML and time-series models for heatwave forecasting.", "Evaluated heatwaves in isolation; neglected joint drought and compound event dynamics."),
    ("Zarei (2026)\nScientific Reports", "Medium-term monitoring and ML-based forecasting of drought dynamics.", "Drought-centric; excluded concurrent temperature extremes and real-time early warning dashboard.")
]

for r_idx, row in enumerate(lit_data):
    for c_idx, val in enumerate(row):
        cell = tbl4.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_BLACK

add_footer(slide4, 4)

# ==================== SLIDE 5: MOTIVATION ====================
slide5 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide5, "3. Motivation")

tf5 = slide5.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf5.word_wrap = True

mot_points = [
    ("Compounding Socio-Economic Threats:", "Compound heatwaves and droughts cause severe agricultural loss, water depletion, power grid stress, and heat-related mortality across urban and rural centers."),
    ("Crucial Preparation Window:", "A 7-day forecasting horizon provides crucial lead time for disaster relief agencies, municipal corporations, and farming communities to mobilize water rationing and cooling measures."),
    ("Nonlinear Climate Interactions:", "Univariate meteorological systems fail to detect interacting hazards. Multivariate AI effectively models complex soil moisture-atmosphere temperature feedback loops."),
    ("Incorporating Large-Scale Climate Context:", "Integrating oceanic indices (NOAA ONI) captures macro-climatic shifts (El Niño/La Niña), enhancing regional prediction precision."),
    ("Explainable AI for Real-World Decision Making:", "Moving beyond 'black-box' predictions by providing SHAP-based feature importance so administrators understand why an alert was triggered.")
]

for title, desc in mot_points:
    p = tf5.add_paragraph() if tf5.paragraphs[0].text else tf5.paragraphs[0]
    p.text = f"• {title} "
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_NAME
    run.font.size = Pt(14)
    run.font.bold = False
    run.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(10)

add_footer(slide5, 5)

# ==================== SLIDE 6: PROBLEM STATEMENT ====================
slide6 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide6, "4. Problem Statement")

tf6 = slide6.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf6.word_wrap = True

prob_points = [
    ("The Core Problem:", "Current operational early warning infrastructure primarily monitors temperature and precipitation hazards in silos, failing to anticipate deadly compound events where heat and moisture deficits amplify one another."),
    ("Data Leakage in Predictive Systems:", "Standard machine learning approaches often suffer from temporal data leakage by using random cross-validation instead of strict chronological time-series splitting."),
    ("High False-Alarm Rates in Rare Events:", "Compound events are statistically rare (~1.3% historical frequency). Off-the-shelf models produce excessive false alarms or entirely miss catastrophic events."),
    ("Our Technical Solution:", "Develop a leakage-safe multivariate forecasting framework combining supervised machine learning, calibrated decision thresholds, and anomaly detection to accurately predict 7-day-ahead heatwaves, droughts, and compound extremes across 12 Indian cities.")
]

for title, desc in prob_points:
    p = tf6.add_paragraph() if tf6.paragraphs[0].text else tf6.paragraphs[0]
    p.text = f"• {title} "
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_NAME
    run.font.size = Pt(14)
    run.font.bold = False
    run.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(12)

add_footer(slide6, 6)

# ==================== SLIDE 7: OBJECTIVES ====================
slide7 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide7, "5. Project Objectives")

tf7 = slide7.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf7.word_wrap = True

p = tf7.paragraphs[0]
p.text = "Primary Objective:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON

p2 = tf7.add_paragraph()
p2.text = "To build a robust, leakage-safe AI-powered early warning system that predicts heatwaves, droughts, and compound events up to 7 days in advance across 12 Indian metropolitan locations."
p2.font.name = FONT_NAME
p2.font.size = Pt(14)
p2.font.color.rgb = COLOR_BLACK
p2.space_after = Pt(12)

p3 = tf7.add_paragraph()
p3.text = "Specific Objectives:"
p3.font.name = FONT_NAME
p3.font.size = Pt(14)
p3.font.bold = True
p3.font.color.rgb = COLOR_MAROON

objectives_list = [
    "1. Data Integration: Ingest and harmonize 27 years (1997–2023) of daily climate records from IMD, NASA POWER, and NOAA ONI (118,250 rows).",
    "2. Ground-Truth Event Labeling: Formulate physically sound classification thresholds for Heatwaves, Dry Days, and Compound Events.",
    "3. Leakage-Safe Feature Engineering: Derive 30-day trailing rolling means, streaks, anomalies, and lag indicators strictly from past context.",
    "4. Model Benchmarking: Train and evaluate Random Forest, Decision Tree, and SVM models using chronological validation.",
    "5. Calibrated Thresholding & Explainability: Calibrate compound event decision thresholds (0.45) and integrate SHAP TreeExplainer feature importance.",
    "6. Interactive Deployment: Develop a production Streamlit dashboard hosted live for real-time monitoring and public access."
]

for obj in objectives_list:
    p = tf7.add_paragraph()
    p.text = f"• {obj}"
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(4)

add_footer(slide7, 7)

# ==================== SLIDE 8: METHODOLOGY ====================
slide8 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide8, "6. Methodology & Architecture")

tf8 = slide8.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf8.word_wrap = True

meth_points = [
    ("1. Multi-Source Climate Data Pipeline:", "Daily gridded maximum temperature from IMD, daily precipitation, relative humidity, wind speed, and solar radiation from NASA POWER, and monthly ONI index from NOAA (118,250 records across 12 cities)."),
    ("2. Event Definition & Physical Labeling:", "Heatwave: TMAX >= 40°C & TMAX >= 90th percentile; Drought: Precipitation < 1 mm & 14-day cumulative rainfall < 5 mm; Compound Event: Simultaneous occurrence of Heatwave and Drought conditions."),
    ("3. Leakage-Safe Causal Features:", "Engineered 30-day trailing moving averages, 7-day & 14-day rainfall deficits, rolling temperature extremes, consecutive dry day streaks, and ONI climate anomaly indices."),
    ("4. Chronological Validation & Model Training:", "Used TimeSeriesSplit cross-validation. Trained Random Forest, Decision Tree, and SVM classifiers to predict hazard probability 7 days ahead."),
    ("5. Anomaly Detection & Explainability:", "Integrated multivariate Z-score anomaly detection, 30-day pattern anomaly scores, and SHAP TreeExplainer to compute feature importance rankings for every prediction.")
]

for step, desc in meth_points:
    p = tf8.add_paragraph() if tf8.paragraphs[0].text else tf8.paragraphs[0]
    p.text = f"• {step} "
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_NAME
    run.font.size = Pt(13)
    run.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(8)

add_footer(slide8, 8)

# ==================== SLIDE 9: RESULTS AND DISCUSSION ====================
slide9 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide9, "7. Results and Discussion")

tbl9 = slide9.shapes.add_table(10, 5, Emu(600000), Emu(1950000), Emu(7944000), Emu(2000000)).table
tbl9.columns[0].width = Emu(1700000)
tbl9.columns[1].width = Emu(2000000)
tbl9.columns[2].width = Emu(1400000)
tbl9.columns[3].width = Emu(1400000)
tbl9.columns[4].width = Emu(1444000)

headers9 = ["Target Event", "Model Architecture", "Accuracy", "Precision", "Recall / F1"]
for c_idx, h in enumerate(headers9):
    cell = tbl9.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_MAROON
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

perf_data = [
    ("Heatwave (7d)", "Random Forest (Best)", "90.10%", "46.35%", "48.69% (F1: 0.475)"),
    ("Heatwave (7d)", "Decision Tree", "88.58%", "36.73%", "33.48% (F1: 0.350)"),
    ("Heatwave (7d)", "SVM (LinearSVC)", "77.76%", "26.38%", "79.30% (F1: 0.396)"),
    ("Drought (7d)", "Random Forest (Best)", "88.23%", "42.00%", "71.61% (F1: 0.529)"),
    ("Drought (7d)", "Decision Tree", "86.43%", "32.22%", "42.41% (F1: 0.366)"),
    ("Drought (7d)", "SVM (LinearSVC)", "76.61%", "26.02%", "83.01% (F1: 0.396)"),
    ("Compound (7d)", "RF Improved (0.45 thresh)", "96.76%", "30.18%", "18.16% (F1: 0.227)"),
    ("Compound (7d)", "Decision Tree", "95.83%", "16.75%", "14.88% (F1: 0.158)"),
    ("Compound (7d)", "SVM (LinearSVC)", "82.53%", "11.41%", "83.81% (F1: 0.201)")
]

for r_idx, row in enumerate(perf_data):
    for c_idx, val in enumerate(row):
        cell = tbl9.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_LIGHT_BG if r_idx % 3 == 0 else RGBColor(255, 255, 255)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        if "Best" in val or "Improved" in val:
            p.font.bold = True
            p.font.color.rgb = COLOR_MAROON
        else:
            p.font.color.rgb = COLOR_BLACK

tf_d = slide9.shapes.add_textbox(Emu(600000), Emu(4100000), Emu(7944000), Emu(700000)).text_frame
tf_d.word_wrap = True
tf_d.margin_top = tf_d.margin_bottom = tf_d.margin_left = tf_d.margin_right = 0

p = tf_d.paragraphs[0]
p.text = "Key Findings & Discussion:"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON

p2 = tf_d.add_paragraph()
p2.text = "• Random Forest consistently delivers the highest accuracy and balanced F1-scores across all three hazard types.\n• Decision Threshold Optimization: Lowering compound probability threshold to 0.45 increased real-event capture while maintaining low false alarms.\n• SHAP explainability confirms 30-day TMAX rolling average, cumulative precipitation deficit, and ONI are the top predictive features."
p2.font.name = FONT_NAME
p2.font.size = Pt(12)
p2.font.color.rgb = COLOR_BLACK

add_footer(slide9, 9)

# ==================== SLIDE 10: CONCLUSION & FUTURE WORK ====================
slide10 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide10, "8. Conclusion & Future Work")

tf10 = slide10.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf10.word_wrap = True

conc_points = [
    ("Key Achievements:", "Developed an operational 7-day advance early warning system for Heatwaves, Droughts, and Compound Events across 12 Indian cities utilizing 27 years of multi-agency climate data (118,250 records)."),
    ("Model Efficacy:", "Random Forest established superior predictive performance (90.1% accuracy for Heatwaves, 88.2% for Droughts, 96.8% for Compound Events). Calibrated 0.45 threshold resolved severe class imbalance."),
    ("Deployment:", "Successfully launched a production-grade Streamlit web application providing interactive risk advisories, 30-day historical validation curves, and model benchmarking."),
    ("Future Scope - Satellite Integration:", "Incorporate active microwave soil moisture indices (SMAP) and GRACE groundwater depletion indicators into the feature pipeline."),
    ("Future Scope - Lead-Time Extension:", "Expand the forecasting window from 7 days to sub-seasonal 14-day forecasts utilizing Numerical Weather Prediction (NWP) ensemble outputs."),
    ("Future Scope - Automated Alerting:", "Integrate SMS/WhatsApp broadcast APIs for automated farmer advisories and municipal heat-action plan mobilization.")
]

for title, desc in conc_points:
    p = tf10.add_paragraph() if tf10.paragraphs[0].text else tf10.paragraphs[0]
    p.text = f"• {title} "
    p.font.name = FONT_NAME
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON
    run = p.add_run()
    run.text = desc
    run.font.name = FONT_NAME
    run.font.size = Pt(13)
    run.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(6)

add_footer(slide10, 10)

# ==================== SLIDE 11: REFERENCES ====================
slide11 = prs.slides.add_slide(blank_layout)
add_slide_heading(slide11, "9. References")

tf11 = slide11.shapes.add_textbox(Emu(600000), Emu(1950000), Emu(7944000), Emu(2800000)).text_frame
tf11.word_wrap = True

references = [
    "[1] X. Xie, F. Ding, Y. Chen, and D. Jiang, \"Global spatiotemporal evolution of compound heatwave–drought events and ENSO modulation,\" Climate Dynamics, vol. 64, no. 9, 2026. doi: 10.1007/s00382-026-08365-z.",
    "[2] M. M. U. Qureshi, A. B. Ahmed, A. Dulmini, M. M. H. Khan, and R. Rois, \"Developing a seasonal-adjusted machine-learning-based hybrid time-series model to forecast heatwave warning,\" Scientific Reports, vol. 15, no. 8699, 2025. doi: 10.1038/s41598-025-93227-7.",
    "[3] A. R. Zarei, \"Medium-term monitoring and machine learning-based forecasting of drought dynamics in Iran,\" Scientific Reports, vol. 16, no. 14303, 2026. doi: 10.1038/s41598-026-45031-0.",
    "[4] India Meteorological Department (IMD), \"Climate Data Services Portal - High Resolution Daily Gridded Temperature Data (1997–2023),\" Ministry of Earth Sciences, Govt. of India.",
    "[5] NASA POWER Project, \"Prediction of Worldwide Energy Resources - Daily Agroclimatology Methodology,\" NASA Langley Research Center, 2023.",
    "[6] National Oceanic and Atmospheric Administration (NOAA) Climate Prediction Center, \"Oceanic Niño Index (ONI) Operational Monitoring,\" NOAA, 2024.",
    "[7] S. M. Lundberg and S.-I. Lee, \"A Unified Approach to Interpreting Model Predictions,\" Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017."
]

for ref in references:
    p = tf11.add_paragraph() if tf11.paragraphs[0].text else tf11.paragraphs[0]
    p.text = ref
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLACK
    p.space_after = Pt(10)

add_footer(slide11, 11)

# ==================== SLIDE 12: THANK YOU & Q&A ====================
slide12 = prs.slides.add_slide(blank_layout)
add_header_banner(slide12)

tf12 = slide12.shapes.add_textbox(Emu(500000), Emu(1600000), Emu(8144000), Emu(3000000)).text_frame
tf12.word_wrap = True

p = tf12.paragraphs[0]
p.text = "Thank You!"
p.font.name = FONT_NAME
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(8)

p = tf12.add_paragraph()
p.text = "Questions & Answers (Q&A)"
p.font.name = FONT_NAME
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(24)

p = tf12.add_paragraph()
p.text = "Project Deployment & Code Links:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(6)

p = tf12.add_paragraph()
p.text = "Live Dashboard Application: https://pbl-project.streamlit.app\nGitHub Repository: https://github.com/mittalpatel1-cell/ExtremeEventWarning13"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(20)

p = tf12.add_paragraph()
p.text = "Contact Details:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_MAROON
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(6)

p = tf12.add_paragraph()
p.text = "Mittal Patel: mittal.patel1@somaiya.edu   |   Hetvi Mehta: hetvi.mehta@somaiya.edu   |   Jahnvi Patel: jahnvi.patel@somaiya.edu\nGuide: Mrs. Sheetal Jagtap | Department of AI&DS, KJSIT"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.color.rgb = COLOR_BLACK
p.alignment = PP_ALIGN.CENTER

add_footer(slide12, 12)

# Global font enforcement pass
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                p.font.name = FONT_NAME
                for r in p.runs:
                    r.font.name = FONT_NAME
        elif shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    for p in cell.text_frame.paragraphs:
                        p.font.name = FONT_NAME
                        for r in p.runs:
                            r.font.name = FONT_NAME

out_path_docs = "/Users/mittal/Downloads/ExtremeEventWarning/docs/PBL_Presentation.pptx"
out_path_root = "/Users/mittal/Downloads/ExtremeEventWarning/PBL_Presentation.pptx"

prs.save(out_path_docs)
prs.save(out_path_root)
print("Saved final presentation to:", out_path_docs)
print("Saved copy to:", out_path_root)
