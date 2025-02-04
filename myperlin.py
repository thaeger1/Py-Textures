import numpy as np
import matplotlib.pyplot as plt

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def grad(hash,x,y):
    vec = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vec[hash % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y

def lerp(a,b,x):
    return a + x*(b-a)

def perlin2d(x,y,seed):

    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()

    xi, yi = x.astype(int), y.astype(int) # try with / without &255
    xf, yf = x - xi, y - yi

    u, v = fade(xf), fade(yf)

    dot_aa = grad(p[ p[xi] + yi     ], xf  , yf  )
    dot_ab = grad(p[ p[xi] + yi+1   ], xf  , yf-1)
    dot_ba = grad(p[ p[xi+1] + yi   ], xf-1, yf  )
    dot_bb = grad(p[ p[xi+1] + yi+1 ], xf-1, yf-1)

    x1 = lerp(dot_aa, dot_ba, u)
    x2 = lerp(dot_ab, dot_bb, u)
    y1 = lerp(x1, x2, v)

    return y1

if __name__ == '__main__':
    print('hi')

    lin = np.linspace(0,5,512,endpoint=False)
    x,y = np.meshgrid(lin,lin)

    plt.imshow(perlin2d(x,y,seed=87), cmap='grey')
    plt.show()

# src:
# https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy
# https://adrianb.io/2014/08/09/perlinnoise.html
