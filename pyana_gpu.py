import matplotlib 
matplotlib.use('Agg')
import os,sys,time
os.environ['GLOG_minloglevel'] = '2' # set message level to warning 

# Check GPU availability before heavy lib loading
from choose_gpu import pick_gpu
GPUMEM = 5000
#GPUID = pick_gpu(mem_min=GPUMEM,caffe_gpuid=True)
#if GPUID < 0:
#    sys.stderr.write('No GPU available with memory > %d\n' % GPUMEM)
#    sys.stderr.flush()
#    sys.exit(1)
GPUID = 0

import numpy as np
import ROOT as rt
rt.gSystem.Load("libGeo2D_Core.so")
from ROOT import larcv
import matplotlib.pyplot as plt
from caffe.image2d_data_layer import Image2DLayer as il
import caffe
#caffe.set_mode_cpu()
caffe.set_device(GPUID)

print "MODULES LOADED"

PROTO  = None
MODEL  = None
OUTCFG = 'pyana_out.cfg'
MASK_ADC = True
MASK_THRESH = 10.
SKIP_CH = [0]

MODELMAP={'plane0' : 'uresnet64_plane0_iter_8000.caffemodel.h5',
          'plane1' : 'uresnet64_plane1_iter_8000.caffemodel.h5',
          'plane2' : 'uresnet64_plane2_iter_8000.caffemodel.h5'}
PLANEID=''
MODEL=''
OUTFILESTEM='larcv_fcn'

flist=rt.std.vector('string')()
for argv in sys.argv:
    if argv.find('.prototxt') >= 0:
        PROTO = argv
    elif argv.endswith('.root'):
        flist.push_back(argv)
    elif argv == 'plane0':
        PLANEID=argv
        MODEL=MODELMAP['plane0']
    elif argv == 'plane1':
        PLANEID=argv
        MODEL=MODELMAP['plane1']
    elif argv == 'plane2':
        PLANEID=argv
        MODEL=MODELMAP['plane2']
    else:
        OUTFILESTEM=argv

if not PLANEID or not MODEL:
    print 'Valid plane id not provided!'
    raise Exception()

INCFG  = 'pyana_in_%s.cfg' % PLANEID
print "Using input config:",INCFG
debug = 'debug' in sys.argv
print "Out file stem: ",OUTFILESTEM

out_proc = larcv.ProcessDriver('OutputProcessDriver')
out_proc.configure(OUTCFG)
py_image_maker = out_proc.process_ptr(out_proc.process_id("PyImageStitcher"))
py_image_maker.set_producer_name('uburn_%s' % PLANEID)
out_proc.override_output_file('%s_%s.root'%(OUTFILESTEM,PLANEID) )
out_proc.initialize()

in_proc = larcv.ProcessDriver('InputProcessDriver')
in_proc.configure(INCFG)
in_proc.override_input_file(flist)
in_proc.initialize()
cropper = in_proc.process_ptr(in_proc.process_id("MultiROICropper"))
il._rows = cropper.target_rows()
il._cols = cropper.target_cols()

net = caffe.Net( PROTO, MODEL, caffe.TEST)

num_events = in_proc.io().get_n_entries()

print
print 'Total number of events:',num_events
print

event_counter = 0
stop_counter  = None

num_event_with_roi = 0.
num_roi = 0.

while event_counter < num_events:
    in_proc.process_entry(event_counter,True)

    img_v = cropper.get_cropped_image()
    sys.stdout.write('Processing entry %d/%d w/ %d ROIs        \r' % (event_counter,num_events,img_v.size()))
    sys.stdout.flush()
    
    num_roi += img_v.size()
    if img_v.size() > 0: num_event_with_roi+=1
    else: 
        event_counter += 1
        continue

    for roi_idx in xrange(img_v.size()):

        il._image2d = img_v[roi_idx]
        net.forward()

        adcimg  = net.blobs["data"].data
        softmax = net.blobs["softmax"].data

        if debug:
            adcpng = plt.imshow(adcimg[0][0])
            adcpng.write_png('entry%04d_%04d.png' % (event_counter,roi_idx))

        img_array = softmax[0]
        out_ch = 0
        for ch in xrange(len(img_array)):
            if ch in SKIP_CH: continue

            img = img_array[ch]
            if MASK_ADC:
                img *= (adcimg[0][0] > MASK_THRESH)

            #py_image_maker.append_ndarray_meta(img.transpose(),img_v[roi_idx].meta(),out_ch)
            py_image_maker.append_ndarray_meta(img,img_v[roi_idx].meta(),out_ch)
            out_ch += 1
            
            if debug:
                png=plt.imshow(img)
                png.write_png('entry%06d_ch%02d.png' % ((ibatch * BATCH_CTR),ch))

    event_id = in_proc.io().last_event_id()
    #event_id = in_proc.io().event_id()
    (run,subrun,event) = (event_id.run(), event_id.subrun(), event_id.event())
    print 'run',run,'subrun',subrun,'event',event

    py_image_maker.set_id(run, subrun, event)
    out_proc.process_entry()
    event_counter += 1

    if stop_counter and event_counter >= stop_counter:
        break

frac_event_with_roi = (int(float(num_event_with_roi)/float(event_counter)*10000.))/100.
average_num_roi_total = num_roi / float(event_counter)
average_num_roi = num_roi / float(num_event_with_roi)

print
print '# events processed:',event_counter
print '# event w/ ROI:    ',num_event_with_roi,'(',frac_event_with_roi,'% )'
print '# ROI processed:   ',num_roi,'(',average_num_roi,'ROI per event, or total average',average_num_roi_total,')'
print

out_proc.finalize()
in_proc.finalize()
sys.exit(0)
