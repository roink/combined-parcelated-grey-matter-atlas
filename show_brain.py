import nibabel as nib
import numpy as np
                             

def change_labels(atlas):
    new_atlas = np.zeros(np.shape(atlas),dtype=np.intc)
    a= atlas.flatten()
    b = a[a>0]
    [values,counts] = np.unique(b,return_counts=True)
    new_label = np.random.permutation(np.size(values))+1
    for i in (range(np.size(values))):
        new_atlas[atlas==values[i]]=new_label[i]
        
        
    return new_atlas

#img = nib.load('/home/philipp/alzheimers/neurodegeneration-forecast/atlases/combined_atlas.nii.gz')
#img = nib.load('/home/philipp/alzheimers/combined-atlas/DTI/DTI_atlas.nii')
#img = nib.load('/tmp/DTI_atlas.nii')

#img = nib.load('/home/philipp/alzheimers/combined-atlas/white_matter_ventricels/ventricle.nii')
img = nib.load('/home/philipp/alzheimers/combined-atlas/white_matter_ventricels/ventricle_regions.nii.gz')

#img = nib.load('/home/philipp/alzheimers/combined-atlas/white_matter_ventricels/white_matter_regions.nii.gz')

#img = nib.load('/home/philipp/alzheimers/neurodegeneration-forecast/atlases/Skull Strpped/diff_preproc_brain.nii')

#print(img)

atlas = img.get_fdata().astype(np.int)

print(np.sum(atlas))
    
a=nib.viewers.OrthoSlicer3D(atlas)
a.cmap='nipy_spectral'
#a.cmap='cubehelix'
a.draw()
a.show()
