from .searchcolorsnumba import search_colors as search_colors2
import numpy as np
def search_colors(pic, colors):
    if not isinstance(colors,np.ndarray):
        colors = np.array(colors,dtype=np.uint8)

    r = np.ascontiguousarray(pic[..., 0].flatten())
    g = np.ascontiguousarray(pic[..., 1].flatten())
    b = np.ascontiguousarray(pic[..., 2].flatten())
    divider =np.uint16(pic.shape[1])
    return search_colors2(r,g,b,colors,divider)
