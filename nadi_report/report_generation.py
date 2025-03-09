# comprehensive_dosha_report.py

import os
import tempfile
import uuid
import logging
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    Paragraph,
    Spacer,
    Image as ReportImage,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet

from .dosha_chart_generation import create_circular_progress
from .dosha_description import add_dosha_analysis_and_profiles
from .vital_signs import add_vital_signs
from .styling import Styles
from .pdf_layout import PDFLayout
from .graph_chart import add_graphs_to_pdf, create_line_graphs
from .curated_recommendations import add_curated_recommendations
from .dinacharya_routine import add_dinacharya_routine
from .yoga_suggestions import add_yoga_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_comprehensive_pdf(
    filename,
    patient_data,
    doctor_data,
    vital_signs,
    dosha_analysis,
    vital_signs_data,
    nadi_check_data,
    chart_data1,
    food_data_json,
    yoga_data,
    routine_data,
):
    """
    Generates a comprehensive Dosha Analysis PDF report.

    Args:
        filename (str): The output PDF filename.
        patient_data (dict): Patient information.
        doctor_data (dict): Doctor information.
        vital_signs (dict): Vital signs details.
        dosha_analysis (dict): Dosha analysis data.
        logo_path (str): Path to the clinic logo.
        icons_path (str): Path to the icons used in the dosha chart.
        vital_signs_data (dict): Detailed vital signs data.
        nadi_check_data (dict): Nadi check data.
        chart_data1 (dict): Data for generating charts.
        food_data_json (dict): Curated food recommendations.
        yoga_data (dict): Yoga recommendations.
        routine_data (dict): Dinacharya routine data.
    """
    # Initialize temporary file paths with unique identifiers to handle concurrency
    temp_files = []
    try:
        # Generate unique temporary filenames for graphs
        temp_dir = tempfile.gettempdir()
        unique_id = uuid.uuid4().hex

        output_path_vatta = os.path.join(temp_dir, f"vatta_graph_{unique_id}.png")
        output_path_pitta = os.path.join(temp_dir, f"pitta_graph_{unique_id}.png")
        output_path_kapha = os.path.join(temp_dir, f"kapha_graph_{unique_id}.png")
        output_path_combined = os.path.join(temp_dir, f"combined_graph_{unique_id}.png")
        temp_files.extend([output_path_vatta, output_path_pitta, output_path_kapha, output_path_combined])

        # Create circular dosha progress chart
        chart_path = create_circular_progress(
            dosha_analysis.get('vata', 0),
            dosha_analysis.get('pitta', 0),
            dosha_analysis.get('kapha', 0),
        )
        temp_files.append(chart_path)

        # Define page size and margins
        page_size = A4
        margin = 30  # 30 points margins on all sides

        # Calculate available width and height
        available_width = page_size[0] - 2 * margin  # 595 - 60 = 535 points
        available_height = page_size[1] - 2 * margin  # 842 - 60 = 782 points


        # Create the PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=page_size,
            rightMargin=margin,
            leftMargin=margin,
            topMargin=margin,
            bottomMargin=margin
        )

        layout = PDFLayout(doc)

        elements = []

        # Initialize styles
        styles = Styles()

        # Add Patient Information Section
        elements.append(Paragraph("Patient Information", styles.get_style('CustomTitle')))
        patient_info_data = [
            ["Name:", patient_data.get('name', 'N/A')],
            ["Date of Birth:", patient_data.get('dob', 'N/A')],
            ["Gender:", patient_data.get('gender', 'N/A')]
        ]

        label_width = 2 * inch
        value_width = doc.width - label_width
        patient_table = Table(patient_info_data, colWidths=[label_width, value_width])

        patient_table.setStyle(styles.get_info_table_style())
        elements.append(patient_table)
        elements.append(Spacer(1, 30))

        # Doctor Information Section
        elements.append(Paragraph("Doctor Information", styles.get_style('CustomTitle')))
        doctor_info_data = [
            ["Name:", doctor_data.get('name', 'N/A')],
            ["Specialty:", doctor_data.get('specialty', 'N/A')],
            ["Gender:", doctor_data.get('gender', 'N/A')],
            ["Clinic Name:", doctor_data.get('clinic_name', 'N/A')],
            ["Clinic Address:", doctor_data.get('clinic_address', 'N/A')],
        ]

        doctor_table = Table(doctor_info_data, colWidths=[label_width, value_width])
        doctor_table.setStyle(styles.get_info_table_style())
        elements.append(doctor_table)
        elements.append(Spacer(1, 30))

        # Insert Circular Dosha Chart with full width
        if os.path.exists(chart_path):
            elements.append(Paragraph("Vikriti", styles.get_style('CustomTitle')))

            # Use full document width for the chart
          # Use full document width for the chart
            chart_width = doc.width
            chart = ReportImage(chart_path, width=chart_width, height=(chart_width / 3))  # Adjust height to maintain aspect ratio
            elements.append(chart)
            elements.append(Spacer(1, 30))
        else:
            logger.warning(f"Chart path '{chart_path}' does not exist. Skipping chart insertion.")

        # ------------ Vital Signs Section ------------
        elements.append(Paragraph("Vital Signs", styles.get_style('CustomTitle')))
        vital_signs_table_data = [
            ["Health Status:", vital_signs_data.get('health_status', 'N/A')],
            ["Health Index:", vital_signs_data.get('health_index', 'N/A')],
            ["Increased Doshas:", vital_signs_data.get('increased_dosha', 'N/A')]
        ]
        label_width = 2 * inch
        value_width = doc.width - label_width
        vital_signs_table = Table(vital_signs_table_data, colWidths=[label_width, value_width])

        # Apply the style to change the text color of only the second column (the values) to teal
        vital_signs_table.setStyle(TableStyle([
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor("#008080")),  # Teal color
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            # Uncomment the following line to add grid lines
            # ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ]))

        elements.append(vital_signs_table)
        # ------------ Vitals Notes Section ------------ 

        elements.append(Spacer(1, 16))
        elements.append(Paragraph("Note:", styles.get_style('CustomSubtitle')))
        elements.append(Paragraph(
            "Ranges from 0 (optimal health) to 10 (severe health issues). Lower scores denote better health; "
            "regular monitoring is advised for tracking and improvement.",
            styles.get_style('CustomNote')
        ))

        elements.append(PageBreak())

        #  ------------------------------------Page 2 --------------------------------------------------------

        # Add Dosha Analysis
        add_dosha_analysis_and_profiles(elements, dosha_analysis, nadi_check_data)

        #  add space between sections
        elements.append(Spacer(1, 30))

        # ---------- Vital Signs Section  --------------
        if vital_signs:
            add_vital_signs(elements, vital_signs)
            
        elements.append(PageBreak())

        #  ------------------------------------Page 3 --------------------------------------------------------

        # Generate the graphs and add them to the PDF using DoshaGraphHandler
        # Use unique temporary files to handle concurrency
        create_line_graphs(
            chart_data1.get('Vatta', []),
            chart_data1.get('Pitta', []),
            chart_data1.get('Kapha', []),
            output_path_combined,
            output_path_vatta,
            output_path_pitta,
            output_path_kapha
        )

        # Add the graphs to the PDF
        add_graphs_to_pdf(
            elements,
            output_path_vatta,
            output_path_pitta,
            output_path_kapha,
            output_path_combined,
            styles,
            doc
        )

        #  ------------------------------------Page 4 --------------------------------------------------------

        add_curated_recommendations(elements, food_data_json)  # Add curated recommendations for Page 4

        #  ----------- Din Charya Section --------------
        add_dinacharya_routine(elements, routine_data, available_width)

        #  --------add yoga poses section -------------
        add_yoga_recommendations(elements, yoga_data)

        # Build the PDF
        doc.build(elements)

        logger.info(f"Comprehensive Dosha Analysis PDF '{filename}' has been generated successfully!")

    except Exception as e:
        logger.error(f"An error occurred while generating the PDF: {e}")
        raise e  # Re-raise exception after logging

    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.debug(f"Temporary file '{temp_file}' has been removed.")
            except Exception as cleanup_error:
                logger.warning(f"Failed to remove temporary file '{temp_file}': {cleanup_error}")
