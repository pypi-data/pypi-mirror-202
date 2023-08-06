import cv2
import numpy as np
from sklearn.cluster import KMeans


def image_clustering(image_path, n_clusters):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Преобразование изображения в формат RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Получение размерности изображения
    rows, cols = image.shape[:2]

    # Преобразование изображения в одномерный массив пикселей
    image_array = image.reshape(rows * cols, 3)

    # Кластеризация пикселей с помощью k-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(image_array)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    # Преобразование одномерного массива пикселей обратно в форму изображения
    segmented_image = cluster_centers[labels].reshape(rows, cols, 3)

    # Округление значений в центрах кластеров
    segmented_image = np.uint8(segmented_image)

    return segmented_image
