from typing import List, Optional, Tuple, Union

import matplotlib as mpl
import numpy as np

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
import matplotlib.pyplot as plt

from ..log import debug, warning
from .data import AnaData
from .utils import saptial_figsize


def plot_cell_type_composition_dataset(ana_data: AnaData) -> Optional[Tuple[plt.Figure, plt.Axes]]:
    """
    Plot spatial distribution of cell type composition.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    try:
        if ana_data.cell_type_composition is None or ana_data.cell_type_codes is None:
            warning("No cell type composition data found.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    samples: List[str] = ana_data.cell_type_composition['sample'].unique().tolist()
    cell_types: List[str] = ana_data.cell_type_codes['Cell_Type'].tolist()

    M, N = len(samples), len(cell_types)
    fig, axes = plt.subplots(M, N, figsize=(3.5 * N, 3 * M))
    for i, sample in enumerate(samples):
        sample_df = ana_data.cell_type_composition.loc[ana_data.cell_type_composition['sample'] == sample]
        for j, cell_type in enumerate(cell_types):
            ax = axes[i, j] if M > 1 else axes[j]
            scatter = ax.scatter(sample_df['x'],
                                 sample_df['y'],
                                 c=sample_df[cell_type],
                                 cmap='Reds',
                                 vmin=0,
                                 vmax=1,
                                 s=1)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.colorbar(scatter)
            ax.set_title(f"{sample} {cell_type}")

    fig.tight_layout()
    if ana_data.options.output is not None:
        fig.savefig(f'{ana_data.options.output}/cell_type_composition.pdf', transparent=True)
        plt.close(fig)
        return None
    else:
        return fig, axes


def plot_cell_type_composition_sample(ana_data: AnaData) -> Optional[List[Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of cell type composition.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    try:
        if ana_data.cell_type_composition is None or ana_data.cell_type_codes is None:
            warning("No cell type composition data found.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    samples: List[str] = ana_data.cell_type_composition['sample'].unique().tolist()
    cell_types: List[str] = ana_data.cell_type_codes['Cell_Type'].tolist()

    output = []
    N = len(cell_types)
    for sample in samples:
        sample_df = ana_data.cell_type_composition.loc[ana_data.cell_type_composition['sample'] == sample]
        fig_width, fig_height = saptial_figsize(sample_df, scale_factor=ana_data.options.scale_factor)
        fig, axes = plt.subplots(1, N, figsize=(fig_width * N, fig_height))
        for j, cell_type in enumerate(cell_types):
            ax = axes[j]  # At least two cell types are required, checked at original data loading.
            scatter = ax.scatter(sample_df['x'],
                                 sample_df['y'],
                                 c=sample_df[cell_type],
                                 cmap='Reds',
                                 vmin=0,
                                 vmax=1,
                                 s=1)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.colorbar(scatter)
            ax.set_title(f"{sample} {cell_type}")
        fig.tight_layout()
        if ana_data.options.output is not None:
            fig.savefig(f'{ana_data.options.output}/{sample}_cell_type_composition.pdf', transparent=True)
            plt.close(fig)
        else:
            output.append((fig, axes))

    return output if len(output) > 0 else None


def plot_cell_type_composition(
        ana_data: AnaData) -> Optional[Union[List[Tuple[plt.Figure, plt.Axes]], Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of cell type composition.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    if hasattr(ana_data.options, 'sample') and ana_data.options.sample:
        return plot_cell_type_composition_sample(ana_data=ana_data)
    else:
        return plot_cell_type_composition_dataset(ana_data=ana_data)


def plot_niche_NT_score_dataset(ana_data: AnaData) -> Optional[Tuple[plt.Figure, plt.Axes]]:
    """
    Plot spatial distribution of niche NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    samples: List[str] = ana_data.NT_score['sample'].unique().tolist()

    try:
        if 'Niche_NTScore' not in ana_data.NT_score.columns:
            warning("Niche_NTScore not found in the NT score data.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    N = len(samples)
    fig, axes = plt.subplots(1, N, figsize=(3.5 * N, 3))
    for i, sample in enumerate(samples):
        sample_df = ana_data.NT_score.loc[ana_data.NT_score['sample'] == sample]
        ax = axes[i] if N > 1 else axes
        NT_score = sample_df['Niche_NTScore'] if not ana_data.options.reverse else 1 - sample_df['Niche_NTScore']
        scatter = ax.scatter(sample_df['x'], sample_df['y'], c=NT_score, cmap='rainbow', vmin=0, vmax=1, s=1)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(scatter)
        ax.set_title(f"{sample} Niche-level NT Score")

    fig.tight_layout()
    if ana_data.options.output is not None:
        fig.savefig(f'{ana_data.options.output}/niche_NT_score.pdf', transparent=True)
        plt.close(fig)
        return None
    else:
        return fig, axes


def plot_niche_NT_score_sample(ana_data: AnaData) -> Optional[List[Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of niche NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    samples: List[str] = ana_data.NT_score['sample'].unique().tolist()

    try:
        if 'Niche_NTScore' not in ana_data.NT_score.columns:
            warning("Niche_NTScore not found in the NT score data.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    output = []
    for sample in samples:
        sample_df = ana_data.NT_score.loc[ana_data.NT_score['sample'] == sample]
        fig_width, fig_height = saptial_figsize(sample_df, scale_factor=ana_data.options.scale_factor)
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
        NT_score = sample_df['Niche_NTScore'] if not ana_data.options.reverse else 1 - sample_df['Niche_NTScore']
        scatter = ax.scatter(sample_df['x'], sample_df['y'], c=NT_score, cmap='rainbow', vmin=0, vmax=1, s=1)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(scatter)
        ax.set_title(f"{sample} Niche-level NT Score")
        fig.tight_layout()
        if ana_data.options.output is not None:
            fig.savefig(f'{ana_data.options.output}/{sample}_niche_NT_score.pdf', transparent=True)
            plt.close(fig)
        else:
            output.append((fig, ax))

    return output if len(output) > 0 else None


def plot_niche_NT_score(
        ana_data: AnaData) -> Optional[Union[List[Tuple[plt.Figure, plt.Axes]], Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of niche NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    if hasattr(ana_data.options, 'sample') and ana_data.options.sample:
        return plot_niche_NT_score_sample(ana_data=ana_data)
    else:
        return plot_niche_NT_score_dataset(ana_data=ana_data)


def plot_cell_NT_score_dataset(ana_data: AnaData) -> Optional[Tuple[plt.Figure, plt.Axes]]:
    """
    Plot spatial distribution of cell NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    samples: List[str] = ana_data.NT_score['sample'].unique().tolist()

    try:
        if 'Cell_NTScore' not in ana_data.NT_score.columns:
            warning("Cell_NTScore not found in the NT score data.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    N = len(samples)
    fig, axes = plt.subplots(1, N, figsize=(3.5 * N, 3))
    for i, sample in enumerate(samples):
        sample_df = ana_data.NT_score.loc[ana_data.NT_score['sample'] == sample]
        ax = axes[i] if N > 1 else axes
        NT_score = sample_df['Cell_NTScore'] if not ana_data.options.reverse else 1 - sample_df['Cell_NTScore']
        scatter = ax.scatter(sample_df['x'], sample_df['y'], c=NT_score, cmap='rainbow', vmin=0, vmax=1, s=1)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(scatter)
        ax.set_title(f"{sample} Cell-level NT Score")

    fig.tight_layout()
    if ana_data.options.output is not None:
        fig.savefig(f'{ana_data.options.output}/cell_NT_score.pdf', transparent=True)
        plt.close(fig)
        return None
    else:
        return fig, axes


def plot_cell_NT_score_sample(ana_data: AnaData) -> Optional[List[Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of cell NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    samples: List[str] = ana_data.NT_score['sample'].unique().tolist()

    try:
        if 'Cell_NTScore' not in ana_data.NT_score.columns:
            warning("Cell_NTScore not found in the NT score data.")
            return None
    except FileNotFoundError as e:
        warning(str(e))
        return None

    output = []
    for sample in samples:
        sample_df = ana_data.NT_score.loc[ana_data.NT_score['sample'] == sample]
        fig_width, fig_height = saptial_figsize(sample_df, scale_factor=ana_data.options.scale_factor)
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
        NT_score = sample_df['Cell_NTScore'] if not ana_data.options.reverse else 1 - sample_df['Cell_NTScore']
        scatter = ax.scatter(sample_df['x'], sample_df['y'], c=NT_score, cmap='rainbow', vmin=0, vmax=1, s=1)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(scatter)
        ax.set_title(f"{sample} Cell-level NT Score")
        fig.tight_layout()
        if ana_data.options.output is not None:
            fig.savefig(f'{ana_data.options.output}/{sample}_cell_NT_score.pdf', transparent=True)
            plt.close(fig)
        else:
            output.append((fig, ax))

    return output if len(output) > 0 else None


def plot_cell_NT_score(
        ana_data: AnaData) -> Optional[Union[List[Tuple[plt.Figure, plt.Axes]], Tuple[plt.Figure, plt.Axes]]]:
    """
    Plot spatial distribution of cell NT score.
    :param ana_data: AnaData, the data for analysis.
    :return: None or Tuple[plt.Figure, plt.Axes].
    """

    if hasattr(ana_data.options, 'sample') and ana_data.options.sample:
        return plot_cell_NT_score_sample(ana_data=ana_data)
    else:
        return plot_cell_NT_score_dataset(ana_data=ana_data)


def spatial_visualization(ana_data: AnaData) -> None:
    """
    All spatial visualization will include here.
    :param ana_data: AnaData, the data for analysis.
    :return: None.
    """

    # 1. cell type composition
    if not hasattr(ana_data.options,
                   'suppress_cell_type_composition') or not ana_data.options.suppress_cell_type_composition:
        plot_cell_type_composition(ana_data=ana_data)

    # 2. NT score
    if not hasattr(ana_data.options, 'suppress_niche_trajectory') or not ana_data.options.suppress_niche_trajectory:
        plot_niche_NT_score(ana_data=ana_data)
        plot_cell_NT_score(ana_data=ana_data)
