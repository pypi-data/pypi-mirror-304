from function import convert_mcd_png,read_parameters_convert


path_mcd,path_png,roi_exclude,marker_exclude=read_parameters_convert()
convert_mcd_png(path_mcd,roi_exclude,marker_exclude,path_png)