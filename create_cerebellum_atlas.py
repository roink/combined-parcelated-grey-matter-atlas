import numpy as np

import nibabel as nib
if 0:
    img = nib.load('../atlases/Cerebellum/Cerebellum-MNIfnirt-maxprob-thr25-1mm.nii.gz')

    Volume1 = img.get_fdata().astype(np.intc)
    Volume1[Volume1>0]=1
    print(np.sum(Volume1==1))

    nib.viewers.OrthoSlicer3D(Volume1)
    array_img = nib.Nifti1Image(Volume1,img.affine,None,img.extra)
    nib.save(array_img, 'cerebellum_atlas.nii.gz')


img = nib.load('../atlases/Cerebellum/Cerebellum-MNIfnirt-maxprob-thr25-1mm.nii.gz')

Volume1 = img.get_fdata().astype(np.intc)
Volume1[np.logical_and(Volume1>0,Volume1<=10)]=1
Volume1[(Volume1>10)]=0
print(np.sum(Volume1==1))

nib.viewers.OrthoSlicer3D(Volume1)
array_img = nib.Nifti1Image(Volume1,img.affine,None,img.extra)
nib.save(array_img, 'superior_cerebellum.nii.gz')
