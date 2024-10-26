from readimc import MCDFile, TXTFile
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

def normalize(img):
  img=(img-np.min(img))/(np.max(img)-np.min(img))
  return img
def normalize_255(img):
  img=((img-np.min(img))/(np.max(img)-np.min(img)))*255
  return img

def arcsinh_std_thresh(img,thresh,cofactor,kernel):
  img_sin=np.arcsinh(img*cofactor)
  img_med=cv2.medianBlur(img_sin,5)
  img_std=(img_med-np.mean(img_med))/np.std(img_med)
  img_thresh=np.where(img_std<thresh,0,img_sin)
  return img_thresh

def read_parameters_convert(path="./arg_convert.txt"):
    with open(path,"r") as f:
        for line in f.readlines():
            line=line.rstrip("\n")
            if line[:8]=="path_mcd":
                path_mcd=line[9:]
            if line[:8]=="path_png":
                path_png=line[9:]
            if line[:11]=="roi_exclude":
                roi_exclude=line[12:].split(",")
            if line[:14]=="marker_exclude":
                marker_exclude=line[15:].split(",")
    return path_mcd,path_png,roi_exclude,marker_exclude
    
def convert_mcd_png(path="./arg_convert.txt"):
    
    path_mcd,path,roi_exclude,marker_exclude=read_parameters_convert(path)
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for file in os.listdir(mcd_file):
        print("** "+file+" **")
        if os.path.isdir(path+"/"+file)==False:
            os.mkdir(path+"/"+file)
        with MCDFile(mcd_file+"/"+file) as f:
            slide = f.slides[0]
            panorama = slide.panoramas[0]
            for acq in range(len(slide.acquisitions)):
                acquisition = slide.acquisitions[acq]
                roi=acquisition.description
                if roi not in roi_exclude:
                    print("ROI: "+roi)
                    if os.path.isdir(path+"/"+file+"/"+acquisition.description)==False:
                         os.mkdir(path+"/"+file+"/"+acquisition.description)
                    try:
                        img = f.read_acquisition(acquisition)
                        list_target=acquisition.channel_labels
                        dico_target={v:i for i,v in enumerate(list_target)}
                        for i in range(len(list_target)):
                            if list_target[i] not in marker_exclude:
                                img_marker=img[dico_target[list_target[i]],:,:]
                                cv2.imwrite(path+"/"+file+"/"+acquisition.description+"/"+list_target[i]+".png",img_marker)
                               
                    except:
                        print("Erreure: "+roi)
                

def visualize_roi(cofactor=1000,thresh=2,kernel=5,path="./Lames_arcsinh"):
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for lame in os.listdir("./Lames_raw"):
        print("** Lame: "+lame+" **")
        if os.path.isdir(path+"/"+lame)==False:
            os.mkdir(path+"/"+lame)
        for roi in os.listdir("./Lames_raw/"+lame):
            print("    ROI: "+roi)
            if os.path.isdir(path+"/"+lame+"/"+roi)==False:
                os.mkdir(path+"/"+lame+"/"+roi)
            for marker in os.listdir("./Lames_raw/"+lame+"/"+roi):
                img=plt.imread("./Lames_raw/"+lame+"/"+roi+"/"+marker)
                img=arcsinh_std_thresh(img,thresh,cofactor,kernel)
                cv2.imwrite(path+"/"+lame+"/"+roi+"/"+marker,normalize_255(img))

