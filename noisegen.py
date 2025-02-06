import matplotlib.pyplot as plt
from lib.Noise import *
import sys

args = sys.argv
assert (len(args) >= 3), 'Incorrect input format'

tnoise = args[1]
scale = int(args[2])
if len(args) > 3:
    oct = args[3]
    freq = args[4]

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
    plt.imshow(fBM2d(x/scale,y/scale,shape,seed=87), cmap='grey')
# TODO: add stripes
elif tnoise == 'stripes':
    pass
else: assert False, 'Invalid noise type'

plt.show()