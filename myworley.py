import numpy as np
import matplotlib.pyplot as plt

def dist(grid, points):
    dx = points[:,:,0]-grid[:,:,0]
    dy = points[:,:,1]-grid[:,:,1]
    return dx*dx + dy*dy

def worley2d(shape,res,seed=0,tile=0):

    np.random.seed(seed)

    step = res/shape
    d = shape//res

    # make [res x res] grid with random point in each
    grid = np.mgrid[0:res:step, 0:res:step].transpose(1,2,0) % 1
    rand = np.random.rand(res+2,res+2,2) # + 2 gives us a buffer on each side of our texture
    points = rand.repeat(d, axis=0).repeat(d, axis=1)

    if (tile):
        points[0:d,:] = points[-2*d:-d,:]
        points[:,0:d] = points[:,-2*d:-d]
        points[-d:,:] = points[d:2*d,:]
        points[:,-d:] = points[:,d:2*d]

    p  = points[d:-d,d:-d] # point we are centered on
    n  = points[d:-d, 0:-2*d]   + [ 0,-1]
    ne = points[2*d:, 0:-2*d]   + [ 1,-1]
    e  = points[2*d:, d:-d]     + [ 1, 0]
    se = points[2*d:, 2*d:]     + [ 1, 1]
    s  = points[d:-d, 2*d:]     + [ 0, 1]
    sw = points[0:-2*d, 2*d:]   + [-1, 1]
    w  = points[0:-2*d, d:-d]   + [-1, 0]
    nw = points[0:-2*d, 0:-2*d] + [-1,-1]

    neighbors = [nw, n, ne, w, p, e, sw, s, se]
    distances = np.asarray([dist(grid,dir) for dir in neighbors]).transpose(1,2,0)

    return np.sqrt(distances.min(axis=2))

if __name__ == '__main__':

    scale = 256
    res = 8

    plt.imshow(worley2d(scale,res,seed=87), cmap='grey')
    plt.show()
