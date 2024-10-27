import pathlib
import random
import matplotlib.pyplot as plt
from math import ceil
import seaborn as sns


def read_class_list(filename: str) -> list[str]:
    """Reads a class list from a file and returns a list of names

    Args:
        filename (str): Filename of class list

    Returns:
        list[str]: List of names

    """
    class_list = []
    with open(filename) as f:
        for line in f:
            class_list.append(line.strip())
    return class_list


def remove_names(class_list: list[str], names: list[str]) -> list[str]:
    """Removes names from a class list

    Args:
        class_list (list[str]): List of names
        names (list[str]): Names to remove from class list

    Returns:
        list[str]: List of names with names removed
    """
    for name in names:
        try:
            class_list.remove(name)
        except:
            raise ValueError(f"{name} er ikke i klasselisten.")
    return class_list


def generate_random_groups(class_list: list[str], group_size: int) -> list[list[str]]:
    """Generates random groups from a class list


    Args:
        class_list (list[str]): List of names
        group_size (int): Size of each group

    Returns:
        list[list[str]]: List of groups

    """

    random.shuffle(class_list)
    num_groups = len(class_list) // group_size

    # Hvis det er flere elever enn det er plass til i gruppene
    if len(class_list) % group_size != 0:
        num_groups += 1

    # Deler ut elever som en kortstokk
    groups = [[] for _ in range(num_groups)]
    while len(class_list) > 0:
        for group in groups:
            if len(class_list) > 0:
                group.append(class_list.pop())
            else:
                break
    return groups


def create(classlist, remove_names: list = None, group_size: int = None):
    class_list = read_class_list(filename=classlist)
    if remove_names is not None:
        class_list = remove_names(remove_names)

    if group_size is not None:
        groups = generate_random_groups(class_list, group_size)
    else:
        groups = generate_random_groups(class_list, len(class_list) // num_groups)

    fig, ax = visualize_groups(groups)
    return fig, ax


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


def savefig(dirname, fname):
    dir = pathlib.Path(dirname)
    dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{dir}/{fname}")

    return None


def show():
    plt.show()
