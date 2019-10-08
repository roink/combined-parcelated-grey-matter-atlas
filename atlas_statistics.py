import nibabel as nib
import numpy as np
from atlas_functions import find_diameter

def sub_label(argument):
    switcher = {
        0 : "Left Cerebral White Matter",
        1 : "Left Cerebral Cortex",
        2 : "Left Lateral Ventricle",
        3 : "Left Thalamus",
        4 : "Left Caudate",
        5 : "Left Putamen",
        6 : "Left Pallidum",
        7 : "Brain-Stem",
        8 : "Left Hippocampus",
        9 : "Left Amygdala",
        10 : "Left Accumbens",
        11 : "Right Cerebral White Matter",
        12 : "Right Cerebral Cortex",
        13 : "Right Lateral Ventricle",
        14 : "Right Thalamus",
        15 : "Right Caudate",
        16 : "Right Putamen",
        17 : "Right Pallidum",
        18 : "Right Hippocampus",
        19 : "Right Amygdala",
        20 : "Right Accumbens"
    }
    return switcher.get(argument-1, None)
    
def cort_label(argument):
    switcher = {
        0 : "Frontal Pole",
		1 : "Insular Cortex",
		2 : "Superior Frontal Gyrus",
		3 : "Middle Frontal Gyrus",
		4 : "Inferior Frontal Gyrus pars triangularis",
		5 : "Inferior Frontal Gyrus pars opercularis",
		6 : "Precentral Gyrus",
		7 : "Temporal Pole",
		8 : "Superior Temporal Gyrus anterior division",
		9 : "Superior Temporal Gyrus posterior division",
		10 : "Middle Temporal Gyrus anterior division",
		11 : "Middle Temporal Gyrus posterior division",
		12 : "Middle Temporal Gyrus temporooccipital part",
		13 : "Inferior Temporal Gyrus anterior division",
		14 : "Inferior Temporal Gyrus posterior division",
		15 : "Inferior Temporal Gyrus temporooccipital part",
		16 : "Postcentral Gyrus",
		17 : "Superior Parietal Lobule",
		18 : "Supramarginal Gyrus anterior division",
		19 : "Supramarginal Gyrus posterior division",
		20 : "Angular Gyrus",
		21 : "Lateral Occipital Cortex superior division",
		22 : "Lateral Occipital Cortex inferior division",
		23 : "Intracalcarine Cortex",
		24 : "Frontal Medial Cortex",
		25 : "Juxtapositional Lobule Cortex (formerly Supplementary Motor Cortex)",
		26 : "Subcallosal Cortex",
		27 : "Paracingulate Gyrus",
		28 : "Cingulate Gyrus anterior division",
		29 : "Cingulate Gyrus posterior division",
		30 : "Precuneous Cortex",
		31 : "Cuneal Cortex",
		32 : "Frontal Orbital Cortex",
		33 : "Parahippocampal Gyrus anterior division",
		34 : "Parahippocampal Gyrus posterior division",
		35 : "Lingual Gyrus",
		36 : "Temporal Fusiform Cortex anterior division",
		37 : "Temporal Fusiform Cortex posterior division",
		38 : "Temporal Occipital Fusiform Cortex",
		39 : "Occipital Fusiform Gyrus",
		40 : "Frontal Operculum Cortex",
		41 : "Central Opercular Cortex",
		42 : "Parietal Operculum Cortex",
		43 : "Planum Polare",
		44 : "Heschl's Gyrus (includes H1 and H2)",
		45 : "Planum Temporale",
		46 : "Supracalcarine Cortex",
		47 : "Occipital Pole"
    }
    return switcher.get(argument-1, None)


def change_labels(atlas,filename):
    a= atlas.flatten()
    print(np.max(atlas))
    b = a[a>0]
    counter=1
    [values,counts] = np.unique(b,return_counts=True)
    new_atlas = np.zeros(np.shape(atlas),dtype=np.intc)
    with open(filename+"_labels2.txt","w") as f:
        for i in range(23):
            for j in range(50):
                c = b[(b % 10000) == (100*j+i)]
                [values,counts] = np.unique(c,return_counts=True)
                for k in range(len(values)):
                    new_atlas[atlas==values[k]]=counter
                    
                    
                    #diameter = np.around(find_diameter(new_atlas,counter),2)
                    #if sub_label(i) is None:
                    #    f.write(str(counter)+',"'+cort_label(j)+'",'+str(np.sum(atlas==values[k]))+","+str(diameter)+"\n")
                    #elif cort_label(j) is None:
                    #    f.write(str(counter)+',"'+sub_label(i)+'",'+str(np.sum(atlas==values[k]))+","+str(diameter)+"\n")
                    #else:
                    #    f.write(str(counter)+',"'+cort_label(j)+" x "+sub_label(i)+'",'+str(np.sum(atlas==values[k]))+","+str(diameter)+"\n")
                    counter = counter+1
                    #f.flush()
    return new_atlas
                             
#for filename in [ "sub_atlas","naive_combined","cort_atlas"]:
for filename in [ "/home/philipp/alzheimers/combined-atlas/2018_09_17/combined_atlas_2018_09_17"]:
    img = nib.load(filename+".nii.gz")
#print(img)

    atlas = img.get_fdata().astype(np.int)
    [x,y,z] = np.shape(atlas)
    print(np.max(atlas))
    #a= atlas.flatten()
    #b = a[a>0]
    #[values,counts] = np.unique(b,return_counts=True)
    #print(filename+" mean: "+str(np.mean(counts)/1000)+" std: "+str(np.std(counts)/1000)+" "+str(np.size(values)))
    
    #new_atlas = change_labels(atlas,'combined_atlas_new_labels_2018_09_17')
    #with open('superior_cerebellum_coord_list.txt',"w+") as f:
    #    for i in range(x):
    #        for j in range(y):
    #            for k in range(z):
    #                if atlas[i,j,k]>0:
    #                
    #                    f.write(str(atlas[i,j,k])+" "+str(i)+" "+str(j)+" "+str(k)+'\n')
        
    #array_img = nib.Nifti1Image(new_atlas,img.affine,None,img.extra)
    #nib.save(array_img, "combined_atlas_new_labels_2018_09_17.nii.gz")
