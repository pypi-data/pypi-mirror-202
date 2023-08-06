# * -------------------------------------------------------------------------------- * #
# * GET RUNS


from datetime import datetime

import pandas as pd

from boilerdata.models.project import Project
from boilerdata.stages.common import set_dtypes
from boilerdata.stages.prep.common import get_run

# * -------------------------------------------------------------------------------- * #
# * MAIN


def main(proj: Project):
    (
        pd.DataFrame(
            columns=[ax.name for ax in proj.axes.cols], data=get_runs(proj)
        ).to_csv(proj.dirs.file_runs, encoding="utf-8")
    )


# * -------------------------------------------------------------------------------- * #
# * STAGES


def get_runs(proj: Project) -> pd.DataFrame:
    """Get runs from all trials."""

    # Get runs and multiindex
    dtypes = {col.name: col.dtype for col in proj.axes.source if not col.index}
    runs: list[pd.DataFrame] = []
    multiindex: list[tuple[datetime, datetime, datetime]] = []
    for trial in proj.trials:
        for file, run_index in zip(trial.run_files, trial.run_index, strict=True):
            run = get_run(proj, file).tail(proj.params.records_to_average)
            runs.append(run)
            multiindex.extend(
                tuple((*run_index, record_time) for record_time in run.index)
            )

    return (
        pd.concat(runs)
        .set_index(
            pd.MultiIndex.from_tuples(
                multiindex, names=[idx.name for idx in proj.axes.index]
            )
        )
        .pipe(set_dtypes, dtypes)
    )


# * -------------------------------------------------------------------------------- * #

if __name__ == "__main__":
    main(Project.get_project())
