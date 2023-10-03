import os
import glob
import nibabel as nib
import numpy as np
import SimpleITK as sitk
from tqdm.contrib.itertools import product
from dfsio import readdfs, writedfs
from multiprocessing import Pool

import nibabel as nib
import numpy as np


def get_cortical_thickness(surf_file):
    s = readdfs(surf_file)

    return s.attributes


def get_roi_vols(label_file, unique_labels):
    unique_labels = unique_labels.astype(int)
    # Load the NIfTI file
    nifti_img = nib.load(label_file)  # Replace with your NIfTI file path

    # Get the data array from the NIfTI image
    sub_lab_data = nifti_img.get_fdata().astype(int)
    roi_data = np.mod(sub_lab_data, 1000)
    roi_data[sub_lab_data == 2000] = 2000

    # Get voxel dimensions (voxel size)
    voxel_size = np.prod(nifti_img.header.get_zooms())

    # Get unique ROI labels
    # unique_labels = np.unique(roi_data)

    # Initialize an array to store ROI volumes
    roi_volumes = []

    roi_volumes = np.full(len(unique_labels), np.nan)

    # Compute the volume for each ROI
    for i, label in enumerate(unique_labels):
        roi_volume = np.sum(roi_data == label) * voxel_size
        roi_volumes[i] = roi_volume

    return roi_volumes


label_ids = np.unique(
    nib.load(
        "/home/ajoshi/BrainSuite23a/svreg/BrainSuiteAtlas1/mri.label.nii.gz"
    ).get_fdata()
)


left_surf = readdfs(
    "/home/ajoshi/BrainSuite23a/svreg/BrainSuiteAtlas1/mri.left.mid.cortex.dfs"
)


right_surf = readdfs(
    "/home/ajoshi/BrainSuite23a/svreg/BrainSuiteAtlas1/mri.right.mid.cortex.dfs"
)


nsub = 5
param_list = ("1e-14", "2e-14")

roi_vols_lf = np.full((2, nsub, 2, len(label_ids)), np.nan)

thickness_left_lf = np.full((2, nsub, 2, len(left_surf.vertices)), np.nan)
thickness_right_lf = np.full((2, nsub, 2, len(right_surf.vertices)), np.nan)


for sess, n, p in product((1, 2), range(1, nsub + 1), range(2)):
    param = param_list[p]
    out_dir = (
        "/deneb_disk/3T_vs_low_field/justins_recons/low_field_mprage_data_BrainSuite/subj"
        + str(n)
        + "_vol"
        + str(sess)
        + "/"
        + param
    )

    sub_label_file = out_dir + "/T1.svreg.label.nii.gz"
    sub_thickness_left_file = out_dir + "/atlas.pvc-thickness_0-6mm.left.mid.cortex.dfs"
    sub_thickness_right_file = (
        out_dir + "/atlas.pvc-thickness_0-6mm.right.mid.cortex.dfs"
    )

    # img = nib.load(sub_label_file)
    # data = img.get_fdata()

    if os.path.isfile(sub_label_file):
        roi_vols_lf[sess - 1, n - 1, p, :] = get_roi_vols(sub_label_file, label_ids)
        thickness_left_lf[sess - 1, n - 1, p, :] = get_cortical_thickness(
            sub_thickness_left_file
        )
        thickness_right_lf[sess - 1, n - 1, p, :] = get_cortical_thickness(
            sub_thickness_right_file
        )

    else:
        print(
            f"The following label file does not exist!! {sub_label_file} Skipping...:"
        )

np.savez(
    "brainSuite_low_field.npz",
    roi_vols=roi_vols_lf,
    thickness_left=thickness_left_lf,
    thickness_right=thickness_right_lf,
    nsub=nsub,
    param_list=param_list,
    label_ids=label_ids,
)

print("Done! for LF")


roi_vols_3t = np.full((2, nsub, len(label_ids)), np.nan)
thickness_left_3t = np.full((2, nsub, len(left_surf.vertices)), np.nan)
thickness_right_3t = np.full((2, nsub, len(right_surf.vertices)), np.nan)

for sess, n in product((1, 2), range(1, nsub + 1)):
    out_dir = (
        "/deneb_disk/3T_vs_low_field/3T_mprage_data_BrainSuite/subj"
        + str(n)
        + "_vol"
        + str(sess)
    )

    sub_label_file = out_dir + "/T1.svreg.label.nii.gz"
    sub_thickness_left_file = out_dir + "/atlas.pvc-thickness_0-6mm.left.mid.cortex.dfs"
    sub_thickness_right_file = (
        out_dir + "/atlas.pvc-thickness_0-6mm.right.mid.cortex.dfs"
    )

    # img = nib.load(sub_label_file)
    # data = img.get_fdata()

    if os.path.isfile(sub_label_file):
        roi_vols_3t[sess - 1, n - 1, :] = get_roi_vols(sub_label_file, label_ids)
        thickness_left_3t[sess - 1, n - 1, :] = get_cortical_thickness(
            sub_thickness_left_file
        )
        thickness_right_3t[sess - 1, n - 1, :] = get_cortical_thickness(
            sub_thickness_right_file
        )

    else:
        print(
            f"The following label file does not exist!! {sub_label_file} Skipping...:"
        )

np.savez(
    "brainSuite_3T.npz",
    roi_vols=roi_vols_3t,
    thickness_left=thickness_left_3t,
    thickness_right=thickness_right_3t,
    nsub=nsub,
    param_list=param_list,
    label_ids=label_ids,
)
print("Done! for 3T")
