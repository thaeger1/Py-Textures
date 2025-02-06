import numpy as np

def normalize(arrIn):
    input_max = np.max(arrIn)
    input_min = np.min(arrIn)
    # maps from [input min, input max] to [0,1]
    return (arrIn - input_min) / (input_max - input_min)

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def grad(hash,x,y):
    vec = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vec[hash % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y

def lerp(a,b,x):
    return a + x*(b-a)

def dist(grid, points):
    dx = points[:,:,0]-grid[:,:,0]
    dy = points[:,:,1]-grid[:,:,1]
    return dx*dx + dy*dy

### NOISE FUNCTIONS

# standard white noise
def whitenoise2d(shape,seed=0):
    np.random.seed(seed)
    return normalize(np.random.rand(shape,shape))

# perlin noise based on ken perlin's original implementation
def perlin2d(x,y,seed):
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()

    xi, yi = x.astype(int), y.astype(int)
    xf, yf = x - xi, y - yi

    u, v = fade(xf), fade(yf)

    dot_aa = grad(p[ p[xi] + yi     ], xf  , yf  )
    dot_ab = grad(p[ p[xi] + yi+1   ], xf  , yf-1)
    dot_ba = grad(p[ p[xi+1] + yi   ], xf-1, yf  )
    dot_bb = grad(p[ p[xi+1] + yi+1 ], xf-1, yf-1)

    x1 = lerp(dot_aa, dot_ba, u)
    x2 = lerp(dot_ab, dot_bb, u)
    y1 = lerp(x1, x2, v)

    return normalize(y1)

# cellular noise, TODO: add voronoi flag
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

    return normalize(np.sqrt(distances.min(axis=2)))

def fBM2d(x,y,shape,seed=0):
    octaves = 3
    amp = 1
    freq = 1
    fBM = np.empty((shape,shape))
    for i in range(octaves):
        fBM += amp * perlin2d(x*freq,y*freq,seed)
        amp /= 2.
        freq *= 2.
    return normalize(fBM)

### sources:
# normalize
# - https://stackoverflow.com/questions/5731863/mapping-a-numeric-range-onto-another
# perlin
# - https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy
# - https://adrianb.io/2014/08/09/perlinnoise.html