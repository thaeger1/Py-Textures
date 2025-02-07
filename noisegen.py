import matplotlib.pyplot as plt
from lib.Noise import *
import sys

args = sys.argv
assert (len(args) >= 3), 'Incorrect input format'
# requires : py file.py [noise_type] [scale] [additional args: direction or seed]

tnoise = args[1]
scale = int(args[2])

shape = 256
res = 8

lin = np.linspace(0,res,shape,endpoint=False)
x,y = np.meshgrid(lin,lin)

if tnoise == 'white':
    plt.imshow(whitenoise2d(shape), cmap='grey')
elif tnoise == 'worley':
    plt.imshow(worley2d(shape,int(res/scale),seed=87), cmap='grey')
elif tnoise == 'perlin':
    plt.imshow(perlin2d(x/scale,y/scale,seed=87), cmap='grey')
elif tnoise == 'fbm':
    oct = int(input('Octaves: '))
    freq = int(input('Init freq: '))
    # TODO: pass oct, freq to fBM
    plt.imshow(fBM2d(x/scale,y/scale,shape,seed=87), cmap='grey')
# TODO: add stripes
elif tnoise == 'stripes':
    # dir = input('Direction: ')
    plt.imshow(stripes2d(shape,res), cmap='grey')
else: assert False, 'Invalid noise type'

plt.show()

# TODO: have option (flag?) to have program print output to stdout so we can pipe together noise functions
# encode as B64, print output, pipe op, intake B64 str and decode