import json
import matplotlib.pyplot as plt
import textwrap
from matplotlib.patches import FancyBboxPatch

# List of JSON filenames to process
json_filenames = ["IT-SAP.json", "Cybersecurity-SAP.json", "CRIMJ-SAP.json"]

# Create a dictionary to map course types to colors
color_mapping = {
    "Core": "#AED6F1",  # Pastel blue
    "Gen Ed": "#FADBD8",  # Pastel pink
    "Major & Gen Ed": "#D7BDE2",  # Pastel purple
    "Elective": "#F9E79F"  # Pastel yellow
}

# Define the number of columns and the number of classes per column
num_columns = 4

# Function to create a year column with an organized layout
def create_year_column(ax, year_data, year_label, x_position, column_width, square_width, square_height, spacing):
    y = 4.5

    # Add the year title
    ax.text(x_position + (column_width / 2), 5.5, year_label, ha="center", fontsize=14, fontweight="bold", fontname="Century Gothic")

    # Add a horizontal line under the title
    ax.axhline(5.3, color="black", linewidth=1)

    # Create two vertical columns of boxes with increased spacing
    for i, course_info in enumerate(year_data):
        if i == 5:  # Start the second vertical column
            x_position += square_width + spacing
            y = 4.5
        course_label = course_info["course"]
        credits = course_info["credits"]
        course_type = course_info["type"]
        color = color_mapping.get(course_type, "gray")

        # Add margins to the box to center the text
        margin = 0.1
        rounded_box = FancyBboxPatch(
            (x_position + margin, y - 0.35 + margin),
            square_width - 2 * margin,
            square_height - 2 * margin,
            boxstyle="round, pad=0.05",
            edgecolor="black",
            facecolor=color,
            label=course_type,
        )
        ax.add_patch(rounded_box)

        # Adjust text size and position to center it and wrap text
        wrapped_text = textwrap.fill(f"{course_label}\n{credits} credits", width=15)
        ax.text(x_position + square_width / 2, y - 0.01, wrapped_text, ha="center", va="center", color="black",
                fontsize=8, fontname='Century Gothic')

        y -= square_height + spacing

# Iterate over each JSON filename and create a separate plot
for json_filename in json_filenames:
    # Load the JSON data
    with open(json_filename, "r") as json_file:
        data = json.load(json_file)

    # Create the academic plan graphic for all four years
    fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the figure size here

    # Create columns, lines, and labels
    x_position = 0.0

    # Increase the linewidth for column borders
    column_border_linewidth = 1

    academic_years = ["1st year", "2nd year", "3rd year", "4th year"]
    column_width = 7.0  # Adjusted total width for 4 columns
    square_width = column_width / 2.2  # Adjusted for 2 vertical columns of 5 boxes each
    square_height = 0.8
    spacing = (column_width - (square_width * 1)) / 9  # Increased spacing

    for i in range(num_columns):
        create_year_column(ax, data["SAP"][i][academic_years[i]], academic_years[i], x_position, column_width, square_width, square_height, spacing)
        ax.axvline(x_position + column_width, color="black", linewidth=column_border_linewidth)
        x_position += column_width

    # Set axis limits and labels
    ax.set_xlim(0, column_width * num_columns)
    ax.set_ylim(0, 6)

    # Remove x and y axis labels and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Create a legend with distinct course type colors
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', label='Core', markerfacecolor=color_mapping['Core'], markersize=15),
        plt.Line2D([0], [0], marker='s', color='w', label='Gen Ed', markerfacecolor=color_mapping['Gen Ed'], markersize=15),
        plt.Line2D([0], [0], marker='s', color='w', label='Major & Gen Ed', markerfacecolor=color_mapping['Major & Gen Ed'], markersize=15),
        plt.Line2D([0], [0], marker='s', color='w', label='Elective', markerfacecolor=color_mapping['Elective'], markersize=15),
    ]

    # Adjust the position and layout of the legend
    ax.legend(handles=legend_elements, loc="upper center", title="Course Type", bbox_to_anchor=(0.51, 0.0), ncol=4)

    # Set the plot title
    plt.title(f"Suggested Academic Plan for {data['Program of Study']}")

    # Display the plot
    plt.show()
