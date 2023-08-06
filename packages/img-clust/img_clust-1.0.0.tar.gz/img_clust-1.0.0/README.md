# Image Clustering using K-Means Algorithm

This package provides an easy-to-use function for clustering pixels in an image using the K-Means algorithm. It requires the OpenCV, Numpy, and Scikit-learn libraries.

## Installation

You can install this package using pip: 

```python
pip install img_clust 
```

## Usage

```python
from img_clust import image_clustering

# Load and cluster the image with 5 clusters
segmented_image = image_clustering('path/to/image.jpg', 5)

# Display the segmented image
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey()
```

The `image_clustering` function takes two arguments: the path to the image file and the desired number of clusters.

## License 

MIT.