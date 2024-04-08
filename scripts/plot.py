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
data_file = "/srv/beegfs/scratch/groups/rodem/ttbar_evt_reco/data_share/20231201_distop_m600_chichi_m300_ttbar_allhad_semilep_10M/hdf5/events_selected_1036.h5"
model_file = root / "stops_nu2flows_rename/stop_models/outputs/events_selected_1036.h5"
plot_dir = root / "stops_nu2flows_rename/stop_models/outputs/plots"

# Load the event data from the file
file_data = read_dilepton_file(Path(data_file))

# Define the model neutrino as a dict and load the data
nuflow = DotMap(
    {
        "name": "nu2flows",
        "label": r"$\nu^2$-Flows",
        "hist_kwargs": {"color": "b"},
    }
)
with h5py.File(model_file, "r") as f:
    data_neutrino = f["neutralino_1"][:, :1]
    data_antineutrino = f["neutralino_2"][:, :1]
    nuflow.nu_1 = Mom4Vec(data_neutrino[:], final_is_mass=True)
    nuflow.nu_2 = Mom4Vec(data_antineutrino[:], final_is_mass=True)

# Define the truth neutrino as a dict and load from the file

nutruth = DotMap(
    {
        "name": "truth_nu",
        "label": r"$\nu$-Truth",
        "nu_1": Mom4Vec(file_data.neutralinos.mom[:, None, 0, :]),
        "nu_2": Mom4Vec(file_data.neutralinos.mom[:, None, 1, :]),
        "hist_kwargs": {"color": "grey", "fill": True, "alpha": 0.5},
        "err_kwargs": {"color": "grey", "hatch": "///"},
    }
)

# Combine the two neutrino types into a single list
neutrino_list = [nuflow, nutruth]

# Create the plotting folder
plot_dir.mkdir(parents=True, exist_ok=True)

# Plot the neutrino energy
plot_multi_hists_2(
    data_list=[n.nu_1.E for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="Energy [MeV]",
    path=plot_dir / "energy_nu1.png",
    bins=np.linspace(0, 2000, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_2.E for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="Energy [MeV]",
    path=plot_dir / "energy_nu2.png",
    bins=np.linspace(0, 2000, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_1.px for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_x$ [MeV]",
    path=plot_dir / "px_nu1.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_2.px for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_x$ [MeV]",
    path=plot_dir / "px_nu2.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_1.py for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_y$ [MeV]",
    path=plot_dir / "py_nu1.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_2.py for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_y$ [MeV]",
    path=plot_dir / "py_nu2.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_1.pz for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_z$ [MeV]",
    path=plot_dir / "pz_nu1.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

plot_multi_hists_2(
    data_list=[n.nu_2.pz for n in neutrino_list],
    data_labels=[n.label for n in neutrino_list],
    col_labels="$p_z$ [MeV]",
    path=plot_dir / "pz_nu2.png",
    bins=np.linspace(0, 600, 30),
    # bins=np.linspace(0, 5, 30),
    do_err=True,
    hist_kwargs=[n.hist_kwargs for n in neutrino_list],
    err_kwargs=[n.err_kwargs for n in neutrino_list],
)

# Pull out the anti-lepton from the file data
# lep = file_data.leptons[:, 1:2]

# # Pull out the corresponding b jet, create a 4 vector object
# b_loc = file_data.jets_indices == 0
# bjet = np.zeros((len(file_data.jets_indices), 1, 4))
# bjet[np.any(b_loc, axis=-1)] = file_data.jets[b_loc].mom[:, None]
# bjet = Mom4Vec(bjet)

# # For each neutrino definition in the list, create a top candidate from the triplet
# for n in neutrino_list:
#     n.top = n.nu + lep + bjet

# # Plot the top mass
# plot_multi_hists_2(
#     data_list=[n.top.mass[file_data.has_both_bs] for n in neutrino_list],
#     data_labels=[n.label for n in neutrino_list],
#     col_labels="Top mass [GeV]",
#     path=plot_dir / "mass.png",
#     bins=np.linspace(0, 400, 100),
#     do_err=True,
#     hist_kwargs=[n.hist_kwargs for n in neutrino_list],
#     err_kwargs=[n.err_kwargs for n in neutrino_list],
# )
