# Detects colors in images up to 8 times as fast as NumPy  

### pip install locate-pixelcolor-cupy
If you haven't installed cupy yet, I recommend you installing it using conda:
conda install -c conda-forge cupy

#### Tested against Windows 10 / Python 3.10 / Anaconda



### Usage

```python

import numpy as np
import cv2
from locate_pixelcolor_cupy import search_colors
# 4525 x 6623 x 3 picture https://www.pexels.com/pt-br/foto/foto-da-raposa-sentada-no-chao-2295744/
picx = r"C:\Users\hansc\Downloads\pexels-alex-andrews-2295744.jpg"
pic = cv2.imread(picx)
colors0 = np.array([[255, 255, 255]], dtype=np.uint8)
resus0 = search_colors(pic=pic, colors=colors0)
colors1 = np.array(
    [
        (66, 71, 69),
        (62, 67, 65),
        (144, 155, 153),
        (52, 57, 55),
        (127, 138, 136),
        (53, 58, 56),
        (51, 56, 54),
        (32, 27, 18),
        (24, 17, 8),
    ],
    dtype=np.uint8,
)
resus1 = search_colors(pic=pic, colors=colors1)
####################################################################
%timeit resus0 = search_colors(pic=pic, colors=colors0)
78.2 ms ± 1.29 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

b,g,r = pic[...,0],pic[...,1],pic[...,2]
%timeit np.where(((b==255)&(g==255)&(r==255)))
150 ms ± 209 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
####################################################################
%timeit resus1 = search_colors(pic=pic, colors=colors1)
139 ms ± 9.78 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit np.where(((b==66)&(g==71)&(r==69))|((b==62)&(g==67)&(r==65))|((b==144)&(g==155)&(r==153))|((b==52)&(g==57)&(r==55))|((b==127)&(g==138)&(r==136))|((b==53)&(g==58)&(r==56))|((b==51)&(g==56)&(r==54))|((b==32)&(g==27)&(r==18))|((b==24)&(g==17)&(r==8)))
1 s ± 16.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
####################################################################
```
