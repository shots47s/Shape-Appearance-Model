#!/bin/bash 

SPM_HOME=/usr/local/SPM12/spm12

mcc   -R '-singleCompThread,-nosplash,-nodisplay'\
      -v -w enable -m\
      -N -p ${SPM_HOME}\
      -I ${SPM_HOME}\
      -I ${SPM_HOME}/toolbox/Shoot\
      runPG
