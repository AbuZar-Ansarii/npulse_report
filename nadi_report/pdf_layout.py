# comprehensive_dosha_report.py

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image as ReportImage,
    PageBreak
)
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime
from .report_header import add_header  # Ensure this path is correct
from .styling import Styles  # Ensure this is defined or adjust accordingly


class PDFLayout:
    """
    Handles the layout configuration for the PDF, including Frames and PageTemplates.
    """
    def __init__(self, doc: BaseDocTemplate):
        """
        Initializes the PDFLayout with the given document and logo path.
        :param doc: An instance of BaseDocTemplate.
        :param logo_path: Path to the logo image.
        """
        self.doc = doc
        self.setup_templates()

    def setup_templates(self):
        """
        Sets up the Frames and PageTemplates for the first and subsequent pages.
        """
        # Frame for the first page with higher top padding (e.g., 60 units reserved for header)
        frame_first_page = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            self.doc.height - 60,  # Adjust as per header height
            id='first_page'
        )

        # Frame for subsequent pages with 30 units top padding
        frame_later_pages = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            self.doc.height - 30,  # 30 units top padding
            id='later_pages'
        )

        # Define PageTemplate for the first page
        template_first_page = PageTemplate(
            id='FirstPage',
            frames=frame_first_page,
            onPage=lambda canvas, doc: add_header(canvas, doc, first_page=True)
        )

        # Define PageTemplate for subsequent pages
        template_later_pages = PageTemplate(
            id='LaterPages',
            frames=frame_later_pages,
            onPage=lambda canvas, doc: add_header(canvas, doc, first_page=False)
        )

        # Add PageTemplates to the document
        self.doc.addPageTemplates([template_first_page, template_later_pages])

