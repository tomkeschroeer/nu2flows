"""
Create a simple plot comparing the test set neutrino kinematics to truth
"""
import pyrootutils

root = pyrootutils.setup_root(search_from=__file__, pythonpath=True)

from pathlib import Path
import h5py
import numpy as np
from dotmap import DotMap

from utils.plotting import plot_multi_hists_2
from src.datamodules.physics import Mom4Vec
from src.utils import read_dilepton_file

# Paths to the relevant files
data_file = "/srv/beegfs/scratch/groups/rodem/ttbar_evt_reco/data_share/20231201_distop_m600_chichi_m300_ttbar_allhad_semilep_10M/hdf5/events_selected_3311.h5"
plot_dir = root / "stops_nu2flows_rename/stop_models/outputs/plots"

# Load the event data from the file
file_data = read_dilepton_file(Path(data_file))
with h5py.File(data_file, "r") as f:
    rem_data = f["delphes"]

    input_vars = {
        "MET": ["px", "py"],
        "leptons": ["px", "py", "pz", "E", "charge", "type"],
        "jets": ["px", "py", "pz", "E", "is_tagged"],
        "misc": ["njets", "nbjets"],
    }

    for key, val in input_vars.items():
        data_mask_px = getattr(file_data[key],"px",None) if key != "misc" else file_data["njets"]
        data_mask_px = ~(data_mask_px == 0)
        data_mask_pt = rem_data[key]["pt"] if (key != "misc" and key != "MET") else None
        if data_mask_pt is not None:
            data_mask_pt = ~(data_mask_pt == 0)
        for var in val:
            data = getattr(file_data[key],var,None) if key != "misc" else file_data[var]
            if data is None:
                mask = data_mask_pt
            else:
                mask = data_mask_px
            data = rem_data[key][var] if data is None else data
            data = data[mask]
            data = np.expand_dims(data, -1)

            print(f"plot {var} for {key}")

            plot_multi_hists_2(
                data_list=[data],
                data_labels=[""],
                col_labels=[f"{var} of {key}"],
                path=plot_dir / f"{key}_{var}.png",
                bins=50 , #[np.linspace(min(data), max(data), 50)],
                # bins=np.linspace(0, 5, 30),
                do_err=True,
            )

