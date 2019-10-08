import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free

def import_seeds():
    def manual_parsing(filename,delim,dtype):
        out = list()
        lengths = list()
        with open(filename,'r') as ins:
            for line in ins:
                l = line.split(delim)
                out.append(l)
                lengths.append(len(l))
        lim = np.max(lengths)
        for l in out:
            while len(l)<lim:
                l.append(0)
        return np.array(out,dtype=dtype)

    switcher = {}

    seeds = manual_parsing("seed_lists/combined_list_10.txt"," ",float)

    values = np.unique(seeds[:,0])

    for i in range(len(values)):
        key = values[i].astype(int)
        a = seeds[seeds[:,0]==values[i],1:]
        b = np.argsort(a[:,0])
        a = a[b,:]
        a = a[0:2,1:]
        b = np.argsort(a[:,0])
        a = a[b,:]
        value = a[0,1:]
        value = value[value>0].astype(int)
        switcher[key]=value
    return switcher

switcher = import_seeds()


cdef int calc_unassigned( int [:,:,:] atlas,int largest_region):
    cdef int output=0
    cdef int x,y,z
    for x in range(182):
        for y in range(218):
            for z in range(182):
                if atlas[x,y,z] == largest_region:
                    output = output+1
    return output
    
    
    
cdef int [:,:,:] dilate_region(int [:,:,:] atlas, int region_number, int largest_region, int radius):
    cdef int [:,:,:] output = atlas.copy()
    cdef int x,y,z,radiusx,radiusy,radiusz
    
    for x in range(atlas.shape[0]):
        for y in range(atlas.shape[1]):
            for z in range(atlas.shape[2]):
                output[x,y,z] = atlas[x,y,z]
    
    for x in range(atlas.shape[0]):
        for y in range(atlas.shape[1]):
            for z in range(atlas.shape[2]):
                if atlas[x,y,z] == region_number:
                    for radiusx in range(-radius,radius+1):
                        #print radiusx
                        for radiusy in range(-radius,radius+1):
                            for radiusz in range(-radius,radius+1):
                                if (0 <= (x+radiusx) < atlas.shape[0]) and (0 <= (y+radiusy) < atlas.shape[1]) and (0 <= (z+radiusz) < atlas.shape[2]):
                                    if ((radiusx*radiusx+radiusy*radiusy+radiusz*radiusz)**0.5)<=radius:
                                        if (atlas[x+radiusx,y+radiusy,z+radiusz] % 100000) == largest_region:
                                            output[x+radiusx,y+radiusy,z+radiusz] = region_number
                                        #pass
                            
    return output
    
    
cdef int [:,:,:] performe_step(int [:,:,:] atlas_view, int largest_region, int number_of_sub_parcels):
    cdef int I,radius,new_unassigned
    seed_sizes=<int*> malloc(sizeof(int) * number_of_sub_parcels)
    cdef int unassigned = calc_unassigned(atlas_view,largest_region)
    cdef int unchanged = 0;
    cdef int i,x,y,z,indx
    cdef int seed_min

    while ((unassigned>0) or not(unchanged>100)):
        ## Calculate seed_sizes
        for i in range(number_of_sub_parcels):
            seed_sizes[i]=0
        for x in range(atlas_view.shape[0]):
            for y in range(atlas_view.shape[1]):
                for z in range(atlas_view.shape[2]):
                    if (atlas_view[x,y,z] % 100000)==largest_region:
                        indx = atlas_view[x,y,z]/100000-1
                        if indx>= 0:
                            seed_sizes[indx] = seed_sizes[indx] + 1             
        ## Find Index I of nonzero minimal element of seed_sizes
        I=0
        seed_min = seed_sizes[0]
        for i in range(number_of_sub_parcels):
            if seed_sizes[i]>0:
                if seed_sizes[i]<seed_min:
                    seed_min = seed_sizes[i]
                    I = i

        if seed_sizes[I] == 0:
            break
        
        radius = unchanged/number_of_sub_parcels +1
            
        if unassigned==0:
            radius = 1
            
        atlas_view = dilate_region(atlas_view,(I+1)*100000+largest_region,largest_region,radius)
        
        new_unassigned = calc_unassigned(atlas_view,largest_region)
        if new_unassigned< unassigned:
            unchanged=0;
            unassigned = new_unassigned;
        else:
            unchanged = unchanged+1;
    free(seed_sizes)
    return atlas_view
    
def provide_seeds(np.ndarray flat_atlas,int largest_region, int number_of_sub_parcels):
    cdef tuple candidate_list
    cdef Py_ssize_t [:] idx
    
    seeds = switcher.get(largest_region,None)
    if seeds is None:
        print('Provided no seeds for ' + str(largest_region))
        candidate_list = np.where(flat_atlas==largest_region)
        idx = np.random.choice(range(len(candidate_list[0].tolist())),number_of_sub_parcels,replace=False).astype(int)
        seeds = candidate_list[0][idx]
    if len(seeds) != number_of_sub_parcels:
        print('Provided wrong number of seeds ' + str(largest_region))
        1/0
    return seeds

    
def sub_parcellate_region(np.ndarray atlas,int largest_region):
    cdef np.ndarray true_atlas = np.copy(atlas)
    cdef np.ndarray flat_atlas
    cdef int unassigned = np.sum(atlas==largest_region)
    
    cdef int number_of_sub_parcels = np.around(unassigned/2000.0);
    if number_of_sub_parcels <2:
        number_of_sub_parcels = 2
    if largest_region in [100,700,1700,300]:
        number_of_sub_parcels = number_of_sub_parcels+1
    cdef Py_ssize_t i
    cdef int [:,:,:] atlas_view
    #cdef Py_ssize_t [:] seeds
    
    max_diameter=10
    cdef float diameter = max_diameter+1
    cdef int volume=0
    cdef int region_volume
    cdef float region_diameter
    cdef int counter = 0

    while (unassigned> 0) or (counter<25):
        flat_atlas = np.reshape(np.copy(true_atlas),-1)
        seeds = provide_seeds(flat_atlas, largest_region, number_of_sub_parcels)
        for i in range(len(seeds)):
            flat_atlas[seeds[i]] = (i+1)*100000+largest_region
        atlas = np.reshape(flat_atlas,np.shape(true_atlas))
        atlas_view =atlas
        #print calc_unassigned( atlas_view, largest_region)
        atlas_view = performe_step( atlas_view, largest_region, number_of_sub_parcels)
        unassigned= calc_unassigned( atlas_view, largest_region)
        diameter = 0
        volume = 0
        if unassigned>0:
            print 'retry with new seeds, some voxels unassigned'
         
        if switcher.get(largest_region,None) is None: 
            for i in range(len(seeds)):
                if (calc_unassigned( atlas_view, (i+1)*100000+largest_region) > 0):
                    region_volume = calc_unassigned( atlas_view, (i+1)*100000+largest_region)
                    if region_volume>volume:
                        volume = region_volume
                    region_diameter = find_diameter(np.asarray(atlas_view), (i+1)*100000+largest_region)
                    if region_diameter>diameter:
                        diameter = region_diameter
                    
            
            if diameter > max_diameter:
                print('retry with new seeds, diameter too large: '+str(diameter))
                #max_diameter = max_diameter +0.05
            if (diameter == 0):
                print('diameter == 0')
                1/0
            print_string = str(largest_region)+' '+str(diameter)+' '+str(volume)
            for i in range(len(seeds)):
                print_string = print_string + ' '+str(seeds[i])
            print_string = print_string + '\n'    
            with open('seed_lists/seed_list_500.txt',"a+") as f:
                f.write(print_string)
            counter = counter+1
        else:
            counter=100
        
    return np.asarray(atlas_view)
    
cdef float find_diameter_fast(int [:,:,:] atlas, int region_number, int xlow, int xhigh, int ylow, int yhigh, int zlow, int zhigh):
    cdef float max_diameter=0.0
    cdef float i,j,k,l,m,n,diameter
    cdef int iplus,iminus,jplus,jminus,kplus,kminus,lplus,lminus,mplus,mminus,nplus,nminus
    i=xlow-0.5
    iplus = xlow
    iminus = xlow-1
    while i < (xhigh+1.6):
        j = ylow-0.5
        jplus = ylow
        jminus = ylow-1
        while j<(yhigh+1.6):
            k = zlow-0.5
            kplus = zlow
            kminus = zlow-1
            while k<(zhigh+1.6):
                if (region_number==atlas[iplus,jplus,kplus]) or (region_number==atlas[iplus,jplus,kminus]) or (region_number==atlas[iplus,jminus,kplus]) or (region_number==atlas[iplus,jminus,kminus]) or (region_number==atlas[iminus,jplus,kplus]) or (region_number==atlas[iminus,jplus,kminus]) or (region_number==atlas[iminus,jminus,kplus]) or (region_number==atlas[iminus,jminus,kminus]):
                    l = xlow-0.5
                    lplus = xlow
                    lminus = xlow -1
                    while l<(xhigh+1.6):
                        m = ylow-0.5
                        mplus = ylow
                        mminus = ylow -1
                        while m <(yhigh+1.6):
                            n = zlow-0.5
                            nplus = zlow
                            nminus = zlow-1
                            while n<(zhigh+1.6):
                                if (region_number==atlas[lplus,mplus,nplus]) or (region_number==atlas[lplus,mplus,nminus]) or (region_number==atlas[lplus,mminus,nplus]) or (region_number==atlas[lplus,mminus,nminus]) or (region_number==atlas[lminus,mplus,nplus]) or (region_number==atlas[lminus,mplus,nminus]) or (region_number==atlas[lminus,mminus,nplus]) or (region_number==atlas[lminus,mminus,nminus]):
                                    diameter = ((l-i)**2.+(m-j)**2.+(n-k)**2.)**0.5
                                    if diameter>max_diameter:
                                        max_diameter=diameter
                                n = n+1
                                nplus = nplus+1
                                nminus = nminus+1
                            m = m+1 
                            mplus = mplus+1
                            mminus = mminus+1   
                        l = l+1
                        lplus = lplus+1
                        lminus =lminus+1
                k = k+1
                kplus = kplus+1
                kminus = kminus +1
            j = j+1    
            jplus = jplus+1
            jminus = jminus +1
        i = i+1
        iplus = iplus +1
        iminus = iminus+1
    return max_diameter
    
def find_diameter(np.ndarray atlas, int region_number):
    cdef tuple d = np.where(atlas==region_number)
    cdef int xlow = np.min(d[0])-1
    cdef int xhigh = np.max(d[0])-1
    cdef int ylow = np.min(d[1])-1
    cdef int yhigh = np.max(d[1])-1
    cdef int zlow = np.min(d[2])-1
    cdef int zhigh = np.max(d[2])-1
    cdef int [:,:,:] atlas_view = atlas
    return find_diameter_fast(atlas_view,region_number, xlow, xhigh, ylow, yhigh, zlow, zhigh)
