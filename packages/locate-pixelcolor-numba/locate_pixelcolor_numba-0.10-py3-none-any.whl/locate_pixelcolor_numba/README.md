# RGB search with numba - 2-3 x faster than numpy 

### pip install locate-pixelcolor-numba


### Important!
This is a compiled .pyd file (Numba AOT), if you can't import it, run the following code to generate a new pyd file, and replace it with the old .pyd file.


```python
from numba_aot_compiler import compnumba #pip install numba-aot-compiler
import numpy as np
from numba import uint8, uint16


def search_colors(r, g, b, rgbs, divider):
    res = np.zeros(b.shape, dtype=np.uint16)
    res2 = np.zeros(b.shape, dtype=np.uint16)
    zaehler = 0
    for rgb in rgbs:
        rr, gg, bb = rgb
        for i in range(r.shape[0]):
            if r[i] == rr:
                if g[i] == gg:
                    if b[i] == bb:
                        dvquot, dvrem = divmod(i, divider)
                        res[zaehler] = dvquot
                        res2[zaehler] = dvrem
                        zaehler = zaehler + 1
    results = np.dstack((res[:zaehler], res2[:zaehler]))
    return results


compi2 = compnumba(
    fu=search_colors,
    funcname="search_colors",
    file="searchcolorsnumba",
    folder="locate_pixelcolor_numba",
    signature=(uint8[:], uint8[:], uint8[:], uint8[:, :], uint16),
    parallel=True,
    fastmath=True,
    nogil=True,
)
```

### How to use it

```python
from locate_pixelcolor_numba import search_colors
import cv2
import time
import numpy as np
pic = cv2.imread(r"pexels-alex-andrews-2295744.jpg") # https://www.pexels.com/pt-br/foto/foto-da-raposa-sentada-no-chao-2295744/
colors = np.array([(66,  71,  69),(62,  67,  65),(144, 155, 153),(52,  57,  55),(127, 138, 136),(53,  58,  56),(51,  56,  54),(32,  27,  18),(24,  17,   8),],dtype=np.uint8)
search_colors(pic,colors)
Out[2]: 
array([[[   0, 4522],
        [   3, 4522],
        [   3, 4523],
        ...,
        [6622, 4522],
        [6622, 4523],
        [6622, 4524]]], dtype=uint16)
%timeit search_colors(pic,colors)
413 ms ± 1.22 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# More benchmarks: https://github.com/hansalemaos/locate_pixelcolor_cpp

```
