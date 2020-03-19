"""
функции и классы для создания маски
"""

import json
import cv2
import numpy as np
import os

class AnnData():
    """класс для получения данных из аннотации"""
    def get_anndata(self, ann_path):
        """Функция возвращает данные из аннотации"""
       
        with open(ann_path) as f:
            ann_data = json.load(f)
        return ann_data

    def get_h_and_w(self, ann_data):
        """Функция возвращает размеры изображения"""
        
        for i, j in ann_data.items():
            if i == 'size':
                size = j
        for i, j in size.items():
            if i == 'height':
                height = j
            else:
                width = j
        return height, width

    def get_exterior(self, ann_data):
        """Функция возвращает точки, по которым строится маска"""
        
        for i, j in ann_data.items():
            if i == 'objects':
                objects = j
        for i, j in objects[0].items():
            if i == 'points':
                points = j
        polygon = points['exterior']
        return polygon

    def get_classTitle(self, ann_data):
        """Функция возвращает класс маски"""
        for i, j in ann_data.items():
            if i == 'objects':
                objects = j
        for i, j in objects[0].items():
            if i == 'classTitle':
                classTitle = j
        return classTitle


class GetMask(AnnData):
    """Класс создает маску"""
    def create_mask(self, ann_path=''):
        """Функция создает маску. На вход подается path картинки"""
        
        # данные аннотации
        ann_data = super().get_anndata(ann_path)
       
        # точки
        exterior = super().get_exterior(ann_data)
        exterior = np.asarray(exterior)
        exterior = exterior.reshape((-1,1,2))
        
        #размеры картинки
        height, width = super().get_h_and_w(ann_data)

        # строим маску
        blank_image = np.zeros((height,width,1), np.uint8)
        mask = cv2.fillPoly(blank_image, [exterior], 255)
        return mask

    def get_classTitle(self, ann_path=''):
        """"Функция возвращает класс маски"""
        ann_data = super().get_anndata(ann_path)
        classTitle = super().get_classTitle(ann_data)
        return classTitle

    def get_img(self, img_path='', img_name=''):
        """Возращает изображение"""
        img_path = os.path.join(img_path, img_name)
        img = cv2.imread(img_path) 
        return img

def get_ann_path(ann_dir='',img_name=''):
    """
    Функция возвращает путь аннотации картинки,
    которую подаем на вход
    """
    ann_path = os.path.join(ann_dir, '{}.json'.format(img_name))
    return ann_path
