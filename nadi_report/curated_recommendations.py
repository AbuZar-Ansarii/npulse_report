from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak


from .styling import Styles

styless = Styles()


def add_curated_recommendations(elements, food_data_json):
    # Subtitle style (for table headers)
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    # Body text style
    body_style = ParagraphStyle(
        name='BodyText',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    elements.append(Spacer(1, 30))

#   from reportlab.platypus import PageBreak

    # Add title and description
    elements.append(Paragraph("Curated Recommendations", styless.get_style('CustomTitle')))
    elements.append(Paragraph(
        "Based on the analysis, the following recommendations are provided: "
        "These suggestions are tailored to balance your doshas and enhance your overall health. "
        "Please consume the recommended foods in moderation and avoid the ones listed. "
        "This guidance aims to support your dietary preferences while aligning with Ayurvedic principles.",
        styless.get_style('CustomNormal')))
    elements.append(Spacer(1, 12))

    # Function to create a table for each food type
    def create_table_for_category(category_name, data):
        category_display_name = f"{category_name.capitalize()}:-"
        elements.append(Paragraph(category_display_name, styless.get_style('CustomSubtitle')))
        elements.append(Spacer(1, 1))

        # Get only the first 4 items for Include and Avoid categories
        include_items = [item['Name'] for item in data['Include'][:4]]
        avoid_items = [item['Name'] for item in data['Avoid'][:4]]

        # Table data
        table_data = [[Paragraph("Consume Freely", subtitle_style), Paragraph("Consume Moderately", subtitle_style)]]
        max_rows = max(len(include_items), len(avoid_items))

        for i in range(max_rows):
            include_item = Paragraph(include_items[i], body_style) if i < len(include_items) else Paragraph("N/A", body_style)
            avoid_item = Paragraph(avoid_items[i], body_style) if i < len(avoid_items) else Paragraph("N/A", body_style)
            table_data.append([include_item, avoid_item])

        page_width = LETTER[0] - 1 * inch
        table = Table(table_data, colWidths=[page_width / 2, page_width / 2])

        # Table styling
        table.setStyle(styless.food_reccomedation_table_style())

        # Add table to elements
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Add a page break after the Vegetables category
        if category_name in ["fruits", "legumes" , "oils"]:
            elements.append(PageBreak())

    # Create tables for all categories
    for category, data in food_data_json.items():
        create_table_for_category(category, data)
