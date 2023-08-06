import numpy as np
import cupy as cp

def search_colors(pic, colors):
    r_gpu = cp.array(pic[..., 2])
    g_gpu = cp.array(pic[..., 1])
    b_gpu = cp.array(pic[..., 0])
    return {
        tuple(y[0].tolist()): np.dstack(
            [y[1][0].get().astype(np.uint16), y[1][1].get().astype(np.uint16)]
        )
        for y in [
            (x, cp.where((b_gpu == x[0]) & (g_gpu == x[1]) & (r_gpu == x[2])))
            for x in colors
        ]
    }

