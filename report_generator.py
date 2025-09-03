from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
from datetime import datetime
from typing import Dict, Any

def generate_report(meeting_title: str, created_at: str, transcript: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate a PDF report from the analysis results
    
    Args:
        meeting_title (str): Title of the meeting
        created_at (str): Meeting creation timestamp
        transcript (str): Full transcript text
        analysis_results (Dict): Analysis results from the AI
        
    Returns:
        str: Path to the generated PDF file
    """
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sales_analysis_{timestamp}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen
    )
    
    # Build the document content
    content = []
    
    # Title page
    content.append(Paragraph("Sales Call Analysis Report", title_style))
    content.append(Spacer(1, 20))
    
    # Meeting info
    meeting_info = [
        ["Meeting Title:", meeting_title],
        ["Date:", created_at],
        ["Overall Score:", f"{analysis_results.get('overall_score', 0)}/100"],
        ["Analysis Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]
    
    info_table = Table(meeting_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(info_table)
    content.append(Spacer(1, 30))
    
    # Overall Performance Summary
    content.append(Paragraph("Overall Performance Summary", heading_style))
    summary_text = analysis_results.get('summary', 'No summary available.')
    content.append(Paragraph(summary_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Score Breakdown
    content.append(Paragraph("Score Breakdown", heading_style))
    
    categories = analysis_results.get('categories', {})
    category_names = {
        'needs_discovery': 'Needs Discovery (25 pts)',
        'pain_point_exploration': 'Pain Point Exploration (25 pts)',
        'consequence_urgency': 'Consequence & Urgency (15 pts)',
        'obstacle_handling': 'Obstacle Handling (15 pts)',
        'objection_handling': 'Objection Handling (10 pts)',
        'next_steps_closing': 'Next Steps & Closing (10 pts)'
    }
    
    score_data = [["Category", "Score", "Weighted Score"]]
    total_weighted = 0
    
    weights = {
        'needs_discovery': 25,
        'pain_point_exploration': 25,
        'consequence_urgency': 15,
        'obstacle_handling': 15,
        'objection_handling': 10,
        'next_steps_closing': 10
    }
    
    for key, name in category_names.items():
        category_data = categories.get(key, {})
        score = category_data.get('score', 0)
        weight = weights.get(key, 0)
        weighted_score = (score * weight) / 10
        total_weighted += weighted_score
        
        score_data.append([name, f"{score}/10", f"{weighted_score:.1f}/{weight}"])
    
    score_data.append(["TOTAL", "", f"{total_weighted:.1f}/100"])
    
    score_table = Table(score_data, colWidths=[3.5*inch, 1*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(score_table)
    content.append(Spacer(1, 20))
    
    # Payment Detection
    payment_detected = analysis_results.get('payment_detected', 'Unknown')
    if payment_detected != 'Unknown':
        content.append(Paragraph(f"Payment Method Detected: {payment_detected}", subheading_style))
        content.append(Spacer(1, 10))
    
    # Detailed Analysis for each category
    content.append(PageBreak())
    content.append(Paragraph("Detailed Category Analysis", heading_style))
    
    for key, name in category_names.items():
        category_data = categories.get(key, {})
        
        if not category_data:
            continue
            
        content.append(Paragraph(name, subheading_style))
        
        # Score
        score = category_data.get('score', 0)
        content.append(Paragraph(f"Score: {score}/10", styles['Normal']))
        content.append(Spacer(1, 10))
        
        # Highlights
        highlights = category_data.get('highlights', [])
        if highlights:
            content.append(Paragraph("What Went Well:", styles['Heading4']))
            for highlight in highlights:
                content.append(Paragraph(f"• {highlight}", styles['Normal']))
            content.append(Spacer(1, 10))
        
        # Missed Opportunities
        missed = category_data.get('missed_opportunities', [])
        if missed:
            content.append(Paragraph("Missed Opportunities:", styles['Heading4']))
            for opportunity in missed:
                content.append(Paragraph(f"• {opportunity}", styles['Normal']))
            content.append(Spacer(1, 10))
        
        # Feedback
        feedback = category_data.get('feedback', [])
        if feedback:
            content.append(Paragraph("Actionable Feedback:", styles['Heading4']))
            for suggestion in feedback:
                content.append(Paragraph(f"• {suggestion}", styles['Normal']))
        
        content.append(Spacer(1, 20))
    
    # Full Transcript (on separate page)
    content.append(PageBreak())
    content.append(Paragraph("Full Transcript", heading_style))
    
    # Split transcript into smaller chunks for better formatting
    transcript_lines = transcript.split('\n')
    for line in transcript_lines:
        if line.strip():
            content.append(Paragraph(line, styles['Normal']))
    
    # Build PDF
    doc.build(content)
    
    return filepath

