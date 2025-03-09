#dosha description.py

from reportlab.platypus import Paragraph, Spacer, Table
from .styling import Styles
import os
from reportlab.platypus import Paragraph, Spacer, Table
from .styling import Styles
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle, PageBreak
from reportlab.lib.pagesizes import letter

#  import page break
# from reportlab.platypus import PageBreak


styles = Styles()

# Main function to add dosha analysis and profiles to the report
# Main function to add dosha analysis, profiles, and vitals table to the report
def add_dosha_analysis_and_profiles(elements, dosha_analysis, nadi_check_data):
    # -------------- Dosha Analysis --------------
    elements.append(Paragraph("Dosha Analysis", styles.get_style('CustomTitle')))
    dosha_data = f"<font color='#008080'>Vata: <b>{dosha_analysis['vata']}%</b> | Pitta: <b>{dosha_analysis['pitta']}%</b> | Kapha: <b>{dosha_analysis['kapha']}%</b></font>"

    elements.append(Paragraph(dosha_data, styles.get_style('CustomNormal')))
    elements.append(Spacer(1, 0.2 * inch))

    # Add Detailed Dosha Profiles
    add_dosha_profiles(elements, styles, dosha_analysis['vata'], dosha_analysis['pitta'], dosha_analysis['kapha'])

    # Add space between sections
    elements.append(Spacer(1, 30))


    # Dosha Vitals Table
    elements.append(Paragraph("Dosha Vitals", styles.get_style('CustomTitle')))
    

    dosha_table_data = [
        ["Parameter", "Kapha", "Pitta", "Vata"],
        ["HR", nadi_check_data["Kapha"]["HR"], nadi_check_data["Pitta"]["HR"], nadi_check_data["Vatta"]["HR"]],
        ["HRV", nadi_check_data["Kapha"]["HRV"], nadi_check_data["Pitta"]["HRV"], nadi_check_data["Vatta"]["HRV"]],
        ["PV", nadi_check_data["Kapha"]["PV"], nadi_check_data["Pitta"]["PV"], nadi_check_data["Vatta"]["PV"]],
        ["PA", nadi_check_data["Kapha"]["PA"], nadi_check_data["Pitta"]["PA"], nadi_check_data["Vatta"]["PA"]],
        ["MST", nadi_check_data["Kapha"]["MST"], nadi_check_data["Pitta"]["MST"], nadi_check_data["Vatta"]["MST"]],
    ]

    # Set column widths for full width usage
    dosha_table = Table(dosha_table_data,colWidths=[1.85 * inch, 1.85 * inch, 1.85 * inch], hAlign='LEFT')
    dosha_table.setStyle(styles.get_top_table_style())

    # Increase row heights by adding padding
    dosha_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ('TOPPADDING', (0, 0), (-1, -1), 12),  # Increase top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)  # Increase bottom padding
    ]))

    # Append the table to elements
    elements.append(dosha_table)
    elements.append(Spacer(1, 0.5 * inch))


    #  add page break
    elements.append(PageBreak())

    # Add Dosha Vitals Explanation Section
    add_dosha_vitals_explanation(elements, styles)


# Function to add Dosha Vitals Explanation
def add_dosha_vitals_explanation(elements, styles: Styles):
    elements.append(Paragraph("Dosha Vitals Explanation", styles.get_style('CustomTitle')))
    elements.append(Spacer(1, 0.1 * inch))

    explanation_data = [
        ("HR (Heart Rate)", "The number of heartbeats per minute. Normal range: 60-100 bpm. Linked to Pitta dosha, indicating cardiovascular health."),
        ("HRV (Heart Rate Variability)", "Variation in time between heartbeats. Higher HRV shows better stress management. Reflects Vata and Pitta balance."),
        ("PV (Pulse Volume)", "Strength of the pulse, indicating blood flow. Stronger pulse means good circulation. Reflects balance in doshas."),
        ("PA (Pulse Amplitude)", "Height of the pulse wave, showing arterial health. Higher amplitude means healthier arteries, linked to Kapha dosha."),
        ("MST (Mean Skin Temperature)", "Average skin temperature, reflecting metabolic activity. Connected to Pitta dosha and body heat regulation.")
    ]

    for title, description in explanation_data:
        elements.append(Paragraph(f"<b>{title}</b>", styles.get_style('CustomSubSubtitle')))
        elements.append(Paragraph(description, styles.get_style('CustomNormal')))
        elements.append(Spacer(1, 12))
        
# Function to add dosha profiles to the report
def add_dosha_profiles(elements, styles: Styles, vata, pitta, kapha):
    doshas = [
        {'name': 'Vata', 'percentage': vata, 'description': vata_description()},
        {'name': 'Pitta', 'percentage': pitta, 'description': pitta_description()},
        {'name': 'Kapha', 'percentage': kapha, 'description': kapha_description()},
    ]

    for dosha in doshas:
        elements.append(Paragraph(f"{dosha['name']} Dosha", styles.get_style('CustomSubSubtitle')))
        elements.append(Spacer(1, 2))

        description = (
            f"{dosha['description']} Your current balance is <b>{dosha['percentage']}%</b>, indicating "
            f"{interpret_dosha_balance(dosha['percentage'])}."
        )
        elements.append(Paragraph(description, styles.get_style('CustomNormal')))
        elements.append(Spacer(1, 12))

# Function that returns Vata description
def vata_description():
    return (
        "Vata Dosha is characterized by the elements of air and space. It governs movement and communication, "
        "influencing bodily functions such as breathing, circulation, and the nervous system."
    )

# Function that returns Pitta description
def pitta_description():
    return (
        "Pitta Dosha embodies the elements of fire and water. It is responsible for metabolism, digestion, and "
        "transformation in the body."
    )

# Function that returns Kapha description
def kapha_description():
    return (
        "Kapha Dosha consists of the elements earth and water. It provides structure, stability, and lubrication to the body."
    )

# Function to interpret dosha balance based on percentage
def interpret_dosha_balance(percentage):
    if percentage > 70:
        return "a predominant balance, indicating strong tendencies associated with this Dosha."
    elif 40 < percentage <= 70:
        return "a significant balance, suggesting noticeable traits of this Dosha."
    else:
        return "a balanced or lower presence, indicating moderate or minimal influence of this Dosha."
