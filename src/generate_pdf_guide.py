import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas for adding page numbers and running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SaaS Customer Churn & Revenue Intelligence — Project & Interview Master Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Confidential | Prepared for Resume & Technical Interview Preparation")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_master_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=60
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    accent_color = colors.HexColor("#2563EB")     # Blue 600
    subtext_color = colors.HexColor("#475569")    # Slate 600
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    card_border = colors.HexColor("#CBD5E1")      # Slate 300
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=subtext_color,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=primary_color,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=TA_LEFT,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        spaceAfter=4
    )
    
    q_style = ParagraphStyle(
        'Q_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    
    a_style = ParagraphStyle(
        'A_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor("#334155"),
        leftIndent=8,
        spaceAfter=5
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []
    
    # -------------------------------------------------------------
    # TITLE & HEADER BLOCK
    # -------------------------------------------------------------
    story.append(Paragraph("SaaS & E-Commerce Customer Churn & Revenue Intelligence", title_style))
    story.append(Paragraph("<b>Comprehensive Resume, Data Provenance & Technical Interview Preparation Master Guide</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=2, spaceAfter=8))
    
    # -------------------------------------------------------------
    # SECTION 1: DATA PROVENANCE (DATA KAHA SE AAYA & KISKA DATA HE)
    # -------------------------------------------------------------
    story.append(Paragraph("1. Data Provenance & Origin (Data Kahan Se Aaya & Kiska Hai?)", h1_style))
    story.append(Paragraph(
        "<b>Q: Is this real customer data, or where did it come from?</b><br/>"
        "This dataset is an <b>Enterprise-Simulated SaaS & E-Commerce Telemetry Dataset (12,500 Customer Accounts, $19.02M ARR)</b> modeled strictly on real-world subscription unit economics from benchmark B2B/B2C SaaS companies (like Stripe, Chargebee, HubSpot, and Salesforce).",
        body_style
    ))
    story.append(Paragraph(
        "<b>How to answer in an Interview:</b><br/>"
        "<i>'The data represents a mid-market multi-tier B2B SaaS and subscription commerce enterprise operating across Starter, Professional, Enterprise, and Growth tiers. Because enterprise customer transaction telemetry contains sensitive PII and confidential financial records, the dataset was generated using rigorous probabilistic business rules—reflecting authentic distributions of churn curves, ticket escalation frequencies, payment gateway failure patterns, and customer health score decay.'</i>",
        a_style
    ))
    story.append(Paragraph("<b>Key Parameters & Realism Built into the Data:</b>", h2_style))
    story.append(Paragraph("• <b>12,500 Customer Profiles:</b> Spanning 4 plans ($49/mo Starter to $999/mo Enterprise) across 2 years of history.", bullet_style))
    story.append(Paragraph("• <b>Multi-Table Relational Schema:</b> Telemetry spans 4 raw sources: Customers, Subscriptions, Usage Events, and Support Tickets.", bullet_style))
    story.append(Paragraph("• <b>True Business Signals:</b> Involuntary churn (payment failure), voluntary churn (usage drop >40%), ticket resolution delays, and contract duration effects.", bullet_style))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 2: RESUME BULLETS (COPY-PASTE READY)
    # -------------------------------------------------------------
    story.append(Paragraph("2. Resume Description & STAR Bullet Points", h1_style))
    story.append(Paragraph("<b>Project Title:</b> SaaS Customer Churn & Revenue Intelligence Platform", h2_style))
    story.append(Paragraph("<b>Core Stack:</b> SQL, Python (Pandas, Scikit-Learn), Power BI (DAX), SQLite, Star Schema Data Modeling", body_style))
    
    bullets = [
        "<b>Data Engineering & Architecture:</b> Built an end-to-end analytics pipeline transforming 12,500 customer transaction records ($19.02M ARR) into an optimized Star Schema SQLite warehouse (Fact_Subscriptions, Dim_Customers, Dim_Plans, Dim_Date).",
        "<b>Advanced SQL Cohort Modeling:</b> Authored complex SQL CTEs and Window Functions (LAG, LEAD, ROW_NUMBER) to calculate dynamic Month-0 to Month-12 cohort retention matrices and subscription expansion velocity.",
        "<b>Predictive Machine Learning:</b> Trained and deployed a Logistic Regression churn risk classifier achieving <b>87.5% Recall</b> (0.88 ROC-AUC), identifying high-risk accounts 30-60 days before contract expiration.",
        "<b>Executive Power BI Dashboard:</b> Engineered a 3-page interactive Power BI reporting suite backed by <b>26 production DAX measures</b> (MRR, ARR, NRR, LTV, ARPU, Quick Ratio) with dynamic drill-throughs.",
        "<b>Financial Strategy & ROI:</b> Modeled 4 proactive retention interventions projected to recover <b>$1.18M in at-risk ARR</b> at an estimated <b>737.5% first-year ROI</b>."
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------
    # SECTION 3: TECH STACK MATRIX
    # -------------------------------------------------------------
    story.append(Paragraph("3. Skills & Technologies Used", h1_style))
    
    table_data = [
        [Paragraph("Category", table_header), Paragraph("Technology / Tool", table_header), Paragraph("Key Applied Use Case in Project", table_header)],
        [Paragraph("<b>Languages</b>", table_cell), Paragraph("Python 3.10+, SQL", table_cell), Paragraph("ETL pipelines, data cleaning, ML model training, and CTE analytics", table_cell)],
        [Paragraph("<b>BI & Visualization</b>", table_cell), Paragraph("Power BI Desktop, DAX", table_cell), Paragraph("3-page executive suite, 26 DAX measures, Star schema data model", table_cell)],
        [Paragraph("<b>Database & Storage</b>", table_cell), Paragraph("SQLite, Relational Star Schema", table_cell), Paragraph("Fact & Dimension tables, primary/foreign key indexing, ACID queries", table_cell)],
        [Paragraph("<b>Data Science & ML</b>", table_cell), Paragraph("Pandas, Scikit-Learn, NumPy", table_cell), Paragraph("Feature engineering, logistic regression, confusion matrix, ROC-AUC", table_cell)],
        [Paragraph("<b>Version Control</b>", table_cell), Paragraph("Git, GitHub", table_cell), Paragraph("Source code versioning, automated workflows, technical markdown specs", table_cell)]
    ]
    
    t = Table(table_data, colWidths=[90, 125, 289])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), accent_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, card_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 4: STEP-BY-STEP WORKFLOW
    # -------------------------------------------------------------
    story.append(Paragraph("4. End-to-End Workflow: Step-by-Step Breakdown", h1_style))
    steps = [
        ("Step 1: Data Ingestion & ETL", "Cleaned raw transaction data, handled null values, normalized date timestamps, and cast data types using automated Python Pandas scripts."),
        ("Step 2: Star Schema Modeling", "Designed 1 central Fact table (Fact_Subscriptions) and 4 Dimension tables (Dim_Customers, Dim_Plans, Dim_Date, Dim_ChurnReason) in SQLite to optimize DAX analytical queries."),
        ("Step 3: SQL Cohort Retention Analytics", "Wrote multi-stage CTEs calculating Month 0 to Month 12 retention rates, identifying that Month 3 experienced the steepest retention drop (18.4% drop)."),
        ("Step 4: Machine Learning Risk Scoring", "Engineered features (login decay, unresolved tickets, billing retry count) and trained a classification model with 87.5% Recall to flag churners before expiration."),
        ("Step 5: Executive Power BI Reporting", "Created 3 dashboards: Executive SaaS Overview, Cohort Lifecycle, and Risk Intelligence with 26 DAX measures (MRR, NRR, LTV, Quick Ratio)."),
        ("Step 6: Financial Impact Modeling", "Calculated $1.18M ARR recoverable across 4 targeted interventions with an implementation cost of $141k (737.5% ROI).")
    ]
    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 5: 60-SECOND ELEVATOR PITCH
    # -------------------------------------------------------------
    story.append(Paragraph("5. 60-Second Interview Elevator Pitch", h1_style))
    story.append(Paragraph(
        "<i>'In my recent project, I built an end-to-end SaaS Churn and Revenue Intelligence platform analyzing 12,500 customer accounts and $19.02M in ARR. The primary business problem was high voluntary churn in the early 90 days and involuntary churn due to billing failures.<br/><br/>"
        "I designed a Star Schema SQLite data warehouse via an automated Python ETL pipeline, wrote advanced SQL CTEs and Window Functions for M0–M12 cohort retention matrices, and trained an ML classification model with 87.5% recall to predict churn ahead of time.<br/><br/>"
        "Finally, I built a 3-page Power BI dashboard with 26 DAX measures and modeled 4 strategic business interventions that can recover $1.18M in ARR at a 737.5% ROI.'</i>",
        a_style
    ))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 6: TOP 10 INTERVIEW QUESTIONS & MODEL ANSWERS
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("6. Top 10 Technical & Business Interview Questions & Answers", h1_style))
    
    qa_list = [
        (
            "Q1: Why did you choose a Star Schema over a single flat CSV table?",
            "Flat tables create massive data redundancy and slow down analytical queries. A Star Schema separates numerical measurements (Fact_Subscriptions) from descriptive attributes (Dim_Customers, Dim_Plans, Dim_Date). This enables Power BI's VertiPaq engine to perform highly efficient 1-to-many relationship filtering, reduces memory footprint, and enforces referential integrity."
        ),
        (
            "Q2: How did you calculate Cohort Retention in SQL? Walk me through the query logic.",
            "I structured a 3-stage SQL CTE: (1) First CTE finds each customer's MIN(start_date) to assign their Cohort Month. (2) Second CTE joins all subsequent active subscription months, calculating Month_Offset (0 to 12) via DATEDIFF. (3) Final query calculates COUNT(DISTINCT customer_id) active in each offset divided by the base Month 0 cohort size to derive the retention percentage."
        ),
        (
            "Q3: Why did you prioritize Recall over Accuracy or Precision in your ML Churn model?",
            "In customer churn prediction, False Negatives (predicting a churning customer as 'Safe') are extremely expensive because the business loses the chance to intervene and retain them. False Positives only result in an extra customer success outreach email. Optimizing for Recall (87.5%) ensures we capture the maximum volume of at-risk revenue."
        ),
        (
            "Q4: What is Net Revenue Retention (NRR) and how did you write its DAX formula?",
            "NRR measures the percentage of recurring revenue retained from existing customers over a period, factoring in expansions (upgrades) minus contractions (downgrades) and churn. An NRR > 100% indicates organic account expansion. DAX Formula:<br/>"
            "<code>[NRR %] = DIVIDE([Starting MRR] + [Expansion MRR] - [Churn MRR] - [Downgrade MRR], [Starting MRR], 0)</code>"
        ),
        (
            "Q5: What were the top 3 root causes of churn identified in your analysis?",
            "1. <b>90-Day Onboarding Cliff:</b> Highest drop occurred between Month 1 and Month 3 on monthly plans.<br/>"
            "2. <b>Support Ticket Escalation:</b> Accounts with >=3 unresolved high-priority tickets had a 4.2x higher churn hazard rate.<br/>"
            "3. <b>Payment Gateway Delays (Involuntary Churn):</b> 22% of churn was due to expired cards and repeated billing retries."
        ),
        (
            "Q6: How did you handle data cleaning and missing values in Python ETL?",
            "Missing cancellation dates were explicitly kept as NULL to represent active subscriptions without corrupting tenure calculations. Plan names and categorical dimensions were standardized (trimmed whitespace, uppercase normalization) to prevent join mismatches. Primary and Foreign key constraints were validated before loading into SQLite."
        ),
        (
            "Q7: How did you calculate the $1.18M ARR recovery and 737.5% ROI figure?",
            "Total at-risk ARR was ~$3.5M. I modeled 4 interventions with conservative recovery rates: (1) Smart Dunning/Payment Retries ($280k saved), (2) Customer Success Outreach ($420k saved), (3) 90-Day Onboarding Overhaul ($350k saved), and (4) Annual Plan Discount Incentives ($130k saved). Total saved = $1.18M. Subtracting the $141k program implementation cost yielded an ROI of ($1.18M - $141k)/$141k = 737.5%."
        ),
        (
            "Q8: What is the SaaS Quick Ratio and why is it important?",
            "The Quick Ratio evaluates revenue growth reliability: <code>([New MRR] + [Expansion MRR]) / ([Churn MRR] + [Contraction MRR])</code>. A ratio > 4.0 indicates hyper-growth efficiency, while < 1.0 indicates a shrinking business. In our dataset, it stood at 2.85."
        ),
        (
            "Q9: How did you design the Customer Health Score?",
            "It is a weighted 0–100 composite index: 35% Product Usage Frequency (login trends), 25% Feature Adoption Breadth, 20% Support Ticket Sentiment/Resolution, and 20% Payment Reliability. Scores <40 are classified as 'Critical Risk', 40–70 as 'Moderate Risk', and >70 as 'Healthy'."
        ),
        (
            "Q10: If data scaled to 100M+ event rows, how would you modify this architecture?",
            "I would migrate SQLite to a cloud data warehouse like Snowflake or Google BigQuery. The Python ETL script would transition to Apache Spark / PySpark or dbt for scalable transformation, and Power BI would switch to Composite Mode with Aggregation Tables over DirectQuery."
        )
    ]
    
    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", q_style))
        story.append(Paragraph(a, a_style))
        story.append(Spacer(1, 4))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "SaaS_Churn_Project_Resume_Interview_MasterGuide.pdf")
    create_master_guide_pdf(out_file)
