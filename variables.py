import io
import pandas as pd
from scipy.io import loadmat
import numpy as np
from datetime import datetime
import base64
from pymatreader import read_mat


def image_variables(filename_decode):
    data = loadmat(
        base64.decodebytes(filename_decode)
    ),
    ct_img = data['ct_image']
    pt_img = data['pt_image']
    ct_bone = ct_img > 260
    ct_pt_bone_mask = np.multiply(ct_bone, pt_img)
    print('max', np.max(ct_img))
    print('min', np.min(ct_img))

    pt_pixel_spacing = data['pt_pixel_spacing']
    pt_slice_thickness = data['pt_slice_thickness']

    # calculate voxel volume
    voxel_volume = (pt_pixel_spacing[0] * pt_pixel_spacing[1] * pt_slice_thickness) / 10
    print(voxel_volume)

    return ct_img, ct_pt_bone_mask, voxel_volume
