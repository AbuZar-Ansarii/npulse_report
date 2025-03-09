import os
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime

import os

def get_logo_path():
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__))  # Current file's directory
    
    # Move up to the project root if needed, depending on your script's location
    project_root = os.path.join(project_root, "..")  # Adjust as per your script's depth
    
    # Construct the path to the 'icons/logo.png' relative to the project root
    logo_path = os.path.join(project_root, "icons", "logo.png")

    return os.path.abspath(logo_path)  # Return the absolute path

# Example usage in your add_header function
logo_path = get_logo_path()
# print("Logo pathsssssssssssssss:", logo_path)  # Check if the path resolves correctly


def add_header(canvas, doc, first_page: bool = False):
    width, height = A4
    canvas.saveState()

    get_logo_path()
    # Construct the path correctly

    # Use relative path, assuming logo.png is in the same directory as the script
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")


    if first_page:
        # Add header content for the first page
        canvas.setFillColor(colors.HexColor("#113730"))
        canvas.rect(0, height - 60, width, 60, fill=1, stroke=0)

        if os.path.exists(logo_path):
            try:
                logo = ImageReader(logo_path)
                # print("Logo loaded successfully.")
                canvas.drawImage(logo, 30, height - 55, width=50, height=50, mask='auto')
            except Exception as e:
                print(f"Error loading logo: {e}")
        else:
            print(f"Logo not found at: {logo_path}")

        canvas.setFont("Helvetica-Bold", 20)
        canvas.setFillColor(colors.white)
        canvas.drawString(100, height - 30, "Nadi Report Summary")
        canvas.setFont("Helvetica", 12)
        canvas.drawString(100, height - 45, datetime.now().strftime("%d %B %Y"))

    # Add page number
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(colors.HexColor("#008080"))
    canvas.drawRightString(width - 30, 15, f"Page {doc.page}")
    canvas.restoreState()
