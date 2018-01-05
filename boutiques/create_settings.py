#!/usr/bin/env python

import os, sys, subprocess, shutil, glob
from argparse import ArgumentParser

def build_settings_file(template_file, output_file, k, vx, v_settings, a_settings, mu_settings, maxit, result_name, result_dir, batch_size):
    with open(template_file) as f:
        template_string = f.read()

    template_string = template_string.replace("__K__", k)
    template_string = template_string.replace("__VX__", vx)
    template_string = template_string.replace("__V_SETTINGS__", v_settings)
    template_string = template_string.replace("__A_SETTINGS__", a_settings)
    template_string = template_string.replace("__MU_SETTINGS__", mu_settings)
    template_string = template_string.replace("__MAXIT__", maxit)
    template_string = template_string.replace("__RESULT_NAME__", result_name)
    template_string = template_string.replace("__RESULT_DIR__", result_dir)
    template_string = template_string.replace("__BATCHSIZE__", batch_size)

    with open(output_file, 'w') as f:
        f.write(template_string)

def build_filename_json(settings):
    ## This is a destructive process, but since this is meant for a single execution, it is ok
    fileNames = glob.glob('{0}/*.nii'.format(settings.filecol))

    ### now we want to parse the filenames.json in the proper format
    ### for now, will assume that the files begin with rcXs, with X being the index of the file
    ### TO DO make more robust if the files do not have a proper naming convention
    offset = len(settings.filecol)
    ids = set([x[(offset + 5):(offset + 21)] for x in fileNames])
    print "Ids = {0}".format(ids)
    counts = {y:len([x for x in fileNames if y in x]) for y in ids}
    print "Counts = {0}".format(counts)
    jsonString = ["["]
    for k,v in counts.items():
        if v > 1:
            fileList = sorted([x for x in fileNames if k in x])
            jsonString.append("{0},\n".format(fileList))
    jsonString[-1] = jsonString[-1][:-1]
    jsonString.append("]")

    with open("filename.json","w") as f:
        f.write("".join(jsonString))    
        
def run_app(file_names, settings):
    path, fil = os.path.split(__file__)
    app_file = os.path.join(path, "runPG")

    cmdStr = "/bin/runPG {0} {1} >> out.dat".format(
                                  file_names,
                                  settings)
    #cmdStr = "cat {0}".format(settings)
    #print "CMD = {0}".format(cmdStr)
    subprocess.check_output(cmdStr,
                            shell=True, stderr=subprocess.STDOUT)
def dir_full_of_niis_exists(parser, dir_name):
    if not os.path.exists(dir_name):
        parser.error("Directory not found {0}".format(dir_name))
    niifileList = glob.glob("{0}/*.nii".format(dir_name))
    if len(niifileList) == 0:
        parser.error("Directory {0} has no nii files in it".format(dir_name))
    return dir_name
                                                 
def file_exists(parser, file_name):
    if not os.path.exists(file_name):
        parser.error("File not found: {0}".format(file_name))
    return file_name

def main(args=None):
    print "Yo"
    parser = ArgumentParser(description="A script that creates the settings file for the runPG application")
    parser.add_argument("filecol", type=lambda x: dir_full_of_niis_exists(parser, x), help='Directory in which the nii files reside')
    parser.add_argument("k", type=int,
                        help="Number of shape and appearance components. Example: 64")
    parser.add_argument("vx", type=str, help="Voxel sizes (mm - matches those of \"imported\" images). Example: [1.5 1.5 1.5]")
    parser.add_argument("v_settings", type=str, help="Registration regularisation settings. Example: [1e-05,0.01,0.2,0.025,0.05].")
    parser.add_argument("a_settings", type=str, help="Appearance regularisation settings. Example: [0.01,1,0].")
    parser.add_argument("mu_settings", type=str, help="Mean image regularisation settings. Example: [0.001,0.1,0].")
    parser.add_argument("maxit", type=int, help="Number of iterations. Example: 8.")
    parser.add_argument("result_name", type=str, help="Name of results files. Example: test.")
    parser.add_argument("result_dir", type=str, help="Name of result directory. Example: /tmp")
    parser.add_argument("batch_size", type=int, help="Batch-size (for local parallelisation). Example: 4.")

    results=parser.parse_args() if args is None else parser.parse_args(args)
    
    path, fil = os.path.split(__file__)
    template_file = os.path.join(path, "template.json")
    build_filename_json(results)
    sys.exit()
    build_settings_file(template_file, ".test.json",
                      str(results.k),
                      results.vx,
                      results.v_settings,
                      results.a_settings,
                      results.mu_settings,
                      str(results.maxit),
                      results.result_name,
                      results.result_dir,
                      str(results.batch_size))
    run_app(results.filenames,'.test.json')

if  __name__ == "__main__":
    main()
