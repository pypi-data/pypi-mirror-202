"""Parse Web Plot Digitizer projects to CSV.

This script aggregates data scraped from papers with Web Plot Digitizer. This folder has
subfolders associated with papers, which have a "paper.toml" describing the year of
publication, the authors of the paper, and the paper name itself. Each paper folder has
subfolders for each image processed by Web Plot Digitizer, which should have a "fig.jpg"
or similar file, a "wpd_project.json" resulting from exporting the processed data from
Web Plot Digitizer, and a "paper.toml" file indicating the figure number that the data
was scraped from. Be sure to assign sensible names to each dataset in the Web Plot
Digitizer GUI, because this also finds its way into the final data.

Reference: <https://gist.github.com/caiofcm/1088c9b62f0968b665a91f15ff23d447>
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import toml

from boilerdata.models.project import Project


def main(proj: Project):
    raw_df = pd.DataFrame(
        columns=["year", "authors", "paper", "fig", "dataset", "ΔT", "q''"]
    )
    dfs: list[pd.DataFrame] = []

    for paper in get_dirs_sorted(proj.dirs.literature):
        paper_meta = toml.loads((paper / "paper.toml").read_text(encoding="utf-8"))

        for fig in get_dirs_sorted(paper):
            fig_meta = toml.loads((fig / "fig.toml").read_text(encoding="utf-8"))
            data = (
                get_data(fig / "wpd_project.json")
                .rename(columns=dict(x="ΔT", y="q''", name="dataset"))
                .sort_values(["dataset", "ΔT", "q''"])
            )
            fig_df = raw_df.assign(**data, **paper_meta, **fig_meta).convert_dtypes()
            dfs.append(fig_df)

    df = pd.concat(dfs)
    df.to_csv(proj.dirs.file_literature_results, index=False)


# * -------------------------------------------------------------------------------- * #
# * UTILS


def get_dirs_sorted(path: Path) -> list[Path]:
    return [
        path
        for path in sorted(path.iterdir())
        if path.is_dir() and "." not in path.name
    ]


# * -------------------------------------------------------------------------------- * #
# * WEB PLOT DIGITIZER


def get_data(file: str | Path) -> pd.DataFrame:
    data = json.loads(Path(file).read_text(encoding="utf-8"))
    data = get_dict(data)
    return get_df(data)


def get_dict(data: dict[str, Any]) -> dict[str, Any]:
    dataset_coll = data["datasetColl"]
    dict_of_data_sets = {}
    for data_set in dataset_coll:
        data = data_set["data"]
        xy_par = np.array([datum["value"] for datum in data])  # type: ignore  # pandas
        dict_of_data_sets[data_set["name"]] = xy_par
    return dict_of_data_sets


def get_df(data: dict[str, Any]) -> pd.DataFrame:
    list_of_dfs = []
    for name, xy_matrix in data.items():
        df = pd.DataFrame(
            {
                "x": xy_matrix[:, 0],
                "y": xy_matrix[:, 1],
                "name": name,
            }
        )
        list_of_dfs += [df]
    return pd.concat(list_of_dfs, ignore_index=True)


# * -------------------------------------------------------------------------------- * #

if __name__ == "__main__":
    main(Project.get_project())
