import numpy as np
import nibabel as nib
from scipy.ndimage.measurements import label
import sys

from atlas_functions import sub_parcellate_region
    

def sub_parcellate(atlas):
    a= atlas.flatten()
    b = a[a>0]
    [values,counts] = np.unique(b,return_counts=True)
    sort_indices = np.argsort(counts)
    for i in range(len(counts)):
        atlas = split_connected_components(np.copy(atlas),values[sort_indices[i]])
    
    a= atlas.flatten()
    b = a[a>0]
    [values,counts] = np.unique(b,return_counts=True)
    sort_indices = np.argsort(counts) 
    #for i in reversed(range(len(counts))):
    #    check_connected_components(np.copy(atlas),values[sort_indices[i]])
    #atlas =  sub_parcellate_region(np.copy(atlas),12100)
    #atlas =  sub_parcellate_region(np.copy(atlas),22100)
    #return
   
    for i in reversed(range(len(counts))):
    #for i in []:
        if counts[sort_indices[i]]<(8000/3):
            break
        atlas =  sub_parcellate_region(np.copy(atlas),values[sort_indices[i]])
        a= atlas.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        print('global mean')
        print(np.mean(new_counts))
        print('global std')
        print(np.std(new_counts))
        sys.stdout.flush()
        if np.mean(new_counts) <2000:
            break
    
    
    return atlas
    

    
def check_connected_components( atlas, largest_region):
    struct =np.ones((3,3,3),dtype=bool).tolist()
    labeled_array, num_features = label(atlas==largest_region,struct)
    print(str(largest_region)+' num_features: '+str(num_features)+' size: '+str(np.sum(atlas==largest_region)))
    if num_features>1:
        for i in range(num_features):
            print(np.sum(labeled_array==i+1))
            
def split_connected_components( atlas, largest_region):
    if largest_region in [2200, 400, 800, 3300, 1800, 1200, 200, 1300, 1500, 4200, 4000, 1900, 3800, 1600, 3900, 600, 3400, 4300, 1100, 4400, 3500, 1400, 4100, 3700, 4500, 900]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        atlas[labeled_array==1]=10000+largest_region
        atlas[labeled_array==2]=20000+largest_region
        if num_features!=2:
            print('Number Of Features changend 0')
    elif largest_region in [2300,4600]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        a= labeled_array.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        sort_indices = np.argsort(new_counts) 
        atlas[labeled_array==new_values[sort_indices[2]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[1]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[0]]]=10000+largest_region
        if num_features!=3:
            print('Number Of Features changend 1')
    elif largest_region in [2000]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        a= labeled_array.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        sort_indices = np.argsort(new_counts) 
        atlas[labeled_array==new_values[sort_indices[2]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[1]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[0]]]=20000+largest_region
        if num_features!=3:
            print('Number Of Features changend 2')
    if largest_region in [500]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        a= labeled_array.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        sort_indices = np.argsort(new_counts) 
        atlas[labeled_array==new_values[sort_indices[4]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[3]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[2]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[1]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[0]]]=20000+largest_region
        if num_features!=5:
            print('Number Of Features changend 3')
    elif largest_region in [1000]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        a= labeled_array.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        sort_indices = np.argsort(new_counts) 
        atlas[labeled_array==new_values[sort_indices[3]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[2]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[1]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[0]]]=20000+largest_region
        if num_features!=4:
            print('Number Of Features changend 4')
    elif largest_region in [2100]:
        struct =np.ones((3,3,3),dtype=bool).tolist()
        labeled_array, num_features = label(atlas==largest_region,struct)
        a= labeled_array.flatten()
        b = a[a>0]
        [new_values,new_counts] = np.unique(b,return_counts=True)
        sort_indices = np.argsort(new_counts) 
        atlas[labeled_array==new_values[sort_indices[3]]]=20000+largest_region
        atlas[labeled_array==new_values[sort_indices[2]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[1]]]=10000+largest_region
        atlas[labeled_array==new_values[sort_indices[0]]]=10000+largest_region
        if num_features!=4:
            print('Number Of Features changend 5')
    elif (largest_region % 100) == 0:
        hemisphere = np.ones(np.shape(atlas),dtype=bool)
        hemisphere[:91,:,:] = True
        hemisphere[91:,:,:] = False
        left_hemisphere = np.logical_and((atlas==largest_region) , hemisphere)
        right_hemisphere = np.logical_and((atlas==largest_region) , np.logical_not(hemisphere))
        atlas[left_hemisphere] = 20000+largest_region
        atlas[right_hemisphere] = 10000+largest_region
    return atlas

 



img = nib.load('../atlases/HarvardOxford/HarvardOxford-cort-maxprob-thr25-1mm.nii')
img2 = nib.load('../atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr25-1mm.nii')

Volume1 = img.get_fdata().astype(np.intc)
Volume1[Volume1==34]=0
Volume1[Volume1==35]=0
Volume2 = img2.get_fdata().astype(np.intc)
Volume2[Volume2==1]=0
Volume2[Volume2==2]=0
Volume2[Volume2==3]=0
Volume2[Volume2==12]=0
Volume2[Volume2==13]=0
Volume2[Volume2==14]=0

combined_atlas = 100*Volume1+Volume2;

combined_atlas[combined_atlas==3019] =19
combined_atlas[combined_atlas==3009] =9
combined_atlas[combined_atlas==3114] =14
combined_atlas[combined_atlas==3103] =3


counter=500
if 1:
    
    sub_parcellated_atlas = sub_parcellate(combined_atlas);
    
    a= sub_parcellated_atlas.flatten()
    b = a[a>0]
    [values,counts] = np.unique(b,return_counts=True)
    print(str(counter)+' mean: '+str(np.mean(counts))+' std: '+str(np.std(counts)))
    #if np.std(counts)<500:
    array_img = nib.Nifti1Image(sub_parcellated_atlas,img.affine,None,img.extra)
    nib.save(array_img, 'combined_atlas'+str(counter)+'.nii.gz')
    #nib.save(array_img, 'naive_combined'+str(counter)+'.nii.gz')
    counter = counter -1
