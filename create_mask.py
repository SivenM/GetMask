"""
Создание масок изображений для unet.

Имеем 12 датасетов. В каждом из них есть директории 
аннотиций и изображений.

Для каждого изображения строим маску по точкам,
взятых из аннотации (только для classTitle: person_poly).

Маску и изображение сохрянаем в отдельные директории.
"""

from func_mask import GetMask, get_ann_path
import cv2
import os


# пути аннотаций, изображений и папок
# для будущего расположения масок и изображений
ann_dirs = ['dataset\\ds10\\ann',
            'dataset\\ds11\\ann',
            'dataset\\ds12\\ann',
            'dataset\\ds13\\ann',
            'dataset\\ds2\\ann',
            'dataset\\ds3\\ann',
            'dataset\\ds4\\ann',
            'dataset\\ds5\\ann',
            'dataset\\ds6\\ann',
            'dataset\\ds7\\ann',
            'dataset\\ds8\\ann',
            'dataset\\ds9\\ann']
orig_img_dirs = ['dataset\\ds10\\img',
                'dataset\\ds11\\img',
                'dataset\\ds12\\img',
                'dataset\\ds13\\img',
                'dataset\\ds2\\img',
                'dataset\\ds3\\img',
                'dataset\\ds4\\img',
                'dataset\\ds5\\img',
                'dataset\\ds6\\img',
                'dataset\\ds7\\img',
                'dataset\\ds8\\img',
                'dataset\\ds9\\img']
img_path = 'dataset\\img'
mask_path = 'dataset\\mask'

# Получем и сохраняем маски
gm = GetMask()

for i in range(len(orig_img_dirs)):
    images = os.listdir(orig_img_dirs[i])
    for image_name in images:
        ann_path = get_ann_path(ann_dirs[i], image_name)
        if gm.get_classTitle(ann_path) == 'person_poly':
            # изображение и соответствующая ему маска
            img = gm.get_img(orig_img_dirs[i], image_name)
            mask = gm.create_mask(ann_path)
            
            # сохранаем в дирректории
            # изображение
            cv2.imwrite(img_path + '\\' + image_name, img)
            # маску
            cv2.imwrite(mask_path + '\\' + image_name, mask)