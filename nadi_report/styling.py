from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

class Styles:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles()

    def custom_styles(self):
        # Text Styles
        self.styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=self.styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=26,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#000000'),
        ))
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            fontSize=13,
            leading=20,
            alignment=TA_LEFT,
            spaceAfter=12,
            textColor = colors.Color(0, 0, 0, alpha=0.8),  # Black with 80% opacity
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomSubSubtitle',
            fontSize=13,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=10,
            textColor=colors.HexColor('#008080'),  # 80% teal
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomSubSubtitle1',
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=10,
            textColor=colors.HexColor('#008080'),  # 80% teal
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            fontSize=12,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=8,
            textColor=colors.HexColor("#333333")
        ))
        # Note Style
        self.styles.add(ParagraphStyle(
            name='CustomNote',
            fontName='Helvetica-Oblique',
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=10,
            textColor=colors.HexColor("#7D7D7D"),
            italic=True
        ))

        # CustomValue Style
        self.styles.add(ParagraphStyle(
            name='CustomValue',
            fontSize=12,
            leading=15,
            alignment=TA_RIGHT,
            spaceAfter=8,
            textColor=colors.black
        ))
        
        

    def get_style(self, style_name):
        return self.styles[style_name]

    def get_info_table_style(self):
        return TableStyle([

        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F5F5F5")),  # Very Light Grey Background for labels
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#3e4040")),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
    ])

    def get_top_table_style(self):
        return TableStyle([
            # Left-align the heading row (header)
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Ensure header is aligned to the left
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.5, 0.5, 0.5, alpha=0.2)),  # Grey with 90% opacity
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 11),

            # Body styling
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Align body rows to the left
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F9F9F9")),
            
            # Grid styling
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ])



    def get_vital_signs_table_style(self):
        return TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B9CD3")),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),               # Header text color
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),            # Header font
            ('FONTSIZE', (0, 0), (-1, 0), 12),                          # Header font size

            # Row styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),        # Default row background
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),             # Alternate row background
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),               # Grid lines
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),                       # Align first column to center
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),                        # Align other columns to left
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),                     # Vertical alignment
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),                # Body font
            ('FONTSIZE', (0, 1), (-1, -1), 11),                         # Body font size

            # Alternating row colors
            ('BACKGROUND', (0, 1), (-1, 1), colors.whitesmoke),
            ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
            ('BACKGROUND', (0, 3), (-1, 3), colors.whitesmoke),
            # Continue pattern as needed
        ])


    def food_reccomedation_table_style(self):
        return  TableStyle([
        # Header styling
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Left-align the header
            # ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F8FF")),  # Light blue background for header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Black text color for header
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
            ('FONTSIZE', (0, 0), (-1, 0), 13),  # Font size for header

            # Body styling
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Left-align the body text
            ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.83, 0.83, 0.83, alpha=0.2)),  # Light gray with 50% opacity
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text color for body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for body
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Font size for body

            # Padding and alignment for all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment in the middle
            ('TOPPADDING', (0, 0), (-1, -1), 12),  # Increase top padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Increase bottom padding
            ('LEFTPADDING', (0, 0), (-1, -1), 20),  # Left padding of 10 units
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Right padding of 10 units
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.white),  # Line below the header row
    ])