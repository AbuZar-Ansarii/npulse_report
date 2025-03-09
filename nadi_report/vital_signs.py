from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from .styling import Styles

styles = Styles()

def add_vital_signs(elements, vital_signs):
    elements.append(Paragraph("Vital Signs", styles.get_style('CustomSubtitle')))
    vital_signs_data = [
        ["Vital", "Your Value", "Average Value"],
        ["Blood Pressure", vital_signs['bp'], "120/80 mmHg"],
        ["Heart Rate", vital_signs['hr'], "60-100 bpm"],
        ["Respiratory Rate", vital_signs['rr'], "12-20 breaths/min"],
        ["Temperature", vital_signs['temp'], "98.6°F (37°C)"],
        ["SpO2", vital_signs['spo2'], "95-100%"]
    ]
    
    # Increase column widths
    vital_table = Table(vital_signs_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch], hAlign='LEFT')
    vital_table.setStyle(styles.get_top_table_style())
    
    # Increase row heights by adding padding
    vital_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
                                      ('TOPPADDING', (0, 0), (-1, -1), 12),  # Increase top padding
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 12)]))  # Increase bottom padding

    elements.append(vital_table)
    elements.append(Spacer(1, 0.5 * inch))  # Increase spacer size if needed
