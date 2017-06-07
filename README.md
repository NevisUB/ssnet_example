# How to install?

First time configuration:
```
git clone https://github.com/LArbys/ssnet_example
cd ssnet_example/sw
source setup.sh
```

Above "source setup.sh" pulls repositories and builds.
caffe and larcv has a particular order (and repeats) of builds, so please follow this procedure of build.
You can look at setup.sh if you are curious of this "order and repeats": it's ultimately something I should fix...

From 2nd time (like you logged out and logged in again), just do
```
source setup.sh
```
under the "sw" directory. This won't attempt a build and you will be ready to use a software.

# How to run?

You need a tagger input (holds original image data) and output (holds tagger's data).

```
python run_ssnet.py out.root FILE1 [FILE2 ...]
```
where ```FILE1```, ```FILE2```, etc. are all input files.
```out.root``` is going to be the name of the output file.
If the same named file already exsits it halt the execution and exits.


# Particular example on Wu

```
(log in)
> cd WHERE_YOU_PUT_THIS_REPO
> source sw/setup.sh
> python run_ssnet.py out.root /stage2/drinkingkazu/march23/intrinsic_nue/out_supera/larcv_0000_0099.root /stage2/drinkingkazu/march23/intrinsic_nue/out_tagger/output_tagger_larcv_0000_0099.root
```
... where 
```
/stage2/drinkingkazu/march23/intrinsic_nue/out_supera/larcv_0000_0099.root
```
is supera output = tagger input, and
```
/stage2/drinkingkazu/march23/intrinsic_nue/out_tagger/output_tagger_larcv_0000_0099.root
```
is tagger output file.
