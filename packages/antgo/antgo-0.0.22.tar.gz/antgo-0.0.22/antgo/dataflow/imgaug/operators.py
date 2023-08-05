# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# function:
#    operators to process sample,
#    eg: decode/resize/crop image

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

try:
    from collections.abc import Sequence
except Exception:
    from collections import Sequence

from numbers import Number

import uuid
import logging
import random
import math
import numpy as np
import os
import time
from antgo.dataflow.core import *
from antgo.utils import logger
import cv2
from PIL import Image, ImageEnhance, ImageDraw
from .functional import *
from antgo.dataflow.vis import *
from io import StringIO, BytesIO
import copy

from .op_helper import (satisfy_sample_constraint, filter_and_process,
                        generate_sample_bbox, clip_bbox, data_anchor_sampling,
                        satisfy_sample_constraint_coverage, crop_image_sampling,
                        generate_sample_bbox_square, bbox_area_sampling,
                        is_poly, gaussian_radius, draw_gaussian)


class BboxError(ValueError):
    pass


class ImageError(ValueError):
    pass


class BaseOperator(Node):
    def __init__(self, name=None, inputs=None):
        super(BaseOperator, self).__init__(name=name, action=self.action, inputs=inputs)
        if name is None:
            name = self.__class__.__name__
        self._id = name + '_' + str(uuid.uuid4())[-6:]

    def __call__(self, sample, context=None):
        """ Process a sample.
        Args:
            sample (dict): a dict of sample, eg: {'image':xx, 'label': xxx}
            context (dict): info about this sample processing
        Returns:
            result (dict): a processed sample
        """
        return sample

    def __str__(self):
        return str(self._id)

    def action(self, *args, **kwargs):
        assert (len(args) == 1)
        image, sample = args[0] if type(args[0]) == tuple or type(args[0]) == list else (args[0], {})
        sample['image'] = image
        sample = self.__call__(sample)

        image = sample['image']
        sample.pop('image')
        return image, sample


# FINISH FIX
class DecodeImage(BaseOperator):
    def __init__(self, to_rgb=True, with_mixup=False, with_cutmix=False, backend="cv", inputs=None):
        """ Transform the image data to numpy format.
        Args:
            to_rgb (bool): whether to convert BGR to RGB
            with_mixup (bool): whether or not to mixup image and gt_bbbox/gt_score
            with_cutmix (bool): whether or not to cutmix image and gt_bbbox/gt_score
        """

        super(DecodeImage, self).__init__(inputs=inputs)
        self.to_rgb = to_rgb
        self.with_mixup = with_mixup
        self.with_cutmix = with_cutmix
        if not isinstance(self.to_rgb, bool):
            raise TypeError("{}: input type is invalid.".format(self))
        if not isinstance(self.with_mixup, bool):
            raise TypeError("{}: input type is invalid.".format(self))
        self.backend = backend # cv,pil
        assert(self.backend.lower() in ['cv', 'pil'])

    def __call__(self, sample, context=None):
        """ load image if 'image_file' field is not empty but 'image' is"""
        if 'image' not in sample or sample['image'] is None:
            with open(sample['image_file'], 'rb') as f:
                sample['image'] = f.read()

        im = sample['image']
        if self.backend.lower() == 'cv':
            data = np.frombuffer(im, dtype='uint8')
            im = cv2.imdecode(data, 1)  # BGR mode, but need RGB mode
            if self.to_rgb:
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)               
        else:
            im = Image.open(BytesIO(im))
        
        sample['image'] = im
        if 'height' not in sample:
            sample['height'] = im.shape[0]
        elif sample['height'] != im.shape[0]:
            # logger.warn(
            #     "The actual image height: {} is not equal to the "
            #     "height: {} in annotation, and update sample['h'] by actual "
            #     "image height.".format(im.shape[0], sample['h']))
            sample['height'] = im.shape[0]
        if 'width' not in sample:
            sample['width'] = im.shape[1]
        elif sample['width'] != im.shape[1]:
            # logger.warn(
            #     "The actual image width: {} is not equal to the "
            #     "width: {} in annotation, and update sample['w'] by actual "
            #     "image width.".format(im.shape[1], sample['w']))
            sample['width'] = im.shape[1]

        # make default im_info with [h, w]
        if 'image_meta' not in sample:
            sample['image_meta'] = {}
        sample['image_meta']['image_shape'] = (im.shape[0], im.shape[1])
            
        # decode mixup image
        if self.with_mixup and 'mixup' in sample:
            self.__call__(sample['mixup'], context)

        # decode cutmix image
        if self.with_cutmix and 'cutmix' in sample:
            self.__call__(sample['cutmix'], context)

        # decode semantic label 
        if 'semantic' in sample.keys():
            if self.backend.lower() == 'cv':
                data = np.frombuffer(sample['semantic'], dtype='uint8')
                sem = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)  # BGR mode, but need RGB mode
            else:
                im = Image.open(BytesIO(im))
            sample['semantic'] = sem

        return sample


class Meta(BaseOperator):
    def __init__(self, 
                 keys=[],
                 with_sample_shape=False, 
                 with_sample_file=False, 
                 with_sample_id=False, 
                 with_sample_tag=False):
        self.keys = keys
        self.with_sample_shape = with_sample_shape
        self.with_sample_file = with_sample_file
        self.with_sample_id = with_sample_id
        self.with_sample_tag = with_sample_tag

    def __call__(self, sample, context=None):
        if 'image_meta' not in sample:
            sample['image_meta'] = {}

        for key in self.keys:
            sample['image_meta'][key] = sample[key]

        if self.with_sample_shape:
            sample['image_meta']['image_shape'] = (sample['image'].shape[0], sample['image'].shape[1])

        if self.with_sample_file:
            sample['image_meta']['image_file'] = ''

        if self.with_sample_id:
            sample['image_meta']['id'] = ''

        if self.with_sample_tag:
            sample['image_meta']['tag'] = ''
        return sample


# FINISH FIX
class KeepRatio(BaseOperator):
    def __init__(self, aspect_ratio=1, focus_on_objects=False,inputs=None):
        """ Transform the image data to numpy format.

        Args:
            to_rgb (bool): whether to convert BGR to RGB
            with_mixup (bool): whether or not to mixup image and gt_bbbox/gt_score
        """

        super(KeepRatio, self).__init__(inputs=inputs)
        self.aspect_ratio = aspect_ratio
        self.focus_on_objects = focus_on_objects
        if not isinstance(self.aspect_ratio, float):
            raise TypeError("{}: input type is invalid.".format(self.aspect_ratio))

    def _random_crop_or_padding_image(self, sample):
        im = sample['image']
        height, width = im.shape[:2]
        cur_ratio = width / height
        gt_bbox = sample['bboxes']

        # 获得目标范围
        if gt_bbox.shape[0] != 0 and self.focus_on_objects:
            min_x = max(np.min(gt_bbox[:,0]), 1)
            min_y = max(np.min(gt_bbox[:,1]), 1)
            max_x = min(np.max(gt_bbox[:,2]), width - 1)
            max_y = min(np.max(gt_bbox[:,3]), height -1 )
            rwi = max_x - min_x
            rhi = max_y - min_y
        else:
            min_x = 1
            min_y = 1
            max_x = width - 1
            max_y = height - 1
            rwi = max_x - min_x
            rhi = max_y - min_y

        # 随机裁切
        left, right, top, bottom = 0,0,0,0
        if cur_ratio < self.aspect_ratio:
            dwi = width
            dhi = int(dwi / self.aspect_ratio)
            if dhi <= rhi:
                dhi = rhi + 20
                dwi = int(dhi * self.aspect_ratio)

            left = np.random.randint(0, min_x)
            right = np.random.randint(min(max_x, min(width-1, dwi-1)), width)

            top = np.random.randint(max(0, max_y - dhi), min_y+1)
            bottom = min(top + dhi, height - 1)
        else:
            dhi = height
            dwi = int(dhi * self.aspect_ratio)
            if dwi <= rwi:
                dwi = rwi + 20
                dhi = int(dwi / self.aspect_ratio)

            top = np.random.randint(0, min_y)
            bottom = np.random.randint(min(max_y, min(height-1, dhi-1)), height)

            left = np.random.randint(max(0, max_x - dwi), min_x+1)
            right = min(left + dwi, width - 1)

        if len(gt_bbox) > 0:
            gt_bbox[:, [0,2]] = gt_bbox[:, [0,2]] - left
            gt_bbox[:, [1,3]] = gt_bbox[:, [1,3]] - top
            
        if 'joints2d' in sample and len(sample['joints2d']) != 0:
            sample['joints2d'][:, 0] = sample['joints2d'][:, 0] - left
            sample['joints2d'][:, 1] = sample['joints2d'][:, 1] - top
            
            if 'joints_vis' in sample and len(sample['joints_vis']) != 0:
                pos_outlie_x = sample['joints2d'][:, 0] <= 0
                pos_outlie_y = sample['joints2d'][:, 1] <= 0

                pos_outlie = pos_outlie_x | pos_outlie_y | sample['joints_vis'] == 0
                sample['joints_vis'][pos_outlie] = 0

        top = int(top)
        bottom = int(bottom)
        left = int(left)
        right = int(right)
        im = im[top:bottom, left:right, :].copy()
        rhi, rwi = im.shape[:2]
        height, width = im.shape[:2]

        # 随机填充，保持比例
        image_new = im
        rhi, rwi = image_new.shape[:2]
        if abs(rwi / rhi - self.aspect_ratio) > 0.0001:
            if rwi / rhi > self.aspect_ratio:
                nwi = rwi
                nhi = int(rwi / self.aspect_ratio)
            else:
                nhi = rhi
                nwi = int(rhi * self.aspect_ratio)

            # 随机填充
            top_padding = 0
            bottom_padding = nhi - rhi
            if nhi > rhi:
                top_padding = np.random.randint(0, nhi - rhi)
                bottom_padding = (nhi - rhi) - top_padding

            left_padding = 0
            right_padding = nwi - rwi
            if nwi > rwi:
                left_padding = np.random.randint(0, nwi - rwi)
                right_padding = (nwi - rwi) - left_padding

            # 调整image
            image_new = cv2.copyMakeBorder(image_new, top_padding, bottom_padding, left_padding, right_padding,
                                         cv2.BORDER_CONSTANT, value=(128, 128, 128))

            # 调整bbox
            if len(gt_bbox) > 0:
                gt_bbox[:, [0,2]] = gt_bbox[:, [0,2]] + left_padding
                gt_bbox[:, [1,3]] = gt_bbox[:, [1,3]] + top_padding
            
            if 'joints2d' in sample and len(sample['joints2d']) > 0:
                gt_kpts = sample['joints2d']
                gt_kpts[:, 0] = gt_kpts[:, 0] + left_padding
                gt_kpts[:, 1] = gt_kpts[:, 1] + top_padding
                sample['joints2d'] = gt_kpts
                
                if 'joints_vis' in sample and len(sample['joints_vis']) > 0:
                    pos_outlie_x = sample['joints2d'][:, 0] <= 0
                    pos_outlie_y = sample['joints2d'][:, 1] <= 0

                    pos_outlie = pos_outlie_x | pos_outlie_y | sample['joints_vis'] == 0
                    sample['joints_vis'][pos_outlie] = 0                    

        sample['image'] = image_new
        sample['bboxes'] = gt_bbox
        sample['height'] = image_new.shape[0]
        sample['width'] = image_new.shape[1]
        
        # vis_2d_boxes_in_image(image_new, gt_bbox, './a.png')        
        if 'image_meta' in sample:
            sample['image_meta']['image_shape'] = (image_new.shape[0], image_new.shape[1])
        return sample

    def __call__(self, sample, context=None):
        im = sample['image']
        height, width = im.shape[:2]
        np.random.seed(int(time.time()))
        cur_ratio = width / height
        if abs(cur_ratio - self.aspect_ratio) > 0.000001:
            sample = self._random_crop_or_padding_image(sample)

        return sample

# FINISH FIX
class Rotation(BaseOperator):
    """
    Rotate the image with bounding box
    """
    def __init__(self, degree=30, border_value=[0, 0, 0], label_border_value=0,inputs=None):
        super(Rotation, self).__init__(inputs=inputs)
        self._degree = degree
        self._border_value = border_value
        self._label_border_value = label_border_value

    def __call__(self, sample, context=None):
        im = sample['image']
        height, width = im.shape[:2]
        cx, cy = width // 2, height // 2
        angle = np.random.randint(0, self._degree * 2) - self._degree
        rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
        image_rotated = cv2.warpAffine(
                src=im,
                M=rot_mat,
                dsize=im.shape[1::-1],
                flags=cv2.INTER_AREA)

        if 'bboxes' in sample:
            gt_bbox = sample['bboxes']
            for i, bbox in enumerate(gt_bbox):
                x1, y1, x2, y2 = bbox
                coor = [[x1, x2, x1, x2], [y1, y1, y2, y2], [1, 1, 1, 1]]
                coor_new = np.matmul(rot_mat, coor)
                xmin = np.min(coor_new[0, :])
                ymin = np.min(coor_new[1, :])
                xmax = np.max(coor_new[0, :])
                ymax = np.max(coor_new[1, :])
                region_scale = np.sqrt((xmax - xmin)*(ymax - ymin))
                if region_scale > 50:
                    margin = 1.8
                    xmin = np.min(coor_new[0, :]) + np.abs(angle/margin)
                    ymin = np.min(coor_new[1, :]) + np.abs(angle/margin)
                    xmax = np.max(coor_new[0, :]) - np.abs(angle/margin)
                    ymax = np.max(coor_new[1, :]) - np.abs(angle/margin)
                    
                xmin = np.clip(xmin, 0, image_rotated.shape[1]-1)
                ymin = np.clip(ymin, 0, image_rotated.shape[0]-1)
                xmax = np.clip(xmax, 0, image_rotated.shape[1]-1)
                ymax = np.clip(ymax, 0, image_rotated.shape[0]-1)
                gt_bbox[i, 0] = xmin
                gt_bbox[i, 1] = ymin
                gt_bbox[i, 2] = xmax
                gt_bbox[i, 3] = ymax
            
            sample['bboxes'] = gt_bbox

        if 'joints2d' in sample and sample['joints2d'].shape[0] > 0:
            gt_kpts = sample['joints2d']
            for instance_i in range(gt_kpts.shape[0]):
                for i, kpt in enumerate(gt_kpts[instance_i]):
                    x1, y1 = kpt
                    coor = [[x1, x1, x1, x1], [y1, y1, y1, y1], [1, 1, 1, 1]]
                    coor_new = np.matmul(rot_mat, coor)
                    gt_kpts[instance_i, i, 0] = coor_new[0, 0]
                    gt_kpts[instance_i, i, 1] = coor_new[1, 0]

            sample['joints2d'] = gt_kpts

        if 'semantic' in sample:
            label = cv2.warpAffine(
                sample['semantic'],
                M=rot_mat,
                dsize=im.shape[1::-1],
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=self._label_border_value)
            sample['semantic'] = label

        sample['height'] = image_rotated.shape[0]
        sample['width'] = image_rotated.shape[1]
        if 'image_meta' in sample:
            sample['image_shape'] = (image_rotated.shape[0], image_rotated.shape[1])
        
        # vis_2d_boxes_in_image(image_rotated, sample['bboxes'], sample['labels'], './a.png') 
        sample['image'] = image_rotated
        return sample


class MultiscaleTestResize(BaseOperator):
    def __init__(self,
                 origin_target_size=800,
                 origin_max_size=1333,
                 target_size=[],
                 max_size=2000,
                 interp=cv2.INTER_LINEAR,
                 use_flip=True, inputs=None):
        """
        Rescale image to the each size in target size, and capped at max_size.
        Args:
            origin_target_size(int): original target size of image's short side.
            origin_max_size(int): original max size of image.
            target_size (list): A list of target sizes of image's short side.
            max_size (int): the max size of image.
            interp (int): the interpolation method.
            use_flip (bool): whether use flip augmentation.
        """
        super(MultiscaleTestResize, self).__init__(inputs=inputs)
        self.origin_target_size = int(origin_target_size)
        self.origin_max_size = int(origin_max_size)
        self.max_size = int(max_size)
        self.interp = int(interp)
        self.use_flip = use_flip

        if not isinstance(target_size, list):
            raise TypeError(
                "Type of target_size is invalid. Must be List, now is {}".
                format(type(target_size)))
        self.target_size = target_size
        if not (isinstance(self.origin_target_size, int) and isinstance(
                self.origin_max_size, int) and isinstance(self.max_size, int)
                and isinstance(self.interp, int)):
            raise TypeError("{}: input type is invalid.".format(self))

    def __call__(self, sample, context=None):
        """ Resize the image numpy for multi-scale test.
        """
        origin_ims = {}
        im = sample['image']
        if not isinstance(im, np.ndarray):
            raise TypeError("{}: image type is not numpy.".format(self))
        if len(im.shape) != 3:
            raise ImageError('{}: image is not 3-dimensional.'.format(self))
        im_shape = im.shape
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        if float(im_size_min) == 0:
            raise ZeroDivisionError('{}: min size of image is 0'.format(self))
        base_name_list = ['image']
        origin_ims['image'] = im
        if self.use_flip:
            sample['image_flip'] = im[:, ::-1, :]
            base_name_list.append('image_flip')
            origin_ims['image_flip'] = sample['image_flip']

        for base_name in base_name_list:
            im_scale = float(self.origin_target_size) / float(im_size_min)
            # Prevent the biggest axis from being more than max_size
            if np.round(im_scale * im_size_max) > self.origin_max_size:
                im_scale = float(self.origin_max_size) / float(im_size_max)
            im_scale_x = im_scale
            im_scale_y = im_scale

            resize_w = np.round(im_scale_x * float(im_shape[1]))
            resize_h = np.round(im_scale_y * float(im_shape[0]))
            im_resize = cv2.resize(
                origin_ims[base_name],
                None,
                None,
                fx=im_scale_x,
                fy=im_scale_y,
                interpolation=self.interp)

            sample[base_name] = im_resize
            info_name = 'im_info' if base_name == 'image' else 'im_info_image_flip'
            sample[base_name] = im_resize
            sample[info_name] = np.array(
                [resize_h, resize_w, im_scale], dtype=np.float32)
            for i, size in enumerate(self.target_size):
                im_scale = float(size) / float(im_size_min)
                if np.round(im_scale * im_size_max) > self.max_size:
                    im_scale = float(self.max_size) / float(im_size_max)
                im_scale_x = im_scale
                im_scale_y = im_scale
                resize_w = np.round(im_scale_x * float(im_shape[1]))
                resize_h = np.round(im_scale_y * float(im_shape[0]))
                im_resize = cv2.resize(
                    origin_ims[base_name],
                    None,
                    None,
                    fx=im_scale_x,
                    fy=im_scale_y,
                    interpolation=self.interp)

                im_info = [resize_h, resize_w, im_scale]
                # hard-code here, must be consistent with
                # ppdet/modeling/architectures/input_helper.py
                name = base_name + '_scale_' + str(i)
                info_name = 'im_info_' + name
                sample[name] = im_resize
                sample[info_name] = np.array(
                    [resize_h, resize_w, im_scale], dtype=np.float32)
        return sample


# FINISH FIX
class RandomFlipImage(BaseOperator):
    def __init__(self, 
                prob=0.5, 
                is_normalized=False, 
                is_mask_flip=False, 
                swap_ids=[[1,3,19,5,7,9,11,13,15],[2,4,20,6,8,10,12,14,16]], 
                swap_labels=[[0,1],[1,0]],
                inputs=None):
        """
        Args:
            prob (float): the probability of flipping image
            is_normalized (bool): whether the bbox scale to [0,1]
            is_mask_flip (bool): whether flip the segmentation
        """
        super(RandomFlipImage, self).__init__(inputs=inputs)
        self.prob = prob
        self.is_normalized = is_normalized
        self.is_mask_flip = is_mask_flip
        self.swap_ids = swap_ids
        self.swap_labels = swap_labels
        if not (isinstance(self.prob, float) and
                isinstance(self.is_normalized, bool) and
                isinstance(self.is_mask_flip, bool)):
            raise TypeError("{}: input type is invalid.".format(self))

    def flip_segms(self, segms, height, width):
        def _flip_poly(poly, width):
            flipped_poly = np.array(poly)
            flipped_poly[0::2] = width - np.array(poly[0::2]) - 1
            return flipped_poly.tolist()

        def _flip_rle(rle, height, width):
            if 'counts' in rle and type(rle['counts']) == list:
                rle = mask_util.frPyObjects(rle, height, width)
            mask = mask_util.decode(rle)
            mask = mask[:, ::-1]
            rle = mask_util.encode(np.array(mask, order='F', dtype=np.uint8))
            return rle

        flipped_segms = []
        for segm in segms:
            if is_poly(segm):
                # Polygon format
                flipped_segms.append([_flip_poly(poly, width) for poly in segm])
            else:
                # RLE format
                import pycocotools.mask as mask_util
                flipped_segms.append(_flip_rle(segm, height, width))
        return flipped_segms

    def flip_keypoint(self, gt_keypoint, width):
        # for i in range(gt_keypoint.shape[1]):
        #     if i % 2 == 0:
        #         old_x = gt_keypoint[:, i].copy()
        #         if self.is_normalized:
        #             gt_keypoint[:, i] = 1 - old_x
        #         else:
        #             gt_keypoint[:, i] = width - old_x - 1
        gt_keypoint[:, :, 0] = width - gt_keypoint[:, :, 0] - 1
        return gt_keypoint

    def __call__(self, sample, context=None):
        """Filp the image and bounding box.
        Operators:
            1. Flip the image numpy.
            2. Transform the bboxes' x coordinates.
              (Must judge whether the coordinates are normalized!)
            3. Transform the segmentations' x coordinates.
              (Must judge whether the coordinates are normalized!)
        Output:
            sample: the image, bounding box and segmentation part
                    in sample are flipped.
        """

        im = sample['image']
        if not isinstance(im, np.ndarray):
            raise TypeError("{}: image is not a numpy array.".format(self))
        if len(im.shape) != 3:
            raise ImageError("{}: image is not 3-dimensional.".format(self))
        height, width, _ = im.shape
        if np.random.uniform(0, 1) < self.prob:
            im = im[:, ::-1, :]
            if 'bboxes' in sample.keys() and sample['bboxes'].shape[0] > 0:
                gt_bbox = sample['bboxes']
                oldx1 = gt_bbox[:, 0].copy()
                oldx2 = gt_bbox[:, 2].copy()
                if self.is_normalized:
                    gt_bbox[:, 0] = 1 - oldx2
                    gt_bbox[:, 2] = 1 - oldx1
                else:
                    gt_bbox[:, 0] = width - oldx2 - 1
                    gt_bbox[:, 2] = width - oldx1 - 1
                if gt_bbox.shape[0] != 0 and (gt_bbox[:, 2] < gt_bbox[:, 0]).all():
                    m = "{}: invalid box, x2 should be greater than x1".format(
                        self)
                    raise BboxError(m)
                sample['bboxes'] = gt_bbox
                
                if len(self.swap_labels) > 0:
                    temp = copy.deepcopy(sample['labels'])
                    for before_label, after_label in self.swap_labels:
                        selected_ids = sample['labels'] == before_label
                        temp[selected_ids] = after_label
                    
                    sample['labels'] = temp

            if 'segments' in sample.keys():
                if self.is_mask_flip and len(sample['segments']) != 0:
                    sample['segments'] = self.flip_segms(sample['segments'],
                                                        height, width)

            if 'joints2d' in sample.keys() and sample['joints2d'].shape[0] > 0:
                gt_keypoints = sample['joints2d']
                gt_keypoints[:, :, 0] = width - gt_keypoints[:, :, 0] - 1.0

                # 更换keypoints位置 (图像水平翻转后，需要对调关键点位置)
                # swap_k1 = [1,3,19,5,7,9,11,13,15]
                # swap_k2 = [2,4,20,6,8,10,12,14,16] 
                if len(self.swap_ids) > 0:
                    swap_k1 = self.swap_ids[0]
                    swap_k2 = self.swap_ids[1]
                    temp = gt_keypoints[:,swap_k1,:].copy()
                    gt_keypoints[:,swap_k1,:] = gt_keypoints[:,swap_k2,:]
                    gt_keypoints[:,swap_k2,:] = temp

                sample['joints2d'] = gt_keypoints.copy()

            if 'semantic' in sample.keys() and sample['semantic'] is not None:
                sample['semantic'] = sample['semantic'][:, ::-1]

            if 'image_meta' in sample:
                sample['image_meta']['flipped'] = True
            sample['image'] = im

        # vis_2d_boxes_in_image(sample['image'].copy(), sample['bboxes'], sample['labels'], './d.png') 
        return sample


# FINISH FIX
class RandomErasingImage(BaseOperator):
    # only for det task
    def __init__(self, prob=0.5, sl=0.02, sh=0.4, r1=0.3, inputs=None):
        """
        Random Erasing Data Augmentation, see https://arxiv.org/abs/1708.04896
        Args:
            prob (float): probability to carry out random erasing
            sl (float): lower limit of the erasing area ratio
            sh (float): upper limit of the erasing area ratio
            r1 (float): aspect ratio of the erasing region
        """
        super(RandomErasingImage, self).__init__(inputs=inputs)
        self.prob = prob
        self.sl = sl
        self.sh = sh
        self.r1 = r1

    def __call__(self, sample, context=None):
        gt_bbox = sample['bboxes']
        im = sample['image']
        if not isinstance(im, np.ndarray):
            raise TypeError("{}: image is not a numpy array.".format(self))
        if len(im.shape) != 3:
            raise ImageError("{}: image is not 3-dimensional.".format(self))

        for idx in range(gt_bbox.shape[0]):
            if self.prob <= np.random.rand():
                continue

            x1, y1, x2, y2 = gt_bbox[idx, :]
            w_bbox = x2 - x1 + 1
            h_bbox = y2 - y1 + 1
            area = w_bbox * h_bbox

            target_area = random.uniform(self.sl, self.sh) * area
            aspect_ratio = random.uniform(self.r1, 1 / self.r1)

            h = int(round(math.sqrt(target_area * aspect_ratio)))
            w = int(round(math.sqrt(target_area / aspect_ratio)))

            if w < w_bbox and h < h_bbox:
                off_y1 = random.randint(0, int(h_bbox - h))
                off_x1 = random.randint(0, int(w_bbox - w))
                im[int(y1 + off_y1):int(y1 + off_y1 + h), int(x1 + off_x1):
                    int(x1 + off_x1 + w), :] = 0
        sample['image'] = im
        return sample

# FINISH FIX
class GridMaskOp(BaseOperator):
    def __init__(self,
                 use_h=True,
                 use_w=True,
                 rotate=1,
                 offset=False,
                 ratio=0.5,
                 mode=1,
                 prob=0.7,
                 upper_iter=360000, inputs=None):
        """
        GridMask Data Augmentation, see https://arxiv.org/abs/2001.04086
        Args:
            use_h (bool): whether to mask vertically
            use_w (boo;): whether to mask horizontally
            rotate (float): angle for the mask to rotate
            offset (float): mask offset
            ratio (float): mask ratio
            mode (int): gridmask mode
            prob (float): max probability to carry out gridmask
            upper_iter (int): suggested to be equal to global max_iter
        """
        super(GridMaskOp, self).__init__(inputs=inputs)
        self.use_h = use_h
        self.use_w = use_w
        self.rotate = rotate
        self.offset = offset
        self.ratio = ratio
        self.mode = mode
        self.prob = prob
        self.upper_iter = upper_iter

        from .gridmask_utils import GridMask
        self.gridmask_op = GridMask(
            use_h,
            use_w,
            rotate=rotate,
            offset=offset,
            ratio=ratio,
            mode=mode,
            prob=prob,
            upper_iter=upper_iter)

    def __call__(self, sample, context=None):
        # now, ignore curr_iter
        curr_iter = sample['curr_iter'] if 'curr_iter' in sample else 0
        sample['image'] = self.gridmask_op(sample['image'], curr_iter)
        return sample


# FINISH FIX
class AutoAugmentImage(BaseOperator):
    def __init__(self, is_normalized=False, autoaug_type="v1", inputs=None):
        """
        Args:
            is_normalized (bool): whether the bbox scale to [0,1]
            autoaug_type (str): autoaug type, support v0, v1, v2, v3, test
        """
        super(AutoAugmentImage, self).__init__(inputs=inputs)
        self.is_normalized = is_normalized
        self.autoaug_type = autoaug_type
        if not isinstance(self.is_normalized, bool):
            raise TypeError("{}: input type is invalid.".format(self))

    def __call__(self, sample, context=None):
        """
        Learning Data Augmentation Strategies for Object Detection, see https://arxiv.org/abs/1906.11172
        """
        gt_bbox = sample['bboxes']
        im = sample['image']
        if not isinstance(im, np.ndarray):
            raise TypeError("{}: image is not a numpy array.".format(self))
        if len(im.shape) != 3:
            raise ImageError("{}: image is not 3-dimensional.".format(self))
        if len(gt_bbox) == 0:
            return sample

        # gt_boxes : [x1, y1, x2, y2]
        # norm_gt_boxes: [y1, x1, y2, x2]
        height, width, _ = im.shape
        norm_gt_bbox = np.ones_like(gt_bbox, dtype=np.float32)
        if not self.is_normalized:
            norm_gt_bbox[:, 0] = gt_bbox[:, 1] / float(height)
            norm_gt_bbox[:, 1] = gt_bbox[:, 0] / float(width)
            norm_gt_bbox[:, 2] = gt_bbox[:, 3] / float(height)
            norm_gt_bbox[:, 3] = gt_bbox[:, 2] / float(width)
        else:
            norm_gt_bbox[:, 0] = gt_bbox[:, 1]
            norm_gt_bbox[:, 1] = gt_bbox[:, 0]
            norm_gt_bbox[:, 2] = gt_bbox[:, 3]
            norm_gt_bbox[:, 3] = gt_bbox[:, 2]

        from .autoaugment_utils import distort_image_with_autoaugment
        im, norm_gt_bbox = distort_image_with_autoaugment(im, norm_gt_bbox,
                                                            self.autoaug_type)
        if not self.is_normalized:
            gt_bbox[:, 0] = norm_gt_bbox[:, 1] * float(width)
            gt_bbox[:, 1] = norm_gt_bbox[:, 0] * float(height)
            gt_bbox[:, 2] = norm_gt_bbox[:, 3] * float(width)
            gt_bbox[:, 3] = norm_gt_bbox[:, 2] * float(height)
        else:
            gt_bbox[:, 0] = norm_gt_bbox[:, 1]
            gt_bbox[:, 1] = norm_gt_bbox[:, 0]
            gt_bbox[:, 2] = norm_gt_bbox[:, 3]
            gt_bbox[:, 3] = norm_gt_bbox[:, 2]

        sample['bboxes'] = gt_bbox
        sample['image'] = im
        return sample


# FINISH FIX
class RandomDistort(BaseOperator):
    def __init__(self,
                 brightness_lower=0.5,
                 brightness_upper=1.5,
                 contrast_lower=0.5,
                 contrast_upper=1.5,
                 saturation_lower=0.5,
                 saturation_upper=1.5,
                 hue_lower=-18,
                 hue_upper=18,
                 brightness_prob=0.5,
                 contrast_prob=0.5,
                 saturation_prob=0.5,
                 hue_prob=0.5,
                 count=4,
                 is_order=False, inputs=None):
        """
        Args:
            brightness_lower/ brightness_upper (float): the brightness
                between brightness_lower and brightness_upper
            contrast_lower/ contrast_upper (float): the contrast between
                contrast_lower and contrast_lower
            saturation_lower/ saturation_upper (float): the saturation
                between saturation_lower and saturation_upper
            hue_lower/ hue_upper (float): the hue between
                hue_lower and hue_upper
            brightness_prob (float): the probability of changing brightness
            contrast_prob (float): the probability of changing contrast
            saturation_prob (float): the probability of changing saturation
            hue_prob (float): the probability of changing hue
            count (int): the kinds of doing distrot
            is_order (bool): whether determine the order of distortion
        """
        super(RandomDistort, self).__init__(inputs=inputs)
        # only support PIL format
        self.brightness_lower = brightness_lower
        self.brightness_upper = brightness_upper
        self.contrast_lower = contrast_lower
        self.contrast_upper = contrast_upper
        self.saturation_lower = saturation_lower
        self.saturation_upper = saturation_upper
        self.hue_lower = hue_lower
        self.hue_upper = hue_upper
        self.brightness_prob = brightness_prob
        self.contrast_prob = contrast_prob
        self.saturation_prob = saturation_prob
        self.hue_prob = hue_prob
        self.count = count
        self.is_order = is_order

    def random_brightness(self, img):
        brightness_delta = np.random.uniform(self.brightness_lower,
                                             self.brightness_upper)
        prob = np.random.uniform(0, 1)
        if prob < self.brightness_prob:
            img = ImageEnhance.Brightness(img).enhance(brightness_delta)
        return img

    def random_contrast(self, img):
        contrast_delta = np.random.uniform(self.contrast_lower,
                                           self.contrast_upper)
        prob = np.random.uniform(0, 1)
        if prob < self.contrast_prob:
            img = ImageEnhance.Contrast(img).enhance(contrast_delta)
        return img

    def random_saturation(self, img):
        saturation_delta = np.random.uniform(self.saturation_lower,
                                             self.saturation_upper)
        prob = np.random.uniform(0, 1)
        if prob < self.saturation_prob:
            img = ImageEnhance.Color(img).enhance(saturation_delta)
        return img

    def random_hue(self, img):
        hue_delta = np.random.uniform(self.hue_lower, self.hue_upper)
        prob = np.random.uniform(0, 1)
        if prob < self.hue_prob:
            img = np.array(img.convert('HSV'))
            img[:, :, 0] = img[:, :, 0] + hue_delta
            img = Image.fromarray(img, mode='HSV').convert('RGB')
        return img

    def __call__(self, sample, context=None):
        """random distort the image"""
        ops = []
        if self.brightness_prob > 0:
            ops.append(self.random_brightness)
        if self.contrast_prob > 0:
            ops.append(self.random_contrast)
        if self.saturation_prob > 0:
            ops.append(self.random_saturation)
        if self.hue_prob > 0:
            ops.append(self.random_hue)
        count = min(self.count, len(ops))

        if self.is_order:
            prob = np.random.uniform(0, 1)
            if prob < 0.5:
                ops = [
                    self.random_brightness,
                    self.random_saturation,
                    self.random_hue,
                    self.random_contrast,
                ]
        else:
            ops = random.sample(ops, count)
        assert 'image' in sample, "image data not found"
        im = sample['image']
        for id in range(count):
            im = ops[id](im)
        sample['image'] = im
        return sample


# FINISH FIX
class ExpandImage(BaseOperator):
    # FINISH CORRET (JIAN)
    # only for det task
    def __init__(self, max_ratio, prob, mean=[127.5, 127.5, 127.5], inputs=None):
        """
        Args:
            max_ratio (float): the ratio of expanding
            prob (float): the probability of expanding image
            mean (list): the pixel mean
        """
        super(ExpandImage, self).__init__(inputs=inputs)
        self.max_ratio = max_ratio
        self.mean = mean
        self.prob = prob

    def __call__(self, sample, context):
        """
        Expand the image and modify bounding box.
        Operators:
            1. Scale the image width and height.
            2. Construct new images with new height and width.
            3. Fill the new image with the mean.
            4. Put original image into new image.
            5. Rescale the bounding box.
            6. Determine if the new bbox is satisfied in the new image.
        Returns:
            sample: the image, bounding box are replaced.
        """

        prob = np.random.uniform(0, 1)
        assert 'image' in sample, 'not found image data'
        im = sample['image']
        gt_bbox = sample['bboxes']
        gt_class = sample['labels']
        im_height, im_width = im.shape[:2]
        if prob < self.prob:
            if self.max_ratio - 1 >= 0.01:
                expand_ratio = np.random.uniform(1, self.max_ratio)
                height = int(im_height * expand_ratio)
                width = int(im_width * expand_ratio)
                h_off = math.floor(np.random.uniform(0, height - im_height))
                w_off = math.floor(np.random.uniform(0, width - im_width))
                expand_bbox = [
                    -w_off / im_width, -h_off / im_height,
                    (width - w_off) / im_width, (height - h_off) / im_height
                ]
                expand_im = np.ones((height, width, 3))
                expand_im = np.uint8(expand_im * np.squeeze(self.mean))
                expand_im = Image.fromarray(expand_im)
                im = Image.fromarray(im)
                expand_im.paste(im, (int(w_off), int(h_off)))
                expand_im = np.asarray(expand_im)

                if 'joints2d' in sample.keys() and 'joints_ignore' in sample.keys():
                    keypoints = (sample['joints2d'],
                                 sample['joints_ignore'])
                    gt_bbox, gt_class, _, gt_keypoints = filter_and_process(
                        expand_bbox, gt_bbox, gt_class, keypoints=keypoints)
                    sample['joints2d'] = gt_keypoints[0]
                    sample['joints_ignore'] = gt_keypoints[1]
                else:
                    gt_bbox, gt_class, _ = filter_and_process(expand_bbox, gt_bbox, gt_class)
                sample['image'] = expand_im
                sample['bboxes'] = gt_bbox
                sample['labels'] = gt_class
                sample['width'] = width
                sample['height'] = height

        return sample


# FINISH FIX
class CropImage(BaseOperator):
    # 已经完成验证
    def __init__(self, prob, batch_sampler, satisfy_all=False, avoid_no_bbox=True, inputs=None):
        """
        Args:
            batch_sampler (list): Multiple sets of different
                                  parameters for cropping.
            satisfy_all (bool): whether all boxes must satisfy.
            e.g.[[1, 1, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.1, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.3, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.5, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.7, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.9, 1.0],
                 [1, 50, 0.3, 1.0, 0.5, 2.0, 0.0, 1.0]]
           [max sample, max trial, min scale, max scale,
            min aspect ratio, max aspect ratio,
            min overlap, max overlap]
            avoid_no_bbox (bool): whether to to avoid the
                                  situation where the box does not appear.
        """
        super(CropImage, self).__init__(inputs=inputs)
        self.batch_sampler = batch_sampler
        self.satisfy_all = satisfy_all
        self.avoid_no_bbox = avoid_no_bbox
        self.prob = prob

    def rotate_2d(self, pt_2d, rot_rad):
        x = pt_2d[0]
        y = pt_2d[1]
        sn, cs = np.sin(rot_rad), np.cos(rot_rad)
        xx = x * cs - y * sn
        yy = x * sn + y * cs
        return np.array([xx, yy], dtype=np.float32)

    def gen_trans_from_bbox(self, c_x, c_y, src_width, src_height, dst_width, dst_height, scale, rot, inv=False):
        # augment size with scale
        src_w = src_width * scale
        src_h = src_height * scale
        src_center = np.array([c_x, c_y], dtype=np.float32)

        # augment rotation
        rot_rad = np.pi * rot / 180
        src_downdir = self.rotate_2d(np.array([0, src_h * 0.5], dtype=np.float32), rot_rad)
        src_rightdir = self.rotate_2d(np.array([src_w * 0.5, 0], dtype=np.float32), rot_rad)

        dst_w = dst_width
        dst_h = dst_height
        dst_center = np.array([dst_w * 0.5, dst_h * 0.5], dtype=np.float32)
        dst_downdir = np.array([0, dst_h * 0.5], dtype=np.float32)
        dst_rightdir = np.array([dst_w * 0.5, 0], dtype=np.float32)

        src = np.zeros((3, 2), dtype=np.float32)
        src[0, :] = src_center
        src[1, :] = src_center + src_downdir
        src[2, :] = src_center + src_rightdir

        dst = np.zeros((3, 2), dtype=np.float32)
        dst[0, :] = dst_center
        dst[1, :] = dst_center + dst_downdir
        dst[2, :] = dst_center + dst_rightdir
        
        if inv:
            trans = cv2.getAffineTransform(np.float32(dst), np.float32(src))
        else:
            trans = cv2.getAffineTransform(np.float32(src), np.float32(dst))

        trans = trans.astype(np.float32)
        return trans

    def __call__(self, sample):
        """
        Crop the image and modify bounding box.
        Operators:
            1. Scale the image width and height.
            2. Crop the image according to a radom sample.
            3. Rescale the bounding box.
            4. Determine if the new bbox is satisfied in the new image.
        Returns:
            sample: the image, bounding box are replaced.
        """
        if np.random.random() > self.prob:
            return sample

        assert 'image' in sample, "image data not found"
        im = sample['image']
        gt_bbox = sample['bboxes']
        gt_class = sample['labels']
        im_height, im_width = im.shape[:2]
        # gt_score = None
        # if 'gt_score' in sample:
        #     gt_score = sample['gt_score']
    
        sampled_bbox = []
        for sampler in self.batch_sampler:
            found = 0
            for i in range(sampler[1]):
                if found >= sampler[0]:
                    break
                sample_bbox = generate_sample_bbox(sampler)
                if gt_bbox.shape[0] == 0:
                    sampled_bbox.append(sample_bbox)
                    found = found + 1
                    break

                if satisfy_sample_constraint(
                    sampler, 
                    sample_bbox, 
                    gt_bbox/np.array([[im_width, im_height, im_width, im_height]]),
                    self.satisfy_all
                ):
                    sampled_bbox.append(sample_bbox)
                    found = found + 1

        im = np.array(im)
        while sampled_bbox:
            idx = int(np.random.uniform(0, len(sampled_bbox)))
            sample_bbox = sampled_bbox.pop(idx)
            sample_bbox = clip_bbox(sample_bbox)
            crop_bbox, crop_class, crop_score = \
                filter_and_process(
                    sample_bbox, 
                    gt_bbox/np.array([[im_width, im_height, im_width, im_height]]) if gt_bbox.shape[0] > 0 else gt_bbox, 
                    gt_class)
            if self.avoid_no_bbox:
                if len(crop_bbox) < 1:
                    continue

            xmin = int(sample_bbox[0] * im_width)
            xmax = int(sample_bbox[2] * im_width)
            ymin = int(sample_bbox[1] * im_height)
            ymax = int(sample_bbox[3] * im_height)
            im = im[ymin:ymax, xmin:xmax].copy()
            sample['image'] = im
            if crop_bbox.shape[0] > 0:
                crop_bbox *= np.array([[im.shape[1], im.shape[0], im.shape[1], im.shape[0]]])
            sample['bboxes'] = crop_bbox
            sample['labels'] = crop_class[:,0]
            sample['width'] = im.shape[1]
            sample['height'] = im.shape[0]
                
            if 'image_meta' in sample and 'transform_matrix' in sample['image_meta']:
                base_trans = sample['image_meta']['transform_matrix']
                crop_trans = self.gen_trans_from_bbox((xmin+xmax)/2.0, (ymin+ymax)/2.0, im_width, im_height, im.shape[1], im.shape[0], 1.0, 0.0, inv=False)
                crop_trans = np.matmul(crop_trans, base_trans)
                sample['image_meta']['transform_matrix'] = crop_trans

            # # 测试可视化
            # for bi in range(len(crop_bbox)):
            #     x0,y0,x1,y1 = sample['gt_bbox'][bi]
            #     cls_label = crop_class[bi]
            #     x0=(int)(x0)
            #     y0=(int)(y0)
            #     x1=(int)(x1)
            #     y1=(int)(y1)
            #     color_v = (255,0,0)
            #     if cls_label == 0:
            #         color_v = (0,0,255)
            #     cv2.rectangle(im, (x0,y0),(x1,y1), color_v, 4)
            # cv2.imwrite("./crop_show.png", im)
            return sample
        return sample


# FINISH FIX
class NormalizeBox(BaseOperator):
    # FINISH CORRET (JIAN)
    # only for det task
    """Transform the bounding box's coornidates to [0,1]."""

    def __init__(self, inputs=None):
        super(NormalizeBox, self).__init__(inputs=inputs)

    def __call__(self, sample, context):
        gt_bbox = sample['bboxes']
        height, width = sample['image'].shape[:2]
        for i in range(gt_bbox.shape[0]):
            gt_bbox[i][0] = gt_bbox[i][0] / width
            gt_bbox[i][1] = gt_bbox[i][1] / height
            gt_bbox[i][2] = gt_bbox[i][2] / width
            gt_bbox[i][3] = gt_bbox[i][3] / height
        sample['bboxes'] = gt_bbox

        if 'joints2d' in sample.keys():
            gt_keypoint = sample['joints2d']

            for i in range(gt_keypoint.shape[1]):
                if i % 2:
                    gt_keypoint[:, i] = gt_keypoint[:, i] / height
                else:
                    gt_keypoint[:, i] = gt_keypoint[:, i] / width
            sample['joints2d'] = gt_keypoint

        return sample


# FINISH FIX
class Permute(BaseOperator):
    # FINISH CORRET (JIAN)
    def __init__(self, to_bgr=True, channel_first=True, inputs=None):
        """
        Change the channel.
        Args:
            to_bgr (bool): confirm whether to convert RGB to BGR
            channel_first (bool): confirm whether to change channel
        """
        super(Permute, self).__init__(inputs=inputs)
        self.to_bgr = to_bgr
        self.channel_first = channel_first
        if not (isinstance(self.to_bgr, bool) and
                isinstance(self.channel_first, bool)):
            raise TypeError("{}: input type is invalid.".format(self))

    def __call__(self, sample, context=None):
        assert 'image' in sample, "image data not found"
        for k in sample.keys():
            # hard code
            if k == 'image':
                im = sample[k]
                if self.channel_first:
                    im = np.swapaxes(im, 1, 2)
                    im = np.swapaxes(im, 1, 0)
                if self.to_bgr:
                    im = im[[2, 1, 0], :, :]
                sample[k] = im
                
            if k == 'semantic':
                label = sample[k]
                if self.channel_first:
                    label = np.expand_dims(label, 0)
                else:
                    label = np.expand_dims(label, -1)
                sample[k] = label

        return sample


# FINISH FIX
class MixupImage(BaseOperator):
    def __init__(self, prob=0.5, alpha=1.5, beta=1.5, inputs=None):
        """ Mixup image and gt_bbbox/gt_score
        Args:
            alpha (float): alpha parameter of beta distribute
            beta (float): beta parameter of beta distribute
        """
        super(MixupImage, self).__init__(inputs=inputs)
        self.alpha = alpha
        self.beta = beta
        self.prob = prob
        if self.alpha <= 0.0:
            raise ValueError("alpha shold be positive in {}".format(self))
        if self.beta <= 0.0:
            raise ValueError("beta shold be positive in {}".format(self))

    def _mixup_img(self, img1, img2, factor):
        h = max(img1.shape[0], img2.shape[0])
        w = max(img1.shape[1], img2.shape[1])
        if len(img1.shape) > 2:
            img = np.zeros((h, w, img1.shape[2]), 'float32')
        else:
            img = np.zeros((h, w), 'float32')
        img[:img1.shape[0], :img1.shape[1]] = \
            img1.astype('float32') * factor
        img[:img2.shape[0], :img2.shape[1]] += \
            img2.astype('float32') * (1.0 - factor)
        return img.astype('uint8')

    def __call__(self, sample, context=None):
        if 'mixup' not in sample:
            return sample
        if np.random.random() > self.prob:
            sample.pop('mixup')
            return sample
        
        factor = np.random.beta(self.alpha, self.beta)
        factor = max(0.0, min(1.0, factor))
        if factor >= 1.0:
            sample.pop('mixup')
            return sample
        if factor <= 0.0:
            return sample['mixup']
        im = self._mixup_img(sample['image'], sample['mixup']['image'], factor)
        gt_bbox1 = sample['bboxes']
        gt_bbox2 = sample['mixup']['bboxes']
        gt_bbox = gt_bbox1
        if gt_bbox2.shape[0] > 0:
            gt_bbox = np.concatenate((gt_bbox1, gt_bbox2), axis=0)

        gt_class1 = sample['labels']
        gt_class2 = sample['mixup']['labels']
        gt_class = gt_class1
        if gt_bbox2.shape[0] > 0:
            gt_class = np.concatenate((gt_class1, gt_class2), axis=0)           

        sample['image'] = im
        sample['boxes'] = gt_bbox
        sample['labels'] = gt_class
        sample['height'] = im.shape[0]
        sample['width'] = im.shape[1]
        sample.pop('mixup')

        if 'cutmix' in sample:
            sample.pop('cutmix')
        return sample


# FINISH FIX
class CutmixImage(BaseOperator):
    def __init__(self, prob=0.5, alpha=1.5, beta=1.5, around_obj_size=True, mix_ann=False, avoid_overlap=True, inputs=None):
        """ 
        CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features, see https://https://arxiv.org/abs/1905.04899
        Cutmix image and gt_bbbox/gt_score
        Args:
             alpha (float): alpha parameter of beta distribute
             beta (float): beta parameter of beta distribute
        """
        super(CutmixImage, self).__init__(inputs=inputs)
        self.alpha = alpha
        self.beta = beta
        self.around_obj_size = around_obj_size  # 如何设置融合区域的大小
        self.mix_ann = mix_ann                  # 是否允许两张图的目标解析的合并（合并后，两张图上的目标都作为GT）
        self.avoid_overlap = avoid_overlap      # 是否允许对img1上目标区域的覆盖
        self.prob = prob
        if self.alpha <= 0.0:
            raise ValueError("alpha shold be positive in {}".format(self))
        if self.beta <= 0.0:
            raise ValueError("beta shold be positive in {}".format(self))

    def _rand_bbox(self, img1, img2, bbox1, bbox2, factor):
        """ _rand_bbox """
        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])

        # 默认选择mix区域
        cut_rat = np.sqrt(1. - factor)
        
        cut_w = np.int(w * cut_rat)
        cut_h = np.int(h * cut_rat)

        # uniform
        cx = np.random.randint(w)
        cy = np.random.randint(h)

        bbx1 = np.clip(cx - cut_w // 2, 0, w)
        bby1 = np.clip(cy - cut_h // 2, 0, h)
        bbx2 = np.clip(cx + cut_w // 2, 0, w)
        bby2 = np.clip(cy + cut_h // 2, 0, h)

        img_1 = np.zeros((h, w, img1.shape[2]), 'float32')
        img_1[:img1.shape[0], :img1.shape[1], :] = \
            img1.astype('float32')
        img_2 = np.zeros((h, w, img2.shape[2]), 'float32')
        img_2[:img2.shape[0], :img2.shape[1], :] = \
            img2.astype('float32')
        img_1[bby1:bby2, bbx1:bbx2, :] = img2[bby1:bby2, bbx1:bbx2, :]
        return img_1

    def _rand_bbox_around_obj_size(self, img1, img2, bbox1, bbox2, factor):
        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])
        cut_rat = np.sqrt(1. - factor)
        
        # 选择混合区域大小
        cut_w = np.int(w * cut_rat)
        cut_h = np.int(h * cut_rat)            
        if self.around_obj_size and bbox1.shape[0] > 0:
            box_w = (bbox1[:,2] - bbox1[:,0]).mean()
            box_h = (bbox1[:,3] - bbox1[:,1]).mean()

            cut_w = min(np.int(box_w * (np.random.random() * 2 + 1.0)), w) # 1.0 ~ 3.0
            cut_h = min(np.int(box_h * (np.random.random() * 2 + 1.0)), h) # 1.0 ~ 3.0

        # 选择混合区域位置
        # uniform
        cx_in_1 = np.random.randint(w)
        cy_in_1 = np.random.randint(h)

        cx_in_2 = np.random.randint(w)
        cy_in_2 = np.random.randint(h)

        # in 1
        bbx1_in_1 = np.clip(cx_in_1 - cut_w // 2, 0, w)
        bby1_in_1 = np.clip(cy_in_1 - cut_h // 2, 0, h)
        bbx2_in_1 = np.clip(cx_in_1 + cut_w // 2, 0, w)
        bby2_in_1 = np.clip(cy_in_1 + cut_h // 2, 0, h)

        # in 2
        bbx1_in_2 = np.clip(cx_in_2 - cut_w // 2, 0, w)
        bby1_in_2 = np.clip(cy_in_2 - cut_h // 2, 0, h)
        bbx2_in_2 = np.clip(cx_in_2 + cut_w // 2, 0, w)
        bby2_in_2 = np.clip(cy_in_2 + cut_h // 2, 0, h)

        adjust_bb_w = min((bbx2_in_1-bbx1_in_1), (bbx2_in_2-bbx1_in_2))
        adjust_bb_h = min((bby2_in_1-bby1_in_1), (bby2_in_2-bby1_in_2))
        bbx2_in_1 = bbx1_in_1 + adjust_bb_w
        bbx2_in_2 = bbx1_in_2 + adjust_bb_w

        bby2_in_1 = bby1_in_1 + adjust_bb_h
        bby2_in_2 = bby1_in_2 + adjust_bb_h

        # img_1 = np.zeros((h, w, img1.shape[2]), 'float32')
        # img_1[:img1.shape[0], :img1.shape[1], :] = \
        #     img1.astype('float32')
        # img_2 = np.zeros((h, w, img2.shape[2]), 'float32')
        # img_2[:img2.shape[0], :img2.shape[1], :] = \
        #     img2.astype('float32')
        img1_c = img1.copy()
        # 避免img2中的目标，进入
        for bb in bbox2:
            x1,y1,x2,y2 = bb.astype(np.int32)
            img2[y1:y2,x1:x2] = np.random.randint(0,255)
        img1_c[bby1_in_1:bby2_in_1, bbx1_in_1:bbx2_in_1] = img2[bby1_in_2:bby2_in_2, bbx1_in_2:bbx2_in_2]      

        if self.avoid_overlap:
            for bb in bbox1:
                x1,y1,x2,y2 = bb.astype(np.int32)
                img1_c[y1:y2,x1:x2] = img1[y1:y2,x1:x2]

        return img1_c

    def __call__(self, sample, context=None):
        if 'cutmix' not in sample:
            return sample
        if np.random.random() > self.prob:
            sample.pop('cutmix')
            return sample

        factor = np.random.beta(self.alpha, self.beta)
        factor = max(0.0, min(1.0, factor))
        if factor >= 1.0:
            sample.pop('cutmix')
            return sample
        if factor <= 0.0:
            return sample['cutmix']
        img1 = sample['image']
        img2 = sample['cutmix']['image']

        gt_bbox1 = sample['boxes']
        gt_bbox2 = sample['cutmix']['boxes']
        img = None
        if self.mix_ann:
            # ignore avoid_overlap, around_obj_size
            img = self._rand_bbox(img1, img2, gt_bbox1, gt_bbox2, factor)
        else:
            img = self._rand_bbox_around_obj_size(img1, img2, gt_bbox1, gt_bbox2, factor)

        gt_bbox = gt_bbox1
        if gt_bbox2.shape[0] != 0 and self.mix_ann:
            gt_bbox = np.concatenate((gt_bbox1, gt_bbox2), axis=0)

        # gt_bbox = np.concatenate((gt_bbox1, gt_bbox2), axis=0)
        # gt_class1 = sample['gt_class']
        # gt_class2 = sample['cutmix']['gt_class']
        # gt_class = np.concatenate((gt_class1, gt_class2), axis=0)
        # gt_score1 = sample['gt_score']
        # gt_score2 = sample['cutmix']['gt_score']
        # gt_score = np.concatenate(
        #     (gt_score1 * factor, gt_score2 * (1. - factor)), axis=0)
        gt_class1 = sample['labels']
        gt_class = gt_class1
        # gt_score1 = sample['gt_score']
        # gt_score = gt_score1
        if gt_bbox2.shape[0] != 0 and self.mix_ann:
            gt_class2 = sample['cutpaste']['labels']
            gt_class = np.concatenate((gt_class1, gt_class2), axis=0)

            # gt_score2 = sample['cutpaste']['gt_score']
            # gt_score = np.concatenate(
            #     (gt_score1 * factor, gt_score2 * (1. - factor)), axis=0)

        sample['image'] = img
        sample['boxes'] = gt_bbox
        sample['labels'] = gt_class
        sample['height'] = img.shape[0]
        sample['width'] = img.shape[1]
        sample.pop('cutmix')

        if 'mixup' in sample:
            sample.pop('mixup')
        return sample


# FINSH FIX
class ResizeS(BaseOperator):
    """Resize image and bbox.
    Args:
        target_dim (int or list): target size, can be a single number or a list
            (for random shape).
        interp (int or str): interpolation method, can be an integer or
            'random' (for randomized interpolation).
            default to `cv2.INTER_LINEAR`.
    """
    # The interpolation mode
    interp_dict = {
        'NEAREST': cv2.INTER_NEAREST,
        'LINEAR': cv2.INTER_LINEAR,
        'CUBIC': cv2.INTER_CUBIC,
        'AREA': cv2.INTER_AREA,
        'LANCZOS4': cv2.INTER_LANCZOS4
    }

    def __init__(self, target_dim=[], interp='LINEAR', inputs=None):
        super(ResizeS, self).__init__(inputs=inputs)
        if type(target_dim) == list or type(target_dim) == tuple:
            self.target_dim = target_dim                # w,h
        else:
            self.target_dim = [target_dim, target_dim]  # w,h
        if not (interp == "RANDOM" or interp in self.interp_dict):
            raise ValueError("interp should be one of {}".format(
                self.interp_dict.keys()))

        self.interp = interp  # 'RANDOM' for yolov3

    def __call__(self, sample, context=None):
        w = sample['image'].shape[1]
        h = sample['image'].shape[0]

        if self.interp == "RANDOM":
            interp = random.choice(list(self.interp_dict.keys()))
        else:
            interp = self.interp

        resize_w, resize_h = self.target_dim
        scale_x = resize_w / w
        scale_y = resize_h / h
        if 'bboxes' in sample and len(sample['bboxes']) > 0:
            scale_array = np.array([scale_x, scale_y] * 2, dtype=np.float32)
            sample['bboxes'] = sample['bboxes'] * scale_array
            x1 = sample['bboxes'][:, 0:1]
            x1 = np.clip(x1, 0, resize_w-1)

            y1 = sample['bboxes'][:, 1:2]
            y1 = np.clip(y1, 0, resize_h-1)

            x2 = sample['bboxes'][:, 2:3]
            x2 = np.clip(x2, 0, resize_w-1)

            y2 = sample['bboxes'][:, 3:4]
            y2 = np.clip(y2, 0, resize_h-1)
            sample['bboxes'] = np.concatenate([x1, y1, x2, y2], axis=-1)
        
        if 'joints2d' in sample and len(sample['joints2d']) > 0:
            scale_array = np.array([scale_x, scale_y, 1], dtype=np.float32)
            sample['joints2d'] = sample['joints2d'] * scale_array
            x = sample['joints2d'][:, :, 0:1]
            x = np.clip(x, 0, resize_w - 1)

            y = sample['joints2d'][:, :, 1:2]
            y = np.clip(y, 0, resize_h - 1)

            if len(sample['joints2d'].shape) == 3:
                v = sample['joints2d'][:, :, 2:3]
                sample['joints2d'] = np.concatenate([x, y, v], axis=-1)
            else:
                sample['joints2d'] = np.concatenate([x, y], axis=-1)

        sample['image_meta']['image_shape'] = (resize_h, resize_w)
        sample['image_meta']['scale_factor'] =  [scale_x, scale_y] * 2
        sample['height'] = resize_h
        sample['width'] = resize_w
        sample['image'] = cv2.resize(
            sample['image'], (resize_w, resize_h), interpolation=self.interp_dict[interp])
        
        # vis_2d_boxes_in_image(sample['image'], sample['bboxes'],sample['labels'], './b.png')
        return sample

    def reset(self, target_dim):
        if type(target_dim) == list or type(target_dim) == tuple:
            self.target_dim = target_dim                # w,h
        else:
            self.target_dim = [target_dim, target_dim]  # w,h

    def get(self):
        return self.target_dim

# FINSH FIX
class ColorDistort(BaseOperator):
    """Random color distortion.
    Args:
        hue (list): hue settings.
            in [lower, upper, probability] format.
        saturation (list): saturation settings.
            in [lower, upper, probability] format.
        contrast (list): contrast settings.
            in [lower, upper, probability] format.
        brightness (list): brightness settings.
            in [lower, upper, probability] format.
        random_apply (bool): whether to apply in random (yolov7) or fixed (SSD)
            order.
        random_channel (bool): whether to swap channels randomly
    """

    def __init__(self,
                 hue=[-18, 18, 0.5],
                 saturation=[0.5, 1.5, 0.5],
                 contrast=[0.5, 1.5, 0.5],
                 brightness=[0.5, 1.5, 0.5],
                 random_apply=True,
                 random_channel=False, inputs=None):
        super(ColorDistort, self).__init__(inputs=inputs)
        self.hue = hue
        self.saturation = saturation
        self.contrast = contrast
        self.brightness = brightness
        self.random_apply = random_apply
        self.random_channel = random_channel

    def apply_hue(self, img):
        low, high, prob = self.hue
        if np.random.uniform(0., 1.) < prob:
            return img

        img = img.astype(np.float32)
        img[..., 0] += random.uniform(low, high)
        img[..., 0][img[..., 0] > 360] -= 360
        img[..., 0][img[..., 0] < 0] += 360
        return img

    def apply_saturation(self, img):
        low, high, prob = self.saturation
        if np.random.uniform(0., 1.) < prob:
            return img
        delta = np.random.uniform(low, high)
        img = img.astype(np.float32)
        img[..., 1] *= delta
        return img
        
    def apply_contrast(self, img):
        low, high, prob = self.contrast
        if np.random.uniform(0., 1.) < prob:
            return img
        delta = np.random.uniform(low, high)

        img = img.astype(np.float32)
        img *= delta
        return img

    def apply_brightness(self, img):
        low, high, prob = self.brightness
        if np.random.uniform(0., 1.) < prob:
            return img
        delta = np.random.uniform(low, high)

        img = img.astype(np.float32)
        img += delta
        return img

    def __call__(self, sample, context=None):
        img = sample['image']
        img = self.apply_brightness(img)
        if np.random.randint(0, 2):
            img = self.apply_contrast(img)
            # to hsv
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            img = self.apply_saturation(img)
            img = self.apply_hue(img)
            # to rgb
            img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        else:
            # to hsv
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            img = self.apply_saturation(img)
            img = self.apply_hue(img)
            # to rgb
            img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
            img = self.apply_contrast(img)

        if self.random_channel:
            if np.random.randint(0, 2):
                img = img[..., np.random.permutation(3)]
        sample['image'] = img
        
        # vis_2d_boxes_in_image(sample['image'], sample['bboxes'], sample['labels'], './c.png')
        return sample


class PadBox(BaseOperator):
    def __init__(self, num_max_boxes=50, inputs=None):
        """
        Pad zeros to bboxes if number of bboxes is less than num_max_boxes.
        Args:
            num_max_boxes (int): the max number of bboxes
        """
        self.num_max_boxes = num_max_boxes
        super(PadBox, self).__init__(inputs=inputs)

    def __call__(self, sample, context=None):
        assert 'gt_bbox' in sample
        bbox = sample['gt_bbox']
        gt_num = min(self.num_max_boxes, len(bbox))
        num_max = self.num_max_boxes
        fields = context['fields'] if context else []
        pad_bbox = np.zeros((num_max, 4), dtype=np.float32)
        if gt_num > 0:
            pad_bbox[:gt_num, :] = bbox[:gt_num, :]
        sample['gt_bbox'] = pad_bbox
        if 'gt_class' in fields:
            pad_class = np.zeros((num_max), dtype=np.int32)
            if gt_num > 0:
                pad_class[:gt_num] = sample['gt_class'][:gt_num, 0]
            sample['gt_class'] = pad_class
        if 'gt_score' in fields:
            pad_score = np.zeros((num_max), dtype=np.float32)
            if gt_num > 0:
                pad_score[:gt_num] = sample['gt_score'][:gt_num, 0]
            sample['gt_score'] = pad_score
        # in training, for example in op ExpandImage,
        # the bbox and gt_class is expandded, but the difficult is not,
        # so, judging by it's length
        if 'is_difficult' in fields:
            pad_diff = np.zeros((num_max), dtype=np.int32)
            if gt_num > 0:
                pad_diff[:gt_num] = sample['difficult'][:gt_num, 0]
            sample['difficult'] = pad_diff
        return sample


class BboxXYXY2XYWH(BaseOperator):
    """
    Convert bbox XYXY format to XYWH format.
    """

    def __init__(self, inputs=None):
        super(BboxXYXY2XYWH, self).__init__(inputs=inputs)

    def __call__(self, sample, context=None):
        assert 'gt_bbox' in sample
        bbox = sample['gt_bbox']
        bbox[:, 2:4] = bbox[:, 2:4] - bbox[:, :2]
        bbox[:, :2] = bbox[:, :2] + bbox[:, 2:4] / 2.
        sample['gt_bbox'] = bbox
        return sample


class Lighting(BaseOperator):
    """
    Lighting the imagen by eigenvalues and eigenvectors
    Args:
        eigval (list): eigenvalues
        eigvec (list): eigenvectors
        alphastd (float): random weight of lighting, 0.1 by default
    """

    def __init__(self, eigval, eigvec, alphastd=0.1, inputs=None):
        super(Lighting, self).__init__(inputs=inputs)
        self.alphastd = alphastd
        self.eigval = np.array(eigval).astype('float32')
        self.eigvec = np.array(eigvec).astype('float32')

    def __call__(self, sample, context=None):
        alpha = np.random.normal(scale=self.alphastd, size=(3, ))
        sample['image'] += np.dot(self.eigvec, self.eigval * alpha)
        return sample


class CornerTarget(BaseOperator):
    """
    Generate targets for CornerNet by ground truth data. 
    Args:
        output_size (int): the size of output heatmaps.
        num_classes (int): num of classes.
        gaussian_bump (bool): whether to apply gaussian bump on gt targets.
            True by default.
        gaussian_rad (int): radius of gaussian bump. If it is set to -1, the 
            radius will be calculated by iou. -1 by default.
        gaussian_iou (float): the threshold iou of predicted bbox to gt bbox. 
            If the iou is larger than threshold, the predicted bboox seems as
            positive sample. 0.3 by default
        max_tag_len (int): max num of gt box per image.
    """

    def __init__(self,
                 output_size,
                 num_classes,
                 gaussian_bump=True,
                 gaussian_rad=-1,
                 gaussian_iou=0.3,
                 max_tag_len=128,
                 inputs=None):
        super(CornerTarget, self).__init__(inputs=inputs)
        self.num_classes = num_classes
        self.output_size = output_size
        self.gaussian_bump = gaussian_bump
        self.gaussian_rad = gaussian_rad
        self.gaussian_iou = gaussian_iou
        self.max_tag_len = max_tag_len

    def __call__(self, sample, context=None):
        tl_heatmaps = np.zeros(
            (self.num_classes, self.output_size[0], self.output_size[1]),
            dtype=np.float32)
        br_heatmaps = np.zeros(
            (self.num_classes, self.output_size[0], self.output_size[1]),
            dtype=np.float32)

        tl_regrs = np.zeros((self.max_tag_len, 2), dtype=np.float32)
        br_regrs = np.zeros((self.max_tag_len, 2), dtype=np.float32)
        tl_tags = np.zeros((self.max_tag_len), dtype=np.int64)
        br_tags = np.zeros((self.max_tag_len), dtype=np.int64)
        tag_masks = np.zeros((self.max_tag_len), dtype=np.uint8)
        tag_lens = np.zeros((), dtype=np.int32)
        tag_nums = np.zeros((1), dtype=np.int32)

        gt_bbox = sample['gt_bbox']
        gt_class = sample['gt_class']
        keep_inds  = ((gt_bbox[:, 2] - gt_bbox[:, 0]) > 0) & \
                ((gt_bbox[:, 3] - gt_bbox[:, 1]) > 0)
        gt_bbox = gt_bbox[keep_inds]
        gt_class = gt_class[keep_inds]
        sample['gt_bbox'] = gt_bbox
        sample['gt_class'] = gt_class
        width_ratio = self.output_size[1] / sample['w']
        height_ratio = self.output_size[0] / sample['h']
        for i in range(gt_bbox.shape[0]):
            width = gt_bbox[i][2] - gt_bbox[i][0]
            height = gt_bbox[i][3] - gt_bbox[i][1]

            xtl, ytl = gt_bbox[i][0], gt_bbox[i][1]
            xbr, ybr = gt_bbox[i][2], gt_bbox[i][3]

            fxtl = (xtl * width_ratio)
            fytl = (ytl * height_ratio)
            fxbr = (xbr * width_ratio)
            fybr = (ybr * height_ratio)

            xtl = int(fxtl)
            ytl = int(fytl)
            xbr = int(fxbr)
            ybr = int(fybr)
            if self.gaussian_bump:
                width = math.ceil(width * width_ratio)
                height = math.ceil(height * height_ratio)
                if self.gaussian_rad == -1:
                    radius = gaussian_radius((height, width), self.gaussian_iou)
                    radius = max(0, int(radius))
                else:
                    radius = self.gaussian_rad
                draw_gaussian(tl_heatmaps[gt_class[i][0]], [xtl, ytl], radius)
                draw_gaussian(br_heatmaps[gt_class[i][0]], [xbr, ybr], radius)
            else:
                tl_heatmaps[gt_class[i][0], ytl, xtl] = 1
                br_heatmaps[gt_class[i][0], ybr, xbr] = 1

            tl_regrs[i, :] = [fxtl - xtl, fytl - ytl]
            br_regrs[i, :] = [fxbr - xbr, fybr - ybr]
            tl_tags[tag_lens] = ytl * self.output_size[1] + xtl
            br_tags[tag_lens] = ybr * self.output_size[1] + xbr
            tag_lens += 1

        tag_masks[:tag_lens] = 1

        sample['tl_heatmaps'] = tl_heatmaps
        sample['br_heatmaps'] = br_heatmaps
        sample['tl_regrs'] = tl_regrs
        sample['br_regrs'] = br_regrs
        sample['tl_tags'] = tl_tags
        sample['br_tags'] = br_tags
        sample['tag_masks'] = tag_masks

        return sample


class CornerCrop(BaseOperator):
    """
    Random crop for CornerNet
    Args:
        random_scales (list): scales of output_size to input_size.
        border (int): border of corp center
        is_train (bool): train or test
        input_size (int): size of input image
    """

    def __init__(self,
                 random_scales=[0.6, 0.7, 0.8, 0.9, 1., 1.1, 1.2, 1.3],
                 border=128,
                 is_train=True,
                 input_size=511, inputs=None):
        super(CornerCrop, self).__init__(inputs=inputs)
        self.random_scales = random_scales
        self.border = border
        self.is_train = is_train
        self.input_size = input_size

    def __call__(self, sample, context=None):
        im_h, im_w = int(sample['h']), int(sample['w'])
        if self.is_train:
            scale = np.random.choice(self.random_scales)
            height = int(self.input_size * scale)
            width = int(self.input_size * scale)

            w_border = self._get_border(self.border, im_w)
            h_border = self._get_border(self.border, im_h)

            ctx = np.random.randint(low=w_border, high=im_w - w_border)
            cty = np.random.randint(low=h_border, high=im_h - h_border)

        else:
            cty, ctx = im_h // 2, im_w // 2
            height = im_h | 127
            width = im_w | 127

        cropped_image = np.zeros(
            (height, width, 3), dtype=sample['image'].dtype)

        x0, x1 = max(ctx - width // 2, 0), min(ctx + width // 2, im_w)
        y0, y1 = max(cty - height // 2, 0), min(cty + height // 2, im_h)

        left_w, right_w = ctx - x0, x1 - ctx
        top_h, bottom_h = cty - y0, y1 - cty

        # crop image
        cropped_ctx, cropped_cty = width // 2, height // 2
        x_slice = slice(int(cropped_ctx - left_w), int(cropped_ctx + right_w))
        y_slice = slice(int(cropped_cty - top_h), int(cropped_cty + bottom_h))
        cropped_image[y_slice, x_slice, :] = sample['image'][y0:y1, x0:x1, :]

        sample['image'] = cropped_image
        sample['h'], sample['w'] = height, width

        if self.is_train:
            # crop detections
            gt_bbox = sample['gt_bbox']
            gt_bbox[:, 0:4:2] -= x0
            gt_bbox[:, 1:4:2] -= y0
            gt_bbox[:, 0:4:2] += cropped_ctx - left_w
            gt_bbox[:, 1:4:2] += cropped_cty - top_h
        else:
            sample['borders'] = np.array(
                [
                    cropped_cty - top_h, cropped_cty + bottom_h,
                    cropped_ctx - left_w, cropped_ctx + right_w
                ],
                dtype=np.float32)

        return sample

    def _get_border(self, border, size):
        i = 1
        while size - border // i <= border // i:
            i *= 2
        return border // i


class CornerRatio(BaseOperator):
    """
    Ratio of output size to image size
    Args:
        input_size (int): the size of input size
        output_size (int): the size of heatmap
    """

    def __init__(self, input_size=511, output_size=64, inputs=None):
        super(CornerRatio, self).__init__(inputs=inputs)
        self.input_size = input_size
        self.output_size = output_size

    def __call__(self, sample, context=None):
        scale = (self.input_size + 1) // self.output_size
        out_height, out_width = (sample['h'] + 1) // scale, (
            sample['w'] + 1) // scale
        height_ratio = out_height / float(sample['h'])
        width_ratio = out_width / float(sample['w'])
        sample['ratios'] = np.array([height_ratio, width_ratio])

        return sample


class RandomScaledCrop(BaseOperator):
    """Resize image and bbox based on long side (with optional random scaling),
       then crop or pad image to target size.
    Args:
        target_dim (int): target size.
        scale_range (list): random scale range.
        interp (int): interpolation method, default to `cv2.INTER_LINEAR`.
    """

    def __init__(self,
                 target_dim=512,
                 scale_range=[.1, 2.],
                 interp=cv2.INTER_LINEAR, inputs=None):
        super(RandomScaledCrop, self).__init__(inputs=inputs)
        self.target_dim = target_dim
        self.scale_range = scale_range
        self.interp = interp

    def __call__(self, sample, context=None):
        w = sample['w']
        h = sample['h']
        random_scale = np.random.uniform(*self.scale_range)
        dim = self.target_dim
        random_dim = int(dim * random_scale)
        dim_max = max(h, w)
        scale = random_dim / dim_max
        resize_w = int(round(w * scale))
        resize_h = int(round(h * scale))
        offset_x = int(max(0, np.random.uniform(0., resize_w - dim)))
        offset_y = int(max(0, np.random.uniform(0., resize_h - dim)))
        if 'gt_bbox' in sample and len(sample['gt_bbox']) > 0:
            scale_array = np.array([scale, scale] * 2, dtype=np.float32)
            shift_array = np.array([offset_x, offset_y] * 2, dtype=np.float32)
            boxes = sample['gt_bbox'] * scale_array - shift_array
            boxes = np.clip(boxes, 0, dim - 1)
            # filter boxes with no area
            area = np.prod(boxes[..., 2:] - boxes[..., :2], axis=1)
            valid = (area > 1.).nonzero()[0]
            sample['gt_bbox'] = boxes[valid]
            sample['gt_class'] = sample['gt_class'][valid]

        img = sample['image']
        img = cv2.resize(img, (resize_w, resize_h), interpolation=self.interp)
        img = np.array(img)
        canvas = np.zeros((dim, dim, 3), dtype=img.dtype)
        canvas[:min(dim, resize_h), :min(dim, resize_w), :] = img[
            offset_y:offset_y + dim, offset_x:offset_x + dim, :]
        sample['h'] = dim
        sample['w'] = dim
        sample['image'] = canvas
        sample['im_info'] = [resize_h, resize_w, scale]
        return sample


class DebugVisibleImage(BaseOperator):
    """
    In debug mode, visualize images according to `gt_box`.
    (Currently only supported when not cropping and flipping image.)
    """

    def __init__(self, output_dir='output/debug', is_normalized=False, inputs=None):
        super(DebugVisibleImage, self).__init__(inputs=inputs)
        self.is_normalized = is_normalized
        self.output_dir = output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        if not isinstance(self.is_normalized, bool):
            raise TypeError("{}: input type is invalid.".format(self))

    def __call__(self, sample, context=None):
        image = Image.open(sample['im_file']).convert('RGB')
        out_file_name = sample['im_file'].split('/')[-1]
        width = sample['w']
        height = sample['h']
        gt_bbox = sample['gt_bbox']
        gt_class = sample['gt_class']
        draw = ImageDraw.Draw(image)
        for i in range(gt_bbox.shape[0]):
            if self.is_normalized:
                gt_bbox[i][0] = gt_bbox[i][0] * width
                gt_bbox[i][1] = gt_bbox[i][1] * height
                gt_bbox[i][2] = gt_bbox[i][2] * width
                gt_bbox[i][3] = gt_bbox[i][3] * height

            xmin, ymin, xmax, ymax = gt_bbox[i]
            draw.line(
                [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin),
                 (xmin, ymin)],
                width=2,
                fill='green')
            # draw label
            text = str(gt_class[i][0])
            tw, th = draw.textsize(text)
            draw.rectangle(
                [(xmin + 1, ymin - th), (xmin + tw + 1, ymin)], fill='green')
            draw.text((xmin + 1, ymin - th), text, fill=(255, 255, 255))

        if 'gt_keypoint' in sample.keys():
            gt_keypoint = sample['gt_keypoint']
            if self.is_normalized:
                for i in range(gt_keypoint.shape[1]):
                    if i % 2:
                        gt_keypoint[:, i] = gt_keypoint[:, i] * height
                    else:
                        gt_keypoint[:, i] = gt_keypoint[:, i] * width
            for i in range(gt_keypoint.shape[0]):
                keypoint = gt_keypoint[i]
                for j in range(int(keypoint.shape[0] / 2)):
                    x1 = round(keypoint[2 * j]).astype(np.int32)
                    y1 = round(keypoint[2 * j + 1]).astype(np.int32)
                    draw.ellipse(
                        (x1, y1, x1 + 5, y1 + 5),
                        fill='green',
                        outline='green')
        save_path = os.path.join(self.output_dir, out_file_name)
        image.save(save_path, quality=95)
        return sample


#################       Segmentation Task   ##############################
class Padding(BaseOperator):
    """对图像或标注图像进行padding，padding方向为右和下。
    根据提供的值对图像或标注图像进行padding操作。

    Args:
        target_size (int|list|tuple): padding后图像的大小。
        im_padding_value (list): 图像padding的值。默认为[127.5, 127.5, 127.5]。
        label_padding_value (int): 标注图像padding的值。默认值为255。

    Raises:
        TypeError: target_size不是int|list|tuple。
        ValueError:  target_size为list|tuple时元素个数不等于2。
    """

    def __init__(self,
                 target_size,
                 im_padding_value=[127.5, 127.5, 127.5],
                 label_padding_value=255, inputs=None):
        super(Padding, self).__init__(inputs=inputs)
        if isinstance(target_size, list) or isinstance(target_size, tuple):
            if len(target_size) != 2:
                raise ValueError(
                    'when target is list or tuple, it should include 2 elements, but it is {}'
                    .format(target_size))
        elif not isinstance(target_size, int):
            raise TypeError(
                "Type of target_size is invalid. Must be Integer or List or tuple, now is {}"
                .format(type(target_size)))
        self.target_size = target_size
        self.im_padding_value = im_padding_value
        self.label_padding_value = label_padding_value

    def __call__(self, sample, context=None):
        im = sample['image']
        semantic = sample.get('semantic', None)
        im_height, im_width = im.shape[0], im.shape[1]
        if isinstance(self.target_size, int):
            target_height = self.target_size
            target_width = self.target_size
        else:
            target_height = self.target_size[1]
            target_width = self.target_size[0]
        pad_height = target_height - im_height
        pad_width = target_width - im_width
        if pad_height < 0 or pad_width < 0:
            raise ValueError(
                'the size of image should be less than target_size, but the size of image ({}, {}), is larger than target_size ({}, {})'
                .format(im_width, im_height, target_width, target_height))
        else:
            im = cv2.copyMakeBorder(
                im,
                pad_height//2,
                pad_height-pad_height//2,
                pad_width//2,
                pad_width-pad_width//2,
                cv2.BORDER_CONSTANT,
                value=self.im_padding_value)
            sample['image'] = im
            if semantic is not None:
                semantic = cv2.copyMakeBorder(
                    semantic,
                    pad_height//2,
                    pad_height-pad_height//2,
                    pad_width//2,
                    pad_width-pad_width//2,
                    cv2.BORDER_CONSTANT,
                    value=self.label_padding_value)
                sample['semantic'] = semantic
        return sample


class RandomPaddingCrop(BaseOperator):
    """对图像和标注图进行随机裁剪，当所需要的裁剪尺寸大于原图时，则进行padding操作。

    Args:
        crop_size (int|list|tuple): 裁剪图像大小。默认为512。
        im_padding_value (list): 图像padding的值。默认为[127.5, 127.5, 127.5]。
        label_padding_value (int): 标注图像padding的值。默认值为255。

    Raises:
        TypeError: crop_size不是int/list/tuple。
        ValueError:  target_size为list/tuple时元素个数不等于2。
    """
    def __init__(self,
                 crop_size=512,
                 im_padding_value=[127.5, 127.5, 127.5],
                 label_padding_value=255,
                 crop_width_random=[0.7, 1.3],
                 crop_height_random=[0.7, 1.3], inputs=None):
        super(RandomPaddingCrop, self).__init__(inputs=inputs)
        if isinstance(crop_size, list) or isinstance(crop_size, tuple):
            if len(crop_size) != 2:
                raise ValueError(
                    'when crop_size is list or tuple, it should include 2 elements, but it is {}'
                        .format(crop_size))
        elif not isinstance(crop_size, int):
            raise TypeError(
                "Type of crop_size is invalid. Must be Integer or List or tuple, now is {}"
                    .format(type(crop_size)))
        self.crop_size = crop_size
        self.im_padding_value = im_padding_value
        self.label_padding_value = label_padding_value
        self.crop_width_random = crop_width_random
        self.crop_height_random = crop_height_random

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

         Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
        """
        if isinstance(self.crop_size, int):
            crop_width = self.crop_size
            crop_height = self.crop_size
        else:
            crop_width = self.crop_size[0]
            crop_height = self.crop_size[1]
        im = sample['image']
        label = sample['semantic']
        img_height = im.shape[0]
        img_width = im.shape[1]

        if img_height == crop_height and img_width == crop_width:
            return sample
        else:
            # if img_width > img_height:
            #     # 宽屏数据
            #     crop_width = (int)((np.random.random() * 0.4 + 0.6) * crop_width)
            # else:
            crop_width = \
                (int)((np.random.random() * (self.crop_width_random[1] - self.crop_width_random[0]) +
                                    self.crop_width_random[0]) * crop_width)

            crop_height = \
                (int)((np.random.random() * (self.crop_height_random[1] - self.crop_height_random[0]) +
                                 self.crop_height_random[0]) * crop_height)

            is_focus = False
            crop_x = 0
            crop_y = 0
            if np.random.random() < 0.6:
                aabb = np.where(label > 0.5)
                if len(aabb[0]) > 0:
                    crop_height_try = np.max(aabb[0]) - np.min(aabb[0])
                    crop_width_try = np.max(aabb[1]) - np.min(aabb[1])
                    if crop_width_try < crop_height_try:
                        # 单人场景（多人场景width会比height大）
                        # 0.7 body_height ~ 1.4 body_height
                        crop_height = (int)(crop_height_try * (np.random.random() * 0.7 + 0.7))
                        # 0.8 body_width ~ 1.2 body_width
                        crop_width = (int)(crop_width_try * (np.random.random() * 0.4 + 0.8))

                        if crop_width > crop_height:
                            # 重新修正crop_height，保证竖屏模式
                            crop_height = (int)(crop_width * (np.random.random() * 0.5 + 1.0))

                        if crop_height > 1.8 * crop_width_try:
                            crop_height = (int)(1.8 * crop_width_try)

                        crop_x = np.min(aabb[1])
                        crop_y = np.min(aabb[0])

                        is_focus = True

            pad_height = (int)(max(crop_height - img_height, 0))
            pad_width = (int)(max(crop_width - img_width, 0))

            random_top_pad = (int)(np.random.random() * (pad_height))
            random_left_pad = (int)(np.random.random() * (pad_width))

            if np.random.random() < 0.5:
                if np.random.random() < 0.5:
                    random_left_pad = 0
                else:
                    random_left_pad = pad_width

                random_top_pad = pad_height
                # if np.random.random() < 0.5:
                #     random_top_pad = 0
                # else:
                #     random_top_pad = pad_height

            if (pad_height > 0 or pad_width > 0):
                im = cv2.copyMakeBorder(
                    im,
                    random_top_pad,
                    pad_height - random_top_pad,
                    random_left_pad,
                    pad_width - random_left_pad,
                    cv2.BORDER_CONSTANT,
                    value=self.im_padding_value)
                if label is not None:
                    label = cv2.copyMakeBorder(
                        label,
                        random_top_pad,
                        pad_height - random_top_pad,
                        random_left_pad,
                        pad_width - random_left_pad,
                        cv2.BORDER_CONSTANT,
                        value=self.label_padding_value)
                img_height = im.shape[0]
                img_width = im.shape[1]

            if crop_height > 0 and crop_width > 0:
                h_off = np.random.randint(img_height - crop_height + 1)
                w_off = np.random.randint(img_width - crop_width + 1)

                if is_focus:
                    h_off = (int)(np.random.randint(0, crop_y + random_top_pad + 1))
                    w_off = (int)(np.random.randint(crop_x + random_left_pad - (int)(crop_width * 0.5),
                                                    crop_x + random_left_pad + (int)(crop_width * 0.5)))
                    if w_off < 0:
                        w_off = 0
                    if w_off + crop_width >= img_width:
                        w_off = img_width - crop_width

                im = im[h_off:(crop_height + h_off), w_off:(
                    w_off + crop_width), :]

                if label is not None:
                    label = label[h_off:(crop_height + h_off), w_off:(
                        w_off + crop_width)]

        sample['image'] = im
        sample['semantic'] = label

        return sample


class RandomBlur(BaseOperator):
    """以一定的概率对图像进行高斯模糊。

    Args：
        prob (float): 图像模糊概率。默认为0.1。
    """

    def __init__(self, prob=0.1, inputs=None):
        super(RandomBlur, self).__init__(inputs=inputs)
        self.prob = prob

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

        Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
        """
        im = sample['image']
        if self.prob <= 0:
            n = 0
        elif self.prob >= 1:
            n = 1
        else:
            n = int(1.0 / self.prob)
        if n > 0:
            if np.random.randint(0, n) == 0:
                radius = np.random.randint(3, 10)
                if radius % 2 != 1:
                    radius = radius + 1
                if radius > 9:
                    radius = 9
                im = cv2.GaussianBlur(im, (radius, radius), 0, 0)

        return sample


class RandomMotionBlur(BaseOperator):
    def __init__(self, max_degree=10, max_angle=10, prob=0.5, inputs=None):
        super(RandomMotionBlur, self).__init__(inputs=inputs)
        self.max_degree = max_degree
        self.max_angle = max_angle
        self.prob = prob

    def motion_blur(self, image, degree=12, angle=45):
        image = np.array(image)

        # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
        M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
        motion_blur_kernel = np.diag(np.ones(degree))
        motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))

        motion_blur_kernel = motion_blur_kernel / degree
        blurred = cv2.filter2D(image, -1, motion_blur_kernel)

        # convert to uint8
        cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
        blurred = np.array(blurred, dtype=np.uint8)
        return blurred

    def __call__(self, sample, context=None):
        im = sample['image']
        if np.random.random() < self.prob:
            degree = np.random.randint(1, self.max_degree)
            angle = np.random.randint(-self.max_angle, self.max_angle)
            im = self.motion_blur(im, degree, angle)

        sample['image'] = im
        return sample


class GaussianNoise(BaseOperator):
    def __init__(self, noise_d=10, random_p=0.5, inputs=None):
        super(GaussianNoise, self).__init__(inputs=inputs)
        self.noise_d = noise_d
        self.random_p = random_p

    def __call__(self, sample, context=None):
        im = sample['image']
        if np.random.random() < self.random_p:
            im = im.astype(np.float)
            h,w,c = im.shape
            for ci in range(c):
                im[:,:,ci] = (np.random.random((h,w))*2-1) * self.noise_d + im[:,:,ci]
            im[np.where(im>255)] = 255
            im[np.where(im<0)] = 0

        sample['image'] = im
        return sample


class ResizeStepScaling(BaseOperator):
    """对图像按照某一个比例resize，这个比例以scale_step_size为步长
    在[min_scale_factor, max_scale_factor]随机变动。当存在标注图像时，则同步进行处理。

    Args:
        min_scale_factor（float), resize最小尺度。默认值0.75。
        max_scale_factor (float), resize最大尺度。默认值1.25。
        scale_step_size (float), resize尺度范围间隔。默认值0.25。

    Raises:
        ValueError: min_scale_factor大于max_scale_factor
    """

    def __init__(self,
                 min_scale_factor=0.75,
                 max_scale_factor=1.25,
                 scale_step_size=0.25,
                 inputs=None):
        super(ResizeStepScaling, self).__init__(inputs=inputs)
        if min_scale_factor > max_scale_factor:
            raise ValueError(
                'min_scale_factor must be less than max_scale_factor, '
                'but they are {} and {}.'.format(min_scale_factor,
                                                 max_scale_factor))
        self.min_scale_factor = min_scale_factor
        self.max_scale_factor = max_scale_factor
        self.scale_step_size = scale_step_size

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

        Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
        """
        im = sample['image']
        label = sample['semantic']
        if self.min_scale_factor == self.max_scale_factor:
            scale_factor = self.min_scale_factor

        elif self.scale_step_size == 0:
            scale_factor = np.random.uniform(self.min_scale_factor,
                                             self.max_scale_factor)

        else:
            num_steps = int((self.max_scale_factor - self.min_scale_factor) /
                            self.scale_step_size + 1)
            scale_factors = np.linspace(self.min_scale_factor,
                                        self.max_scale_factor,
                                        num_steps).tolist()
            np.random.shuffle(scale_factors)
            scale_factor = scale_factors[0]
        w = int(round(scale_factor * im.shape[1]))
        h = int(round(scale_factor * im.shape[0]))

        im = resize(im, (w, h), cv2.INTER_LINEAR)
        if label is not None:
            label = resize(label, (w, h), cv2.INTER_NEAREST)

        sample['image'] = im
        sample['semantic'] = label
        return sample


class ResizeRangeScaling(BaseOperator):
    """对图像长边随机resize到指定范围内，短边按比例进行缩放。当存在标注图像时，则同步进行处理。

    Args:
        min_value (int): 图像长边resize后的最小值。默认值400。
        max_value (int): 图像长边resize后的最大值。默认值600。

    Raises:
        ValueError: min_value大于max_value
    """

    def __init__(self, min_value=400, max_value=600, inputs=None):
        super(ResizeRangeScaling, self).__init__(inputs=inputs)
        if min_value > max_value:
            raise ValueError('min_value must be less than max_value, '
                             'but they are {} and {}.'.format(
                                 min_value, max_value))
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

        Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
        """
        im = sample['image']
        label = sample['semantic']
        if self.min_value == self.max_value:
            random_size = self.max_value
        else:
            random_size = int(
                np.random.uniform(self.min_value, self.max_value) + 0.5)
        im = resize_long(im, random_size, cv2.INTER_LINEAR)
        if label is not None:
            label = resize_long(label, random_size, cv2.INTER_NEAREST)

        sample['image'] = im
        sample['semantic'] = label
        return sample


class ResizeByLong(BaseOperator):
    """对图像长边resize到固定值，短边按比例进行缩放。当存在标注图像时，则同步进行处理。

    Args:
        long_size (int): resize后图像的长边大小。
    """

    def __init__(self, long_size, inputs=None):
        super(ResizeByLong, self).__init__(inputs=inputs)
        self.long_size = long_size

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

        Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
                其中，im_info新增字段为：
                    -shape_before_resize (tuple): 保存resize之前图像的形状(h, w）。
        """
        im = sample['image']
        label = sample['semantic']

        im = resize_long(im, self.long_size)
        if label is not None:
            label = resize_long(label, self.long_size, cv2.INTER_NEAREST)

        sample['image'] = im
        sample['semantic'] = label
        return sample

class ResizeByShort(BaseOperator):
    """对图像长边resize到固定值，短边按比例进行缩放。当存在标注图像时，则同步进行处理。

    Args:
        long_size (int): resize后图像的长边大小。
    """

    def __init__(self, short_size, inputs=None):
        super(ResizeByShort, self).__init__(inputs=inputs)
        self.short_size = short_size

    def __call__(self, sample, context=None):
        """
        Args:
            im (np.ndarray): 图像np.ndarray数据。
            im_info (dict): 存储与图像相关的信息。
            label (np.ndarray): 标注图像np.ndarray数据。

        Returns:
            tuple: 当label为空时，返回的tuple为(im, im_info)，分别对应图像np.ndarray数据、存储与图像相关信息的字典；
                当label不为空时，返回的tuple为(im, im_info, label)，分别对应图像np.ndarray数据、
                存储与图像相关信息的字典和标注图像np.ndarray数据。
                其中，im_info新增字段为：
                    -shape_before_resize (tuple): 保存resize之前图像的形状(h, w）。
        """
        im = sample['image']
        label = sample['semantic']

        im = resize_short(im, self.short_size)
        if label is not None:
            label = resize_short(label, self.short_size, cv2.INTER_NEAREST)

        sample['image'] = im
        sample['semantic'] = label
        return sample

