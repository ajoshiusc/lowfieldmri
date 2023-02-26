import nibabel
import pydicom
import os
from tqdm import tqdm
from glob import glob


def convertNsave(arr,file_dir, index=0):
    """
    `arr`: parameter will take a numpy array that represents only one slice.
    `file_dir`: parameter will take the path to save the slices
    `index`: parameter will represent the index of the slice, so this parameter will be used to put 
    the name of each slice while using a for loop to convert all the slices
    """
    
    dicom_file = pydicom.dcmread('images/dcmimage.dcm')
    arr = arr.astype('uint16')
    dicom_file.Rows = arr.shape[0]
    dicom_file.Columns = arr.shape[1]
    dicom_file.PhotometricInterpretation = "MONOCHROME2"
    dicom_file.SamplesPerPixel = 1
    dicom_file.BitsStored = 16
    dicom_file.BitsAllocated = 16
    dicom_file.HighBit = 15
    dicom_file.PixelRepresentation = 1
    dicom_file.PixelData = arr.tobytes()
    dicom_file.save_as(os.path.join(file_dir, f'slice{index}.dcm'))


def nifti2dicom_1file(nifti_dir, out_dir):
    """
    This function is to convert only one nifti file into dicom series
    `nifti_dir`: the path to the one nifti file
    `out_dir`: the path to output
    """

    nifti_file = nibabel.load(nifti_dir)
    nifti_array = nifti_file.get_fdata()
    number_slices = nifti_array.shape[2]

    for slice_ in tqdm(range(number_slices)):
        convertNsave(nifti_array[:,:,slice_], out_dir, slice_)

    



def main():        


  list_svr_files = glob.glob('/home/ajoshi/projects/disc_mri/clinical_svr_study/SVR*SVR.nii.gz')

  for nii_file in list_svr_files:
       
  
    output_dcm_path = '/home/ajoshi/projects/disc_mri/clinical_svr_study/SVR001_SVR_dicom_my'

    nifti_file = nibabel.load(nii_file)
    nifti2dicom_1file(nii_file, output_dcm_path)


