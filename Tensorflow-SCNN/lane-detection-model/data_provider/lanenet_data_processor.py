#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-11 下午4:58
# @Author  : Luo Yao
# @Site    : http://icode.baidu.com/repos/baidu/personal-code/Luoyao
# @File    : lanenet_data_processor.py
# @IDE: PyCharm Community Edition
"""
实现LaneNet的数据解析类
"""
import os.path as ops

import cv2
import numpy as np

try:
    from cv2 import cv2
except ImportError:
    pass


class DataSet(object):
    """
    实现数据集类
    """

    def __init__(self, dataset_info_file):
        """

        :param dataset_info_file:
        """
        self._gt_img_list, \
        self._gt_label_instance_list, self._gt_label_existence_list = self._init_dataset(dataset_info_file)
        self._random_dataset()
        self._next_batch_loop_count = 0

    def _init_dataset(self, dataset_info_file):
        """

        :param dataset_info_file:
        :return:
        """
        gt_img_list = []
        gt_label_instance_list = []
        gt_label_existence_list = []

        assert ops.exists(dataset_info_file), '{:s}　不存在'.format(dataset_info_file)

        with open(dataset_info_file, 'r') as file:
            for _info in file:
                info_tmp = _info.strip(' ').split()

                gt_img_list.append(info_tmp[0][1:])
                gt_label_instance_list.append(info_tmp[1][1:])
                gt_label_existence_list.append([int(info_tmp[2]), int(info_tmp[3]), int(info_tmp[4]), int(info_tmp[5])])

        return gt_img_list, gt_label_instance_list, gt_label_existence_list

    def _random_dataset(self):
        """

        :return:
        """
        assert len(self._gt_img_list) == len(self._gt_label_instance_list) == len(self._gt_label_existence_list)

        random_idx = np.random.permutation(len(self._gt_img_list))
        new_gt_img_list = []
        new_gt_label_instance_list = []
        new_gt_label_existence_list = []

        for index in random_idx:
            new_gt_img_list.append(self._gt_img_list[index])
            new_gt_label_instance_list.append(self._gt_label_instance_list[index])
            new_gt_label_existence_list.append(self._gt_label_existence_list[index])

        self._gt_img_list = new_gt_img_list
        self._gt_label_instance_list = new_gt_label_instance_list
        self._gt_label_existence_list = new_gt_label_existence_list

    def next_batch(self, batch_size):
        """

        :param batch_size:
        :return:
        """
        assert len(self._gt_label_instance_list) == len(self._gt_label_existence_list) \
               == len(self._gt_img_list)

        idx_start = batch_size * self._next_batch_loop_count
        idx_end = batch_size * self._next_batch_loop_count + batch_size

        if idx_end > len(self._gt_label_instance_list):
            self._random_dataset()
            self._next_batch_loop_count = 0
            return self.next_batch(batch_size)
        else:
            gt_img_list = self._gt_img_list[idx_start:idx_end]
            gt_label_instance_list = self._gt_label_instance_list[idx_start:idx_end]
            gt_label_existence_list = self._gt_label_existence_list[idx_start:idx_end]

            gt_imgs = []
            gt_labels_instance = []
            gt_labels_existence = []

            for gt_img_path in gt_img_list:
                gt_imgs.append(cv2.imread(gt_img_path, cv2.IMREAD_COLOR))

            for gt_label_path in gt_label_instance_list:
                label_img = cv2.imread(gt_label_path, cv2.IMREAD_UNCHANGED)
                gt_labels_instance.append(label_img)

            gt_labels_existence = gt_label_existence_list

            self._next_batch_loop_count += 1
            return gt_imgs, gt_labels_instance, gt_labels_existence


if __name__ == '__main__':
    val = DataSet('/home/houyuenan/lanenet-lane-detection/data/training_data_example/train.txt')
    a1, a2, a3 = val.next_batch(1)
    cv2.imwrite('test_binary_label.png', a2[0] * 255)
    b1, b2, b3 = val.next_batch(50)
    c1, c2, c3 = val.next_batch(50)
    dd, d2, d3 = val.next_batch(50)
