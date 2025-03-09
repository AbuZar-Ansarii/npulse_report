from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,  # Ensure PageBreak is imported
)
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from .styling import Styles  # Assuming this is your custom styling module

# Initialize your custom styles
styless = Styles()

def add_dinacharya_routine(elements, routine_data, available_width):
    # Stylesheet
    styles = getSampleStyleSheet()
    
    # Body Text Style
    body_style = ParagraphStyle(
        name='Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        spaceBefore=0,  # Reduce space before the description

        alignment=TA_JUSTIFY,
        textColor=colors.black,
        leftIndent=0,    # Ensure no indentation
        rightIndent=0,   # Ensure no indentation
    )
    
    # Card Style
    card_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.83, 0.83, 0.83, alpha=0.2)),  # Light grey background
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Uncomment the next line for debugging table boundaries
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.red),
    ])
    
    # Add Initial Spacer
    elements.append(Spacer(1, 10))
    
    # Add Title
    elements.append(Paragraph("Your Personalized Dinacharya", styless.get_style('CustomTitle')))
    elements.append(Spacer(1, 5))
    
    # Introduction Text
    intro_text = """
    A daily routine designed to balance your doshas and enhance your well-being. Following this routine helps harmonize your body's natural rhythms with the cycles of nature, promoting optimal health and vitality.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 20))
        
    # Add Routine Items with Background Cards
    for idx, item in enumerate(routine_data, start=1):
        # Time and Activity Heading
        time_heading = f"{item['time']} - {item['activity']}"
        heading_para = Paragraph(time_heading, styless.get_style('CustomSubSubtitle1'))
        
        # Description
        description = f"{item['description']}"
        body_para = Paragraph(description, body_style)
        
        # Create a table with a single column spanning the full available width
        card_table = Table(
            [[heading_para], [body_para]],
            colWidths=[available_width]  # Single column with full available width
        )
        card_table.setStyle(card_style)
        
        # Add the table (card) to the elements
        elements.append(card_table)
        elements.append(Spacer(1, 0.1 * inch))  # Space between cards
        
        # Insert PageBreak only after the 4th item (once)
        if idx == 4:
            elements.append(PageBreak())
    
    # Optional: Add a PageBreak at the end if desired
    elements.append(PageBreak())

