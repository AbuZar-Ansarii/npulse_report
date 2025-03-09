from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from .styling import Styles

styless = Styles()

def add_yoga_recommendations(elements, yoga_data_json):
    # Define styles for the table header and body
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=TA_LEFT,  # Change alignment to left
        textColor=colors.black,
    )

    body_style = ParagraphStyle(
        name='BodyText',
        fontName='Helvetica',
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
    )

    #  Add a spacer
    # elements.append(Spacer(1, 30))
    
    # Add title
    elements.append(Paragraph("Yoga Recommendations", styless.get_style('CustomTitle')))
    # add description about yoga recommendations
    elements.append(Paragraph("Yoga is a powerful tool for maintaining physical, mental, and emotional well-being. Here are some yoga that are recommended for you, as well as some to avoid.", styless.get_style('CustomNormal')))
    elements.append(Spacer(1, 20))

    # Limit the number of items to 10 for each list
    dos_list = [item['Yoga Pose'] for item in yoga_data_json['doList'][:10]]
    donts_list = [item['Yoga Pose'] for item in yoga_data_json['dontList'][:10]]

    # Create the table header
    table_data = [
        [Paragraph("Do's", subtitle_style), Paragraph("Don'ts", subtitle_style)]
    ]

    # Find the maximum length between the two lists
    max_length = max(len(dos_list), len(donts_list))

    # Create the table data with only 10 rows max
    for i in range(max_length):
        do_item = Paragraph(dos_list[i], body_style) if i < len(dos_list) else ""
        dont_item = Paragraph(donts_list[i], body_style) if i < len(donts_list) else ""
        table_data.append([do_item, dont_item])

    # Set page width and create the table
    page_width = LETTER[0] - 1 * inch
    table = Table(table_data, colWidths=[page_width / 2, page_width / 2])

    # Table styling
    table.setStyle(styless.food_reccomedation_table_style())


    # Add table to elements
    elements.append(table)
    elements.append(Spacer(1, 20))


# Example usage
doc = SimpleDocTemplate("Yoga_Recommendations.pdf", pagesize=LETTER)
elements = []

