import matplotlib.pyplot as plt
from reportlab.platypus import Image as ReportImage, PageBreak, Paragraph, Spacer
import os
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend suitable for script-based plotting

def create_line_graphs(vatta_data, pitta_data, kapha_data, output_path_combined, output_path_vatta, output_path_pitta, output_path_kapha):
    """Generate graphs for Vatta, Pitta, and Kapha, and save them as images."""
    
    # Create figure for the combined dosha graph
    fig, ax = plt.subplots(1, 1, figsize=(8, 4), dpi=100)
    
    # Plot each dosha signal on the same graph
    ax.plot(vatta_data, color=(75/255, 74/255, 160/255), linewidth=2, label='Vatta')
    ax.plot(pitta_data, color=(212/255, 94/255, 47/255), linewidth=2, label='Pitta')
    ax.plot(kapha_data, color=(62/255, 163/255, 65/255), linewidth=2, label='Kapha')

    # Add titles and labels for the combined graph
    ax.set_title('Combined Dosha Signal Data')
    ax.set_yticklabels([])  # Hide y-axis labels

    # Remove the x and y axis lines (top, right, left, and bottom spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Add only the center line (zero) on the horizontal axis
    ax.axhline(0, color='gray', linestyle='--')

    # Set a light grey background
    ax.set_facecolor((0.95, 0.95, 0.95))  # Light grey background

    ax.set_yticks([])  # This removes both the tick marks and the labels

    # Disable the full grid
    ax.grid(False)

    # Add a legend to differentiate between the signals
    ax.legend()

    # Save the combined graph as an image
    plt.tight_layout()
    plt.savefig(output_path_combined, format='png')
    plt.close()

    # Create individual graphs for each dosha
    def plot_individual_graph(data, color, label, output_path):
        fig, ax = plt.subplots(1, 1, figsize=(8, 4), dpi=100)
        ax.plot(data, color=color, linewidth=2, label=label)
        # ax.set_title(f'{label} Signal Data')

        # Remove the x and y axis lines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Add only the center line (zero) on the horizontal axis
        ax.axhline(0, color='gray', linestyle='--')

        # Set a light grey background
        ax.set_facecolor((0.95, 0.95, 0.95))  # Light grey background

        ax.set_yticks([])  # This removes both the tick marks and the labels

        # Disable the full grid
        ax.grid(False)

        # Add a legend to differentiate between the signals
        ax.legend()

        # Save the graph as an image
        plt.tight_layout()
        plt.savefig(output_path, format='png')
        plt.close()

    # Plot individual graphs for Vatta, Pitta, and Kapha
    plot_individual_graph(vatta_data, (75/255, 74/255, 160/255), 'Vatta', output_path_vatta)
    plot_individual_graph(pitta_data, (212/255, 94/255, 47/255), 'Pitta', output_path_pitta)
    plot_individual_graph(kapha_data, (62/255, 163/255, 65/255), 'Kapha', output_path_kapha)


def add_graphs_to_pdf(elements, output_path_vatta, output_path_pitta, output_path_kapha, output_path_combined, styles, doc):
    """Add graphs to the PDF, individual doshas on one page, combined on the next."""


    # Add the dosha graphs (Vatta, Pitta, Kapha) to a single page
    elements.append(Paragraph("Dosha Graphs", styles.get_style('CustomTitle')))

    # Reduce height so all graphs fit on the same page
    image_height = doc.width * 0.4  # Adjust the height to fit all three graphs on the same page

    # Add Vatta graph
    if os.path.exists(output_path_vatta):
        graph_image = ReportImage(output_path_vatta, width=doc.width, height=image_height)
        elements.append(graph_image)
        elements.append(Spacer(1, 12))

    # Add Pitta graph
    if os.path.exists(output_path_pitta):
        graph_image = ReportImage(output_path_pitta, width=doc.width, height=image_height)
        elements.append(graph_image)
        elements.append(Spacer(1, 12))

    # Add Kapha graph
    if os.path.exists(output_path_kapha):
        graph_image = ReportImage(output_path_kapha, width=doc.width, height=image_height)
        elements.append(graph_image)
        elements.append(Spacer(1, 12))

    # Add combined graph on the next page
    # elements.append(PageBreak())
    if os.path.exists(output_path_combined):
        # elements.append(Paragraph("Combined Dosha Graph", styles.get_style('CustomSubtitle')))
        graph_image = ReportImage(output_path_combined, width=doc.width, height=image_height)
        elements.append(graph_image)
        elements.append(Spacer(1, 12))
    
        elements.append(Spacer(1, 12))
    elements.append(Paragraph("Graph Explanation:", styles.get_style('CustomSubtitle')))
    elements.append(Paragraph(
        "The graphs above represent the spectrum amplitude of each dosha. Higher peaks indicate higher activity levels in that particular dosha. Monitoring these can help in balancing your doshas.",
        styles.get_style('CustomNormal')
    ))

