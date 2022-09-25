# This file converts a batch of acquisitions at DISC to nifti files

import dicom2nifti
import glob
import os

#scans_dir = '/deneb_disk/fetal_scan_8_3_2022/data'
scans_dir = '/deneb_disk/fetal_heart_data_svr_ye_tian_9_5_2022/multiple_stacks/21_stacks/dicom_recon_21_stacks/dicom_recon'
scans = glob.glob(scans_dir+"/*")

#out_dir = '/deneb_disk/fetal_scan_8_3_2022/nifti'
out_dir = '/deneb_disk/fetal_heart_data_svr_ye_tian_9_5_2022/multiple_stacks/21_stacks/dicom_recon_21_stacks/nii_files'

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

for s in scans:
    print(s)

    dicom2nifti.convert_dir.convert_directory(s, out_dir, compression=True)













