from myperlin import perlin2d as perlin
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    shape = 256
    lin = np.linspace(0,5,shape,endpoint=False)
    x,y = np.meshgrid(lin,lin)

    octaves = 3
    amp = 1
    freq = 1

    dout = np.empty((shape,shape))

    mmax = 0
    for i in range(octaves):
        dout += amp * perlin(x*freq,y*freq,seed=0)
        amp /= 2.
        freq *= 2.
        mmax += amp
    
    dout /= mmax
    plt.imshow(dout, cmap='grey')
    plt.show()
