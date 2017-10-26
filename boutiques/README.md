# Boutiques package

This folder contains the files used to creates a (Boutiques)[http://github.com/boutiques/boutiques] package for the pipeline.

* Dockerfile: file used to build a Docker container for the pipeline. Requires that the pipeline is compiled with `mcc`. Compilation can be done with `../compile.sh`.
* runPG.json: the Boutiques descriptor, used to integrate the pipeline in platforms supporting Boutiques (such as (CBRAIN)[http://github.com/aces/cbrain]).
* create_settings.py: a script that creates `settings.json` from parameters passed on the command line.
* template.json: template JSON file for `settings.json`, used by `create_settings.py`. 
