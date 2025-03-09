# dosha_chart_generation.py

import os
import uuid
import tempfile
import logging
import matplotlib.pyplot as plt

def create_circular_progress(vata, pitta, kapha):
    """
    Generates a circular progress chart for Vata, Pitta, and Kapha doshas.

    Args:
        vata (int or float): Vata dosha percentage.
        pitta (int or float): Pitta dosha percentage.
        kapha (int or float): Kapha dosha percentage.

    Returns:
        str: Path to the generated circular progress chart image.
    """
    # Configure logging
    logger = logging.getLogger(__name__)

    # Validate input percentages
    for dosha, value in zip(['Vata', 'Pitta', 'Kapha'], [vata, pitta, kapha]):
        if not isinstance(value, (int, float)):
            logger.error(f"{dosha} value must be a number. Received: {value}")
            raise ValueError(f"{dosha} value must be a number. Received: {value}")
        if not (0 <= value <= 100):
            logger.error(f"{dosha} value must be between 0 and 100. Received: {value}")
            raise ValueError(f"{dosha} value must be between 0 and 100. Received: {value}")

    sizes = [vata, pitta, kapha]
    colors_list = [
        (75/255, 74/255, 160/255, 0.7),  # Vata color with 70% opacity
        (212/255, 94/255, 47/255, 0.7),  # Pitta color with 70% opacity
        (62/255, 163/255, 65/255, 0.7)   # Kapha color with 70% opacity
    ]
    labels = ['Vata', 'Pitta', 'Kapha']

    # Create subplots for the circular progress charts
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    # Set the background color for the entire figure
    fig.patch.set_facecolor('#F9F9F9')

    for i, ax in enumerate(axs):
        try:
            # Set each axis background to #F9F9F9 to match the figure background
            ax.set_facecolor('#F9F9F9')

            # Plot a gray circle for the full background of the progress chart
            ax.pie([100], radius=1, colors=['#F0F0F0'], startangle=90, counterclock=False)

            # Plot the actual progress segment
            ax.pie(
                [sizes[i], 100 - sizes[i]],
                radius=1,
                startangle=90,
                colors=[colors_list[i], '#F0F0F0'],
                counterclock=False,
                wedgeprops={'width': 0.3, 'edgecolor': 'w', 'linewidth': 2}
            )
            
            # Add the percentage text in the center of each pie chart
            ax.text(
                0, 0.1, f"{sizes[i]}%", 
                ha='center', va='center', fontsize=14, 
                color=colors_list[i], fontweight='bold'
            )
            
            # Add the label (Vata, Pitta, Kapha) under the percentage
            ax.text(
                0, -0.2, labels[i], 
                ha='center', va='center', fontsize=12, 
                color='#333333', fontweight='bold'
            )
            
            # Make sure the subplot background is visible and consistent
            ax.set_aspect('equal')
            ax.axis('off')
        
        except Exception as e:
            logger.error(f"Error generating chart for {labels[i]} dosha: {e}")
            raise e

    # Adjust the layout to avoid overlap
    plt.tight_layout()

    # Generate a unique filename to handle concurrency
    unique_id = uuid.uuid4().hex
    chart_filename = f'dosha_circular_chart_{unique_id}.png'
    temp_dir = tempfile.gettempdir()
    chart_path = os.path.join(temp_dir, chart_filename)

    try:
        # Save the figure with a transparent background to preserve the overall figure's color
        plt.savefig(chart_path, transparent=False, dpi=300)  # transparent=False ensures the background is saved
        logger.info(f"Circular dosha chart saved at '{chart_path}'.")
    except Exception as e:
        logger.error(f"Failed to save circular dosha chart: {e}")
        raise e
    finally:
        plt.close()

    return chart_path
