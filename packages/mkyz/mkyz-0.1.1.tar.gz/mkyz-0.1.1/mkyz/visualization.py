# mkyz/visualization.py dosyası içeriği

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import warnings
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pandas.plotting import parallel_coordinates
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import matplotlib.patches as mpatches
from itertools import combinations

import plotly.graph_objects as go
from scipy.interpolate import griddata

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set default Matplotlib style with a dark background
plt.style.use('dark_background')

# Default color palette with at least 20 colors
DEFAULT_PALETTE = sns.color_palette("tab20", 20)

# Function to dynamically select a palette based on the number of columns
def get_dynamic_palette(palette, num_cols):
    if num_cols <= len(palette):
        return palette[:num_cols]
    else:
        # If more colors are needed, extend the palette by repeating it
        repeat_factor = math.ceil(num_cols / len(palette))
        extended_palette = palette * repeat_factor
        return extended_palette[:num_cols]

# Helper function to create grid layouts, potentially across multiple figures
def create_grids(num_plots, cols=3, per_subplot_size=(15, 15), max_plots_per_fig=12):
    """
    Splits the total number of plots into multiple grids if necessary.

    Args:
        num_plots (int): Total number of plots to create.
        cols (int): Number of columns per grid.
        per_subplot_size (tuple): Size of each subplot (width, height).
        max_plots_per_fig (int): Maximum number of subplots per figure.

    Returns:
        list of tuples: Each tuple contains (fig, axes) for a grid.
    """
    grids = []
    plots_remaining = num_plots
    while plots_remaining > 0:
        current_plots = min(plots_remaining, max_plots_per_fig)
        rows = math.ceil(current_plots / cols)
        total_fig_width = cols * per_subplot_size[0]
        total_fig_height = rows * per_subplot_size[1]
        fig, axes = plt.subplots(rows, cols, figsize=(total_fig_width, total_fig_height))
        if rows == 1 and cols == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        grids.append((fig, axes[:current_plots]))
        plots_remaining -= current_plots
    return grids

# 1. Histogram - Continuous data
def histogram_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.histplot(data=data, x=column, hue=target, fill=True, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'Histogram - {column}', color='white')
            ax.tick_params(colors='white')
        plt.tight_layout()
        plt.show()

# 2. Bar Plot - Categorical data
def plot_bar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            sns.countplot(data=data, x=column, hue=target, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'Bar Plot - {column}', color='white')
            ax.tick_params(colors='white')
        plt.tight_layout()
        plt.show()

# 3. Box Plot - Continuous data
def plot_box_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.boxplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'Box Plot - {column}', color='white')
            ax.tick_params(colors='white')
        plt.tight_layout()
        plt.show()

# 4. [Add any additional plotting functions here, following the same pattern]

# 5. Violin Plot - Continuous data
def plot_violin_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.violinplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=ax, legend=False)
            ax.set_title(f'Violin Plot - {column}', color='white')
            ax.tick_params(colors='white')
        plt.tight_layout()
        plt.show()

# 6. Pie Chart - Categorical data
def plot_pie_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            counts = data[column].value_counts()
            ax.pie(counts, labels=counts.index, colors=get_dynamic_palette(palette, len(counts)),
                   autopct='%1.1f%%', startangle=140)
            ax.set_title(f'Pie Chart - {column}', color='white')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        plt.show()

# 7. Scatter Plot - Continuous data
def plot_scatter_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for scatter plot.")

    # Plot scatter for every pair of continuous columns
    pairs = list(combinations(numerical_columns, 2))
    num_plots = len(pairs)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(pairs):
                ax.set_visible(False)
                continue
            x_col, y_col = pairs[i]
            sns.scatterplot(data=data, x=x_col, y=y_col, hue=target, palette=palette, ax=ax)
            ax.set_title(f'Scatter Plot - {x_col} vs {y_col}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 8. Line Plot - Continuous data
def plot_line_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.lineplot(data=data, x=data.index, y=column, label=column, ax=ax)
            ax.set_title(f'Line Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 9. Heatmap - Correlation Matrix
def plot_correlation_matrix(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    plt.figure(figsize=figsize)
    corr = data[numerical_columns].corr()

    # Using cubehelix_palette for color mapping
    cubehelix_palette_map = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)

    sns.heatmap(corr, annot=True, cmap=cubehelix_palette_map, linewidths=0.5)
    plt.title("Correlation Matrix", color='white')
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    plt.show()

# 10. Pair Plot - Continuous data
def plot_pair_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    sns.pairplot(data[numerical_columns + [target]], hue=target, palette=palette)
    plt.suptitle("Pair Plot", y=1.02, color='white')
    plt.show()

# 11. Swarm Plot - Categorical data
def plot_swarm_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Swarm Plot.")
    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            sns.swarmplot(data=data, x=column, y=continuous_cols[0], hue=target, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'Swarm Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 12. Strip Plot - Categorical data
def plot_strip_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Strip Plot.")
    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            sns.stripplot(data=data, x=column, y=continuous_cols[0], hue=target, palette=[dynamic_palette[i]], ax=ax, jitter=True)
            ax.set_title(f'Strip Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 13. KDE Plot - Continuous data 
def plot_kde_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.kdeplot(data=data, x=column, hue=target, fill=True, common_norm=False, alpha=0.5, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'KDE Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 14. Ridge Plot - Continuous data
def plot_ridge_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Ridge Plot.")

    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    unique_targets = data[target].unique()
    n_targets = len(unique_targets)
    dynamic_palette = get_dynamic_palette(palette, n_targets)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.kdeplot(data=data, x=column, hue=target, fill=True, common_norm=False, alpha=0.5, palette=dynamic_palette, ax=ax)
            ax.set_title(f'Ridge Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 15. Density Plot - Continuous data
def plot_density_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.kdeplot(data=data, x=column, hue=target, fill=True, palette=palette, label=column)

    plt.title("Density Plot", color='white')
    plt.legend()
    plt.show()

# 16. Joint Plot - Continuous data
def plot_joint_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for joint plot.")

    # Plot jointplot for every pair of continuous columns
    pairs = list(combinations(numerical_columns, 2))
    num_plots = len(pairs)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(pairs):
                ax.set_visible(False)
                continue
            x_col, y_col = pairs[i]
            g = sns.jointplot(data=data, x=x_col, y=y_col, hue=target, palette=palette, kind='scatter')
            g.fig.suptitle(f'Joint Plot - {x_col} vs {y_col}', y=1.02, color='white')
            g.fig.tight_layout()
            g.fig.subplots_adjust(top=0.95)
    plt.show()

# 17. Facet Grid - Categorical data
def plot_facet_grid_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    if len(categorical_columns) == 0 or len(numerical_columns) == 0:
        raise ValueError("Insufficient categorical or continuous columns for Facet Grid.")

    for column in categorical_columns:
        g = sns.FacetGrid(data, col=column, hue=target, palette=palette, height=5, aspect=1)
        g.map(sns.histplot, numerical_columns[0], kde=True)
        g.add_legend()
        plt.subplots_adjust(top=0.9)
        g.fig.suptitle(f'Facet Grid - {column}', color='white')
        plt.show()

# 18. Regression Plot - Continuous data
def plot_regression_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for regression plot.")

    # Plot regression for every pair of continuous columns
    pairs = list(combinations(numerical_columns, 2))
    num_plots = len(pairs)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            if i >= len(pairs):
                ax.set_visible(False)
                continue
            x_col, y_col = pairs[i]
            sns.regplot(data=data, x=x_col, y=y_col, scatter_kws={'alpha':0.5}, line_kws={'color': 'red'}, ax=ax)
            ax.set_title(f'Regression Plot - {x_col} vs {y_col}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 19. Dendrogram - Categorical data
def plot_dendrogram_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for dendrogram.")

    # Encode categorical variables
    encoded_data = pd.get_dummies(data[categorical_cols])
    linked = linkage(encoded_data, 'single')

    plt.figure(figsize=figsize)
    dendrogram(linked, labels=data[target].values, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Dendrogram', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.show()

# 20. Donut Chart - Categorical data
def plot_donut_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= num_plots:
                ax.set_visible(False)
                continue
            column = categorical_cols[i]
            counts = data[column].value_counts()
            wedges, texts, autotexts = ax.pie(counts, labels=counts.index, colors=get_dynamic_palette(palette, len(counts)),
                                              autopct='%1.1f%%', startangle=140, pctdistance=0.85)
            # Draw circle
            centre_circle = plt.Circle((0,0),0.70,fc='black')
            ax.add_artist(centre_circle)
            ax.set_title(f'Donut Chart - {column}', color='white')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.show()

# 21. Bubble Plot - Continuous data
def plot_bubble_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for bubble plot.")

    # Plot bubble plot for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))
    num_plots = len(triplets)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(triplets):
                ax.set_visible(False)
                continue
            x_col, y_col, size_col = triplets[i]
            sns.scatterplot(data=data, x=x_col, y=y_col, size=size_col, hue=target, palette=palette, sizes=(20, 200), alpha=0.6, ax=ax)
            ax.set_title(f'Bubble Plot - {x_col} vs {y_col} sized by {size_col}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 22. Sunburst Chart - Categorical data
def plot_sunburst_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Plotly is required for Sunburst Chart. Please install it using pip install plotly.")

    categorical_cols = categorical_columns
    if len(categorical_cols) < 2:
        raise ValueError("Need at least two categorical columns for Sunburst Chart.")

    # Create combinations for sunburst paths
    paths = list(combinations(categorical_cols, 2))

    for path in paths:
        fig = px.sunburst(data, path=path, color=target, color_discrete_sequence=palette,
                          title=f'Sunburst Chart - {" & ".join(path)}')
        fig.update_layout(title_font_color='white')
        fig.show()

# 23. Interactive 3D Scatter Plot - Continuous data using Plotly
def plot_3d_scatter_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for 3D scatter plot.")

    # Plot 3D scatter for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))
    num_plots = len(triplets)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(triplets):
                ax.set_visible(False)
                continue
            x_col, y_col, z_col = triplets[i]
            fig_plot = px.scatter_3d(
                data_frame=data,
                x=x_col,
                y=y_col,
                z=z_col,
                color=target,
                color_discrete_sequence=palette,
                title=f'3D Scatter Plot - {x_col} vs {y_col} vs {z_col}',
                labels={
                    x_col: x_col,
                    y_col: y_col,
                    z_col: z_col,
                    target: target
                },
                opacity=0.7
            )
            fig_plot.update_layout(
                title=dict(
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top',
                    font=dict(color='white')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            fig_plot.show()

# 24. Parallel Coordinates - Continuous data
def plot_parallel_coordinates_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if target not in continuous_cols:
        # Assuming target is categorical or already included
        pass
    plt.figure(figsize=figsize)
    parallel_coordinates(data[numerical_columns + [target]], target, color=get_dynamic_palette(palette, len(data[target].unique())))
    plt.title('Parallel Coordinates Plot', color='white')
    plt.show()

# 25. Radar Chart - Categorical data
def plot_radar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    import matplotlib.colors as mcolors
    from matplotlib import cm
    import numpy as np

    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Radar Chart.")

    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    dynamic_palette = get_dynamic_palette(palette, len(categorical_cols))

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(categorical_cols):
                ax.set_visible(False)
                continue
            column = categorical_cols[i]
            counts = data[column].value_counts()
            categories = list(counts.index)
            values = counts.values
            N = len(categories)

            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            values = np.concatenate((values, [values[0]]))
            angles += angles[:1]

            ax.plot(angles, values, color=dynamic_palette[i], linewidth=2)
            ax.fill(angles, values, color=dynamic_palette[i], alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), categories)
            ax.set_title(f'Radar Chart - {column}', color='white')
            ax.tick_params(colors='white')
            ax.grid(color='white')

    plt.tight_layout()
    plt.show()

# 26. Waterfall Chart - Categorical data
def plot_waterfall_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Waterfall Chart.")

    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            counts = data[column].value_counts().sort_index()
            cumulative = counts.cumsum()
            ax.bar(counts.index, counts.values, color=get_dynamic_palette(palette, len(counts)))
            ax.plot(cumulative, color='cyan', marker='o')
            ax.set_title(f'Waterfall Chart - {column}', color='white')
            ax.set_xlabel(column)
            ax.set_ylabel('Count')
            ax.tick_params(colors='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
    plt.tight_layout()
    plt.show()

# 27. Area Plot - Continuous data
def plot_area_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.kdeplot(data=data, x=column, fill=True, label=column, alpha=0.5)

    plt.title('Area Plot - Continuous Variables', color='white')
    plt.legend()
    plt.show()

# 28. Step Plot - Continuous data
def plot_step_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.lineplot(data=data, x=data.index, y=column, drawstyle='steps', label=column)

    plt.title('Step Plot - Continuous Variables', color='white')
    plt.legend()
    plt.show()

# 29. Trellis Plot - Categorical data
def plot_trellis_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(categorical_cols) == 0 or len(continuous_cols) == 0:
        raise ValueError("Insufficient categorical or continuous columns for Trellis Plot.")

    for column in categorical_cols:
        g = sns.FacetGrid(data, col=column, hue=target, palette=palette, height=5, aspect=1)
        g.map(sns.histplot, continuous_cols[0], kde=True)
        g.add_legend()
        plt.subplots_adjust(top=0.9)
        g.fig.suptitle(f'Trellis Plot - {column}', color='white')
        plt.show()

# 30. Lollipop Chart - Categorical data
def plot_lollipop_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Lollipop Chart.")

    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            counts = data[column].value_counts()
            ax.stem(counts.index, counts.values, linefmt='C0-', markerfmt='C0o', basefmt=" ", use_line_collection=True)
            ax.set_title(f'Lollipop Chart - {column}', color='white')
            ax.set_xlabel(column)
            ax.set_ylabel('Count')
            ax.tick_params(colors='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
    plt.tight_layout()
    plt.show()

# 31. PCA Visualization - Continuous data
def plot_pca_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, n_components=2, max_plots_per_fig=20):
    # n_components neden 2 olmalı = 2D grafik oluşturmak için
    continuous_cols = numerical_columns
    if len(continuous_cols) < n_components:
        raise ValueError(f"Need at least {n_components} continuous columns for PCA.")

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(data[continuous_cols])
    pca_df = pd.DataFrame(data=components, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df[target] = data[target]

    plt.figure(figsize=figsize)
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue=target, palette=palette)
    plt.title('PCA Visualization', color='white')
    plt.legend()
    plt.show()

# 32. TSNE Visualization - Continuous data
def plot_tsne_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, n_components=2, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for t-SNE.")

    tsne = TSNE(n_components=n_components, random_state=42)
    components = tsne.fit_transform(data[continuous_cols])
    tsne_df = pd.DataFrame(data=components, columns=[f'Dim{i+1}' for i in range(n_components)])
    tsne_df[target] = data[target]

    plt.figure(figsize=figsize)
    sns.scatterplot(data=tsne_df, x='Dim1', y='Dim2', hue=target, palette=palette)
    plt.title('t-SNE Visualization', color='white')
    plt.legend()
    plt.show()

# 33. Mosaic Plot - Categorical data
def plot_mosaic_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    try:
        from statsmodels.graphics.mosaicplot import mosaic
    except ImportError:
        raise ImportError("Statsmodels is required for Mosaic Plot. Please install it using pip install statsmodels.")

    categorical_cols = categorical_columns
    if len(categorical_cols) < 2:
        raise ValueError("Need at least two categorical columns for Mosaic Plot.")

    num_plots = len(categorical_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        dynamic_palette = get_dynamic_palette(palette, len(axes))
        for i, ax in enumerate(axes):
            column = categorical_cols[i]
            plt.sca(ax)
            mosaic(data, [column, target], title=f'Mosaic Plot - {column} vs {target}', facecolor=lambda x: palette[x[1] % len(palette)])
            ax.set_title(f'Mosaic Plot - {column} vs {target}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 34. Boxen Plot - Continuous data 
def plot_boxen_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            column = continuous_cols[i]
            sns.boxenplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=ax)
            ax.set_title(f'Boxen Plot - {column}', color='white')
            ax.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

# 35. Stacked Bar Plot - Categorical data
def plot_stacked_bar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    categorical_cols = categorical_columns
    for column in categorical_cols:
        counts = pd.crosstab(data[column], data[target])
        counts.plot(kind='bar', stacked=True, color=get_dynamic_palette(palette, counts.shape[1]))
        plt.title(f'Stacked Bar Plot - {column}', color='white')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.legend(title=target)
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.show()

# 36. Funnel Chart - Categorical data
def plot_funnel_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Plotly is required for Funnel Chart. Please install it using pip install plotly.")

    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Funnel Chart.")

    for column in categorical_cols:
        counts = data[column].value_counts().reset_index()
        counts.columns = [column, 'count']
        fig = px.funnel(counts, x='count', y=column, title=f'Funnel Chart - {column}', color_discrete_sequence=palette)
        fig.show()

# 37. Hexbin Plot - Continuous data
def plot_hexbin_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 2:
        raise ValueError("Need at least two continuous columns for Hexbin Plot.")

    # Plot hexbin for every pair of continuous columns
    pairs = list(combinations(continuous_cols, 2))
    num_plots = len(pairs)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(pairs):
                ax.set_visible(False)
                continue
            x_col, y_col = pairs[i]
            hb = ax.hexbin(data[x_col], data[y_col], gridsize=30, cmap='viridis')
            ax.set_xlabel(x_col, color='white')
            ax.set_ylabel(y_col, color='white')
            ax.set_title(f'Hexbin Plot - {x_col} vs {y_col}', color='white')
            ax.tick_params(colors='white')
            fig.colorbar(hb, ax=ax, label='count in bin')
    plt.tight_layout()
    plt.show()

# 39. Interactive 3D Surface Plot - Continuous data using Plotly
def plot_3d_surface_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE, max_plots_per_fig=20):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for 3D surface plot.")

    # Plot 3D surface for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))
    num_plots = len(triplets)
    grids = create_grids(num_plots, cols, per_subplot_size=(5, 5), max_plots_per_fig=max_plots_per_fig)

    for fig, axes in grids:
        for i, ax in enumerate(axes):
            if i >= len(triplets):
                ax.set_visible(False)
                continue
            x_col, y_col, z_col = triplets[i]
            x = data[x_col]
            y = data[y_col]
            z = data[z_col]

            # Create grid values first.
            xi = np.linspace(x.min(), x.max(), 100)
            yi = np.linspace(y.min(), y.max(), 100)
            xi, yi = np.meshgrid(xi, yi)

            # Interpolate
            zi = griddata((x, y), z, (xi, yi), method='linear')

            # Create the surface plot
            fig_plot = go.Figure(data=[go.Surface(x=xi, y=yi, z=zi, colorscale='Viridis')])

            fig_plot.update_layout(
                title=f'3D Surface Plot - {x_col} vs {y_col} vs {z_col}',
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col,
                    xaxis=dict(color='white'),
                    yaxis=dict(color='white'),
                    zaxis=dict(color='white')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            fig_plot.show()

# 40. Additional Plots can be added here following the same pattern

# General visualize function
def visualize(
        data,
        graphics='kde',
        cols=3,
        figsize=(15, 15),
        palette=DEFAULT_PALETTE,
        max_plots_per_fig=20  # New parameter to limit plots per figure
):
    """
    Veriyi belirtilen grafik türüne göre görselleştirir.

    Args:
        data (tuple or pandas.DataFrame): Eğer tuple ise (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns) içermeli.
                                         Eğer DataFrame ise, gerekli sütunların mevcut olduğundan emin olunmalı.
        graphics (str): Oluşturulacak grafik türü (örn., 'scatter', 'bar', 'heatmap', 'corr').
        cols (int, optional): Her subplot grid'inde olacak sütun sayısı.
        figsize (tuple, optional): Her figürün boyutu.
        palette (list, optional): Plotlar için renk paleti.
        max_plots_per_fig (int, optional): Her figürde maksimum subplot sayısı.

    Returns:
        None: Grafikleri görüntüler.
    """
    if data is None:
        raise ValueError("Veri sağlanmalıdır.")

    # Eğer data tuple ise, gerekli bileşenleri ayrıştırın
    if isinstance(data, tuple):
        if len(data) < 8:
            raise ValueError("Data tuple'ı en az 8 eleman içermelidir: (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns).")
        df, target_column, numerical_columns, categorical_columns = data[4], data[5], data[6], data[7]
    elif isinstance(data, pd.DataFrame):
        # DataFrame doğrudan sağlanmışsa, hedef ve feature sütunlarını ayrıca belirtmelisiniz
        raise NotImplementedError("DataFrame doğrudan sağlanmışsa, lütfen target_column, numerical_columns ve categorical_columns parametrelerini ayrı olarak geçin.")
    else:
        raise TypeError("Data, pandas DataFrame veya (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns) içeren bir tuple olmalıdır.")

    graphics = graphics.lower()

    # Grafik fonksiyonlarını tanımlayın veya ithal edin
    graphics_dict = {
        'corr': plot_correlation_matrix,

        # Sürekli görselleştirmeler
        'histogram': histogram_continuous,
        'box': plot_box_continuous,
        'scatter': plot_scatter_continuous,
        'line': plot_line_continuous,
        'kde': plot_kde_continuous,
        'pair': plot_pair_continuous,
        'violin': plot_violin_continuous,
        'ridge': plot_ridge_continuous,
        'area': plot_area_continuous,
        'step': plot_step_continuous,
        'density': plot_density_continuous,
        'bubble': plot_bubble_continuous,
        '3dscatter': plot_3d_scatter_continuous,
        'parallel': plot_parallel_coordinates_continuous,
        'hexbin': plot_hexbin_continuous,
        'boxen': plot_boxen_continuous,
        '3dsurface': plot_3d_surface_continuous,
        'pca': plot_pca_continuous,
        'tsne': plot_tsne_continuous,
        'regression': plot_regression_continuous,
        'joint': plot_joint_continuous,

        # Kategorik görselleştirmeler
        'bar': plot_bar_categorical,
        'pie': plot_pie_categorical,
        'swarm': plot_swarm_categorical,
        'strip': plot_strip_categorical,
        'trellis': plot_trellis_categorical,
        'lollipop': plot_lollipop_categorical,
        'mosaic': plot_mosaic_categorical,
        'donut': plot_donut_categorical,
        'sunburst': plot_sunburst_categorical,
        'radar': plot_radar_categorical,
        'waterfall': plot_waterfall_categorical,
        'funnel': plot_funnel_categorical,
        'stackedbar': plot_stacked_bar_categorical,
        'dendrogram': plot_dendrogram_categorical,
        'facetgrid': plot_facet_grid_categorical,
    }

    if graphics not in graphics_dict:
        raise ValueError(f"Geçersiz grafik türü. Aşağıdakilerden birini seçin: {', '.join(graphics_dict.keys())}")

    graphics_func = graphics_dict[graphics]

    # Grafik fonksiyonunu çağırın with the new max_plots_per_fig parameter
    graphics_func(
        data=df,
        target=target_column,
        numerical_columns=numerical_columns,
        categorical_columns=categorical_columns,
        cols=cols,
        figsize=figsize,
        palette=palette,
        max_plots_per_fig=max_plots_per_fig
    )

def visualize(
        data,
        graphics='kde',
        cols=3,
        figsize=(15, 15),
        palette=DEFAULT_PALETTE,
        max_plots_per_fig=20
):
    """
    Visualizes data using the specified type of graphics.

    This function creates various types of plots for data exploration and analysis. It supports
    both continuous and categorical visualizations based on the provided `graphics` parameter.
    The function can handle data provided either as a tuple containing multiple components or
    directly as a pandas DataFrame.

    Args:
        data (tuple or pandas.DataFrame): 
            - If tuple, it should contain (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns).
            - If DataFrame, ensure that the necessary columns are provided separately.
        graphics (str): Type of graph to create (e.g., 'scatter', 'bar', 'heatmap', 'corr'). Defaults to 'kde'.
        cols (int, optional): Number of columns in each subplot grid. Defaults to 3.
        figsize (tuple, optional): Size of each figure. Defaults to (15, 15).
        palette (list, optional): Color palette for the plots. Defaults to DEFAULT_PALETTE.
        max_plots_per_fig (int, optional): Maximum number of subplots per figure. Defaults to 20.

    Returns:
        None: Displays the generated plots.

    Raises:
        ValueError: 
            - If the `data` tuple does not contain at least 8 elements.
            - If an invalid `graphics` type is specified.
        TypeError:
            - If `data` is not a pandas DataFrame or the required tuple.
        NotImplementedError:
            - If `data` is a DataFrame, as this case is not implemented.

    Examples:
        >>> # Example 1: Visualize using KDE plots
        >>> visualize(data, graphics='kde', cols=4, figsize=(20, 20))
        
        >>> # Example 2: Visualize using correlation heatmap
        >>> visualize(data, graphics='corr')
        
        >>> # Example 3: Visualize categorical data using bar plots
        >>> visualize(data, graphics='bar', palette=['#1f77b4', '#ff7f0e', '#2ca02c'])
    """
    try:
        if data is None:
            raise ValueError("Data must be provided.")

        # If data is a tuple, unpack the necessary components
        if isinstance(data, tuple):
            if len(data) < 8:
                raise ValueError("Data tuple must contain at least 8 elements: (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns).")
            df, target_column, numerical_columns, categorical_columns = data[4], data[5], data[6], data[7]
        elif isinstance(data, pd.DataFrame):
            # If DataFrame is provided directly, target and feature columns must be specified separately
            raise NotImplementedError("If a DataFrame is provided directly, please pass target_column, numerical_columns, and categorical_columns as separate parameters.")
        else:
            raise TypeError("Data must be a pandas DataFrame or a tuple containing (X_train, X_test, y_train, y_test, df, target_column, numerical_columns, categorical_columns).")

        graphics = graphics.lower()

        # Define or import graphic functions
        graphics_dict = {
            'corr': plot_correlation_matrix,

            # Continuous visualizations
            'histogram': histogram_continuous,
            'box': plot_box_continuous,
            'scatter': plot_scatter_continuous,
            'line': plot_line_continuous,
            'kde': plot_kde_continuous,
            'pair': plot_pair_continuous,
            'violin': plot_violin_continuous,
            'ridge': plot_ridge_continuous,
            'area': plot_area_continuous,
            'step': plot_step_continuous,
            'density': plot_density_continuous,
            'bubble': plot_bubble_continuous,
            '3dscatter': plot_3d_scatter_continuous,
            'parallel': plot_parallel_coordinates_continuous,
            'hexbin': plot_hexbin_continuous,
            'boxen': plot_boxen_continuous,
            '3dsurface': plot_3d_surface_continuous,
            'pca': plot_pca_continuous,
            'tsne': plot_tsne_continuous,
            'regression': plot_regression_continuous,
            'joint': plot_joint_continuous,

            # Categorical visualizations
            'bar': plot_bar_categorical,
            'pie': plot_pie_categorical,
            'swarm': plot_swarm_categorical,
            'strip': plot_strip_categorical,
            'trellis': plot_trellis_categorical,
            'lollipop': plot_lollipop_categorical,
            'mosaic': plot_mosaic_categorical,
            'donut': plot_donut_categorical,
            'sunburst': plot_sunburst_categorical,
            'radar': plot_radar_categorical,
            'waterfall': plot_waterfall_categorical,
            'funnel': plot_funnel_categorical,
            'stackedbar': plot_stacked_bar_categorical,
            'dendrogram': plot_dendrogram_categorical,
            'facetgrid': plot_facet_grid_categorical,
        }

        if graphics not in graphics_dict:
            raise ValueError(f"Invalid graphics type. Choose one of: {', '.join(graphics_dict.keys())}")

        graphics_func = graphics_dict[graphics]

        # Call the graphic function with the provided parameters
        graphics_func(
            data=df,
            target=target_column,
            numerical_columns=numerical_columns,
            categorical_columns=categorical_columns,
            cols=cols,
            figsize=figsize,
            palette=palette,
            max_plots_per_fig=max_plots_per_fig
        )

    except ValueError as ve:
        print(f"ValueError caught: {ve}")
    except TypeError as te:
        print(f"TypeError caught: {te}")
    except NotImplementedError as nie:
        print(f"NotImplementedError caught: {nie}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# kullanım

if __name__ == "__main__":
   
   
    import data_processing as dp
          
    data_path = 'data.csv'
    data = dp.prepare_data(data_path)
    visualize(data, graphics='corr')
   
    #bütün grafikleri görselleştir
    graphics = ['histogram', 'box', 'scatter', 'line', 'kde',  'violin', 'ridge', 'area', 'step', 'density',
                'bubble',  'parallel', 'hexbin', 'boxen',  'pca', 'tsne', 'regression', 
                 'bar', 'pie', 'swarm', 'strip', 'trellis', 'lollipop', 'mosaic', 'donut', 'sunburst', 
                'radar', 'waterfall', 'funnel', 'stackedbar', 'dendrogram', 'facetgrid',
                'joint' ,'pair', '3dsurface','3dscatter',]
   
   
   
    for graphic in graphics:
        visualize(data, graphics=graphic)