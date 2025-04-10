def test_basic():
    import numpy as np
    from skimage import color, data
    from skimage.util import view_as_blocks

    # from skimage import io
    # io.use_plugin('matplotlib', 'imread')

    # get astronaut from skimage.data in grayscale
    a = data.astronaut()
    l = color.rgb2gray(a)#.astype(np.float32)
    assert l.size == 262144
    assert l.shape == (512, 512)

    # size of blocks
    block_shape = (4, 4)
    # see astronaut as a matrix of blocks (of shape block_shape)
    view = view_as_blocks(l, block_shape)
    assert view.shape == (128, 128, 4, 4)

    from skimage.filters import threshold_otsu

    to = threshold_otsu(l)
    assert to.hex() == "0x1.8e00000000000p-2"
    from skimage.color import rgb2gray
    from skimage.data import astronaut
    from skimage.filters import sobel
    from skimage.segmentation import felzenszwalb, quickshift, slic, watershed
    from skimage.util import img_as_float

    img = img_as_float(astronaut()[::2, ::2])

    segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)

    segments_slic = slic(img, n_segments=250, compactness=10, sigma=1)

    segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)
    grayscale = rgb2gray(img)
    gradient = sobel(grayscale)
    segments_watershed = watershed(gradient, markers=250, compactness=0.001)
    assert len(np.unique(segments_fz)) == 194
    assert len(np.unique(segments_slic)) == 196
    assert len(np.unique(segments_quick)) == 695
    assert len(np.unique(segments_watershed)) == 256
