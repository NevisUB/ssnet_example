import os, sys

flist=[]
if len(sys.argv) < 3:
    print 'Usage:',sys.argv[0],'OUTPUT_FILE','INPUT_FILE0, INPUTFILE1, ...'
    sys.exit(1)

outfile = sys.argv[1]
if os.path.isfile(outfile):
    print 'output file already present:',outfile
    sys.exit(1)
if outfile[-5:]!=".root":
    print "output file does not end with .root"
    sys.exit(1)

for argv in sys.argv:
    if argv == outfile: continue
    if not argv.endswith('.root'): continue
    flist.append(argv)

outlist=[]
ERROR=False
for plane in ['plane0','plane1','plane2']:
    try:
        print 'Processing',plane
        fname_stem = outfile.replace(".root","")
        cmd = 'python pyana_gpu.py pyana.prototxt %s %s '%(fname_stem, plane)
        for f in flist:
            cmd += '%s ' % f

        print cmd
        return_code = int(os.system(cmd))
    
        #fname = 'larcv_fcn_plane%s.root' % plane
        fname = outfile.replace(".root","_%s.root"%(plane))
        if return_code:
            sys.stderr.write('Failed with return code %d\n' % return_code)
            raise Exception

        if not os.path.isfile(fname):
            sys.stderr.write('Expected output not found: %s\n' % fname)
            raise Exception
        outlist.append(fname)

    except Exception:
        print 'Error occurred! cleaning...'
        for f in outlist:
            os.remove(f)
        ERROR=True
        break
if ERROR:
    if os.path.isfile('ssnet_input.root'):
        os.remove('ssnet_input.root')
    sys.exit(1)
outlist.append('ssnet_input.root')
cmd='hadd %s ' % outfile
print cmd
for f in outlist:
    cmd += ' %s' % f
os.system(cmd)

for f in outlist:
    os.remove(f)
sys.exit(0)
