# How to install?

First time configuration:
```
git clone https://github.com/NevisUB/ssnet_example
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
First, set up
```
(log in)
> cd WHERE_YOU_PUT_THIS_REPO
> source sw/setup.sh
```
We will use one version of trained network. The script we will use (```run_ssnet.py```) requires trained networks' weights to exist in the same directory. So let's make symbolic links there.
```
ln -s /data/drinkingkazu/UBDeconvNet/dlmc_mcc8_ssnet_v4/segmentation_pixelwise_ikey_plane0_iter_75500.caffemodel
ln -s /data/drinkingkazu/UBDeconvNet/dlmc_mcc8_ssnet_v4/segmentation_pixelwise_ikey_plane1_iter_65500.caffemodel 
ln -s /data/drinkingkazu/UBDeconvNet/dlmc_mcc8_ssnet_v4/segmentation_pixelwise_ikey_plane2_iter_68000.caffemodel 
```
... where three symbolic links correspond to a stored weight file per plane (you see plane0, plane1, plane2 in file name).

Next let's make a sample input root file with just 5 events. We just use one of many handy example files @ wu to do this.
```
run_processor copy.cfg /stage2/drinkingkazu/march23/intrinsic_nue/out_supera/larcv_0000_0099.root
```

Now we are ready to try out
```
python run_ssnet.py out.root sample.root
```
... where ```out.root``` is the output file name and ```sample.root``` is the input (symbolic link) file.
