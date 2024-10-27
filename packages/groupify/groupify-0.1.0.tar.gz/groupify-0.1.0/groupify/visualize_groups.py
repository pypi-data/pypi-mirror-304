import matplotlib.pyplot as plt
from math import ceil
import seaborn as sns


def visualize_groups(groups: list[list[str]]) -> None:
    # Define the size of the figure
    fig, ax = plt.subplots(figsize=(14, 8))

    # Define the number of rows and columns based on group number
    n_rows = ceil(len(groups) / 2)
    n_cols = 2

    # Define the size of each cell based on number of rows and columns
    cell_size_x = 1.0 / n_cols
    cell_size_y = 1.0 / n_rows

    # Get a color palette
    colors = sns.color_palette("hls", len(groups))
    # colors = sns.color_palette("husl", len(groups))

    # Loop through each group
    for i, group in enumerate(groups):
        # Calculate the row and column number
        row = i // n_cols
        col = i % n_cols

        # Calculate the position of the bottom-left corner of the rectangle
        bottom_left_x = col * cell_size_x
        bottom_left_y = (n_rows - 1 - row) * cell_size_y

        # Create the rectangle
        rectangle = plt.Rectangle(
            (bottom_left_x, bottom_left_y),
            cell_size_x,
            cell_size_y,
            fill=True,
            color=colors[i],
            edgecolor="black",
            lw=2,
            alpha=0.3,
        )
        ax.add_patch(rectangle)

        # Calculate the center position of the rectangle
        center_x = bottom_left_x + cell_size_x / 2
        center_y = bottom_left_y + cell_size_y / 2

        # Add the group number to the center of the rectangle
        ax.text(
            center_x,
            center_y,
            f"{i+1}",
            ha="center",
            va="center",
            fontsize=20,
            bbox=dict(facecolor="white", alpha=0.5),
        )

        # Positions of names in the sub-rectangles of the rectangle
        positions = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]

        # Add the individuals to the rectangle
        for j, individual in enumerate(group):
            pos_x = positions[j][0] * cell_size_x + bottom_left_x
            pos_y = positions[j][1] * cell_size_y + bottom_left_y
            ax.text(
                pos_x,
                pos_y,
                individual,
                ha="center",
                va="center",
                fontsize=20,
                bbox=dict(facecolor="white", alpha=0.5),
            )

    # Remove the axis
    ax.axis("off")
    group_size = max([len(group) for group in groups])
    plt.title(f"{group_size}-grupper", fontsize=25, weight="bold")

    return fig, ax
