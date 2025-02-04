import numpy as np
import matplotlib.pyplot as plt

def dist(grid, points):
    dx = points[:,:,0]-grid[:,:,0]
    dy = points[:,:,1]-grid[:,:,1]
    return dx*dx + dy*dy

def worley2d(shape,res,seed=0):

    np.random.seed(seed)

    step = res/shape
    d = shape//res

    # make [res x res] grid with random point in each
    grid = np.mgrid[0:res:step, 0:res:step].transpose(1,2,0) % 1
    rand = np.random.rand(res+2,res+2,2) # + 2 gives us a buffer on each side of our texture
    points = rand.repeat(d, axis=0).repeat(d, axis=1)

    repeat = 1
    if (repeat):
        print('hi')

    p  = points[d:-d,d:-d] # point we are centered on
    n  = points[d:-d, 0:-2*d]   + [0,-1]
    ne = points[2*d:, 0:-2*d]   + [1,-1]
    e  = points[2*d:, d:-d]     + [1,0]
    se = points[2*d:, 2*d:]     + [1,1]
    s  = points[d:-d, 2*d:]     + [0,1]
    sw = points[0:-2*d, 2*d:]   + [-1,1]
    w  = points[0:-2*d, d:-d]   + [-1,0]
    nw = points[0:-2*d, 0:-2*d] + [-1,-1]

    neighbors = [nw, n, ne, w, p, e, sw, s, se]
    # neighbors = [p]

    distances = np.asarray([ ( dist(grid,dir) ) for dir in neighbors]).transpose(1,2,0)
    # TODO: currently checking distance between

    # print(distances.shape)

    return np.sqrt(distances.min(axis=2))

    # dx = grid[:,:,0] - p[:,:,0] # get distance between xf,yf and nearest point
    # dy = grid[:,:,1] - p[:,:,1]
    # data = np.sqrt(dx*dx + dy*dy) # calc dist
    # return data

if __name__ == '__main__':

    lin = np.linspace(0,5,100,endpoint=False)
    x,y = np.meshgrid(lin,lin)

    scale = 256
    res = 8

    plt.imshow(worley2d(scale,res,seed=87), cmap='grey')
    plt.show()

    # print(np.min(data))
    # print(np.max(data))

# src:
# https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy
# https://adrianb.io/2014/08/09/perlinnoise.html