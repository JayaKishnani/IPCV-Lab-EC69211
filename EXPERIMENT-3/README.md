# EXPERIMENT-3 Frequency Domain Transformation

1. In the first question we analyzed the frequency domain representation of the image. 

- The magnitude spectrum of the image represents the distribution of frequency components in the image. High-magnitude regions in the spectrum correspond to edges, textures, and other fine details in the image. Low-magnitude regions correspond to smoother and low-frequency regions in the image.

- The phase spectrum of an image tells us about the orientation of the image. Edges and lines in the image are characterized by abrupt phase changes. The direction of these changes can provide insights into the orientation of edges.

2. In the second question, the operations described are a series of Fourier domain manipulations. Multiplying by (-1)^(x + y) effectively shifts the image's frequency spectrum. The complex conjugate ensures that the iFFT results in a real-valued image, and finally, multiplying by (-1)^(x + y) again shifts the spectrum back.

    
