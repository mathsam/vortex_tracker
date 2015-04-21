
import subprocess
import os

fgdir = './fg/'
bginfo = './negatives.txt'

fg_files = os.listdir(fgdir)

for i, i_file in enumerate(fg_files):
    """
    subprocess.call(["opencv_createsamples", "-img " + fgdir + i_file,
                     "-bg " + bginfo, 
                     "-info annotation%d.lst" %i,
                     "-pngoutput",
                     "-maxxangle 0",
                     "-maxyangle 0",
                     "-maxzangle 1"])
    """
    os.system("opencv_createsamples " + "-img " + fgdir + i_file + " "
              + "-bg " + bginfo + " "
              + "-info annotation%d.lst" %i + " "
              + "-pngoutput "
              + "-maxxangle 0 -maxyangle 0 -maxzangle 1 -h 20 -w 20")
    os.system("mv *jpg ./tmp")
    current_files = os.listdir("./tmp")
    for which_current_file in current_files:
        os.system("mv ./tmp/%s ./tmp/file%d_%s" %(which_current_file,
                                                  i,
                                                  which_current_file))
    add_prefix_cmd = """awk '{ printf "./processed/file%d_"; print }' %s >>%s""" %(i, "annotation%d.lst" %i,    
                                                                      "total.lst")
    os.system(add_prefix_cmd)
    os.system("mv ./tmp/*jpg ./processed")
    
os.system('opencv_createsamples -info total.lst -bg bg/bg.txt -vec total.vec -h 24 -w 24')