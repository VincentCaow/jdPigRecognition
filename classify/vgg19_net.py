#!/usr/bin/Python
# -*- coding: utf-8 -*-
import os
import sys
import math
import numpy as np
import tensorflow as tf

# 将运行路径切换到当前文件所在路径
cur_dir_path = os.path.abspath(os.path.split(__file__)[0])
if cur_dir_path:
    os.chdir(cur_dir_path)
    sys.path.append(cur_dir_path)
    sys.path.append(os.path.split(cur_dir_path)[0])

import load
import lib.base as base
import model.vgg as vgg

''' 全卷积神经网络 '''


class VGG19(base.NN):
    MODEL_NAME = 'vgg_19'  # 模型的名称

    ''' 参数的配置 '''

    BATCH_SIZE = 16  # 迭代的 epoch 次数
    EPOCH_TIMES = 100  # 随机梯度下降的 batch 大小

    NUM_CHANNEL = 3  # 输入图片为 3 通道，彩色
    NUM_CLASSES = 30  # 输出的类别

    # 学习率的相关参数
    BASE_LEARNING_RATE = 0.00000005  # 初始 学习率
    DECAY_RATE = 0.0001  # 学习率 的 下降速率

    # 防止 overfitting 相关参数
    REGULAR_BETA = 0.02  # 正则化的 beta 参数
    KEEP_PROB = 0.5  # dropout 的 keep_prob

    # early stop
    MAX_VAL_ACCURACY_DECR_TIMES = 20  # 校验集 val_accuracy 连续 100 次没有降低，则 early stop

    # 保存模型时 校验集准确率 与 训练集准确率的占比: accuracy = val_accuracy * VAL_WEIGHT + train_accuracy * (1 - VAL_WEIGHT)
    VAL_WEIGHT = 0.7

    ''' 类的配置 '''

    USE_BN = True  # 网络里是否使用了 batch normalize
    USE_BN_INPUT = True  # 输入是否使用 batch normalize

    SHOW_PROGRESS_FREQUENCY = 10  # 每 SHOW_PROGRESS_FREQUENCY 个 step show 一次进度 progress

    ''' 模型的配置；采用了 VGG19 模型的 FCN '''

    LOSS_TYPE = 0  # loss type 有两种；0：使用正常的loss，1：使用log_loss

    IMAGE_SHAPE = [56, 56]
    IMAGE_PH_SHAPE = [None, IMAGE_SHAPE[0], IMAGE_SHAPE[1], NUM_CHANNEL]  # image 的 placeholder 的 shape

    VGG_MODEL = vgg.VGG.load(True)  # 加载 VGG 模型

    MODEL = [
        {
            'name': 'conv1_1',
            'type': 'conv',
            'W': VGG_MODEL['conv1_1'][0],
            'b': VGG_MODEL['conv1_1'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv1_2',
            'type': 'conv',
            'W': VGG_MODEL['conv1_2'][0],
            'b': VGG_MODEL['conv1_2'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'pool_1',
            'type': 'pool',
            'k_size': 2,
            'pool_type': 'avg',
        },
        {
            'name': 'conv2_1',
            'type': 'conv',
            'W': VGG_MODEL['conv2_1'][0],
            'b': VGG_MODEL['conv2_1'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv2_2',
            'type': 'conv',
            'W': VGG_MODEL['conv2_2'][0],
            'b': VGG_MODEL['conv2_2'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'pool_2',
            'type': 'pool',
            'k_size': 2,
            'pool_type': 'avg',
        },
        {
            'name': 'conv3_1',
            'type': 'conv',
            'W': VGG_MODEL['conv3_1'][0],
            'b': VGG_MODEL['conv3_1'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv3_2',
            'type': 'conv',
            'W': VGG_MODEL['conv3_2'][0],
            'b': VGG_MODEL['conv3_2'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv3_3',
            'type': 'conv',
            'W': VGG_MODEL['conv3_3'][0],
            'b': VGG_MODEL['conv3_3'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv3_4',
            'type': 'conv',
            'W': VGG_MODEL['conv3_4'][0],
            'b': VGG_MODEL['conv3_4'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'pool_3',
            'type': 'pool',
            'k_size': 2,
            'pool_type': 'avg',
        },
        {
            'name': 'conv4_1',
            'type': 'conv',
            'W': VGG_MODEL['conv4_1'][0],
            'b': VGG_MODEL['conv4_1'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv4_2',
            'type': 'conv',
            'W': VGG_MODEL['conv4_2'][0],
            'b': VGG_MODEL['conv4_2'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv4_3',
            'type': 'conv',
            'W': VGG_MODEL['conv4_3'][0],
            'b': VGG_MODEL['conv4_3'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv4_4',
            'type': 'conv',
            'W': VGG_MODEL['conv4_4'][0],
            'b': VGG_MODEL['conv4_4'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'pool_4',
            'type': 'pool',
            'k_size': 2,
            'pool_type': 'avg',
        },
        {
            'name': 'conv5_1',
            'type': 'conv',
            'W': VGG_MODEL['conv5_1'][0],
            'b': VGG_MODEL['conv5_1'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv5_2',
            'type': 'conv',
            'W': VGG_MODEL['conv5_2'][0],
            'b': VGG_MODEL['conv5_2'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv5_3',
            'type': 'conv',
            'W': VGG_MODEL['conv5_3'][0],
            'b': VGG_MODEL['conv5_3'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'conv5_4',
            'type': 'conv',
            'W': VGG_MODEL['conv5_4'][0],
            'b': VGG_MODEL['conv5_4'][1],
            'bn': True,
            'trainable': False,
        },
        {
            'name': 'pool_5',
            'type': 'pool',
            'k_size': 2,
            'pool_type': 'max',
        },
        {
            'name': 'fc6',
            'type': 'fc',
            # 'shape': [2048, 1024],
            'filter_out': 1024,
            'trainable': True,
        },
        {
            'name': 'dropout_6',
            'type': 'dropout',
        },
        {
            'name': 'fc7',
            'type': 'fc',
            # 'shape': [1024, 512],
            'filter_out': 512,
            'trainable': True,
        },
        {
            'name': 'dropout_7',
            'type': 'dropout',
        },
        {
            'name': 'fc8',
            'type': 'fc',
            # 'shape': [512, 256],
            'filter_out': 256,
            'trainable': True,
        },
        {
            'name': 'softmax',
            'type': 'fc',
            # 'shape': [256, NUM_CLASSES],
            'filter_out': NUM_CLASSES,
            'activate': False,
        },
    ]

    ''' 自定义 初始化变量 过程 '''

    def init(self):
        # 加载数据
        self.load()

        # 常量
        self.__iter_per_epoch = int(self.__train_size // self.BATCH_SIZE)
        self.__steps = self.EPOCH_TIMES * self.__iter_per_epoch

        # 输入 与 label
        self.__image = tf.placeholder(tf.float32, self.IMAGE_PH_SHAPE, name='X')
        self.__label = tf.placeholder(tf.float32, [None, self.NUM_CLASSES], name='y')
        self.__size = tf.placeholder(tf.float32, name='size')

        # dropout 的 keep_prob
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        # 随训练次数增多而衰减的学习率
        self.__learning_rate = self.get_learning_rate(
            self.BASE_LEARNING_RATE, self.global_step, self.__steps, self.DECAY_RATE, staircase=False
        )

        self.__has_rebuild = False

    ''' 加载数据 '''

    def load(self):
        self.__train_set = load.Data(0.0, 0.8, 'train', self.IMAGE_SHAPE)
        self.__val_set = load.Data(0.8, 1.0, 'validation', self.IMAGE_SHAPE)
        # self.__test_set = load.Data(0.8, 1.0, 'test')

        self.__train_set.start_thread()
        self.__val_set.start_thread()

        self.__train_size = self.__train_set.get_size()
        self.__val_size = self.__val_set.get_size()
        # self.__test_size = self.__test_set.get_size()

    ''' 模型 '''

    def model(self):
        if self.start_from_model:
            self.restore_model_w_b(self.start_from_model)
            self.rebuild_model()
        else:
            self.__output = self.parse_model(self.__image)

    ''' 重建模型 '''

    def rebuild_model(self):
        self.__output = self.parse_model_rebuild(self.__image)

    ''' 计算 loss '''

    def get_loss(self):
        with tf.name_scope('loss'):
            self.__loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits=self.__output, labels=self.__label)
            )

    ''' 将图片输出到 tensorboard '''

    def __summary(self):
        with tf.name_scope('summary'):
            self.__mean_accuracy = tf.placeholder(tf.float32, name='mean_accuracy')
            self.__mean_loss = tf.placeholder(tf.float32, name='mean_loss')
            self.__mean_log_loss = tf.placeholder(tf.float32, name='mean_log_loss')

            tf.summary.scalar('learning_rate', self.__learning_rate)
            tf.summary.scalar('mean_accuracy', self.__mean_accuracy)
            tf.summary.scalar('mean_loss', self.__mean_loss)
            tf.summary.scalar('mean_log_loss', self.__mean_log_loss)

    def __get_accuracy(self):
        with tf.name_scope('accuracy'):
            labels = tf.argmax(self.__label, 1)
            predict = tf.argmax(self.__output, 1)
            correct = tf.equal(labels, predict)  # 返回 predict 与 labels 相匹配的结果

            self.__accuracy = tf.divide(tf.reduce_sum(tf.cast(correct, tf.float32)), self.__size)  # 计算准确率

    def __get_log_loss(self):
        with tf.name_scope('log_loss'):
            exp_x = tf.transpose(tf.exp(self.__output))
            prob = tf.transpose(exp_x / tf.reduce_sum(exp_x, axis=0))
            p = tf.maximum(tf.minimum(prob, 1 - 1e-15), 1e-15)
            self.__log_loss = - tf.divide(tf.reduce_sum(tf.multiply(self.__label, tf.log(p))), self.__size)

    def __measure(self, data_set, max_times=None):
        times = int(math.ceil(float(data_set.get_size()) / self.BATCH_SIZE))
        if max_times:
            times = min(max_times, times)

        mean_accuracy = 0
        mean_loss = 0
        mean_log_loss = 0
        for i in range(times):
            batch_x, batch_y = data_set.next_batch(self.BATCH_SIZE)

            batch_x = (batch_x - self.mean_x) / (self.std_x + self.EPSILON)

            feed_dict = {self.__image: batch_x, self.__label: batch_y,
                         self.__size: batch_y.shape[0], self.keep_prob: 1.0, self.t_is_train: False}
            loss, log_loss, accuracy = self.sess.run([self.__loss, self.__log_loss, self.__accuracy], feed_dict)
            mean_accuracy += accuracy
            mean_loss += loss
            mean_log_loss += log_loss

            del batch_x
            del batch_y

            progress = float(i + 1) / times * 100
            self.echo('\r >> measuring progress: %.2f%% | %d \t' % (progress, times), False)

        return mean_accuracy / times, mean_loss / times, mean_log_loss / times

    ''' 主函数 '''

    def run(self):
        # 生成模型
        self.model()

        # 计算 loss
        self.get_loss()

        self.__get_log_loss()

        # 正则化
        if self.LOSS_TYPE == 0:
            loss_regular = self.regularize_trainable(self.__loss, self.REGULAR_BETA)
        else:
            loss_regular = self.regularize_trainable(self.__log_loss, self.REGULAR_BETA)

        # 生成训练的 op
        train_op = self.get_train_op(loss_regular, self.__learning_rate, self.global_step)

        self.__get_accuracy()

        # # tensorboard 相关记录
        self.__summary()

        # 初始化所有变量
        self.init_variables()

        # TensorBoard merge summary
        self.merge_summary()

        mean_train_loss = 0
        mean_train_log_loss = 0
        mean_train_accuracy = 0

        mean_val_accuracy, mean_val_loss, mean_val_log_loss = self.__measure(self.__val_set)

        best_val_log_loss = mean_val_log_loss
        best_val_accuracy = mean_val_accuracy
        incr_val_log_loss_times = 0

        self.echo('\n best val_accuracy: %.6f  val_loss: %.6f  val_log_loss: %.6f  ' % (mean_val_accuracy,
                                                                                        mean_val_loss,
                                                                                        mean_val_log_loss))

        if self.start_from_model:
            self.get_new_model()  # 将模型保存到新的 model

        self.save_model_w_b()

        self.echo('\nepoch:')

        moment = 0.975
        self.__running_mean = None
        self.__running_std = None

        for step in range(self.__steps):
            if step % self.SHOW_PROGRESS_FREQUENCY == 0:
                epoch_progress = float(step) % self.__iter_per_epoch / self.__iter_per_epoch * 100.0
                step_progress = float(step) / self.__steps * 100.0
                self.echo('\r step: %d (%d|%.2f%%) / %d|%.2f%% \t\t' % (step, self.__iter_per_epoch, epoch_progress,
                                                                        self.__steps, step_progress), False)

            batch_x, batch_y = self.__train_set.next_batch(self.BATCH_SIZE)

            reduce_axis = tuple(range(len(batch_x.shape) - 1))
            _mean = np.mean(batch_x, axis=reduce_axis)
            _std = np.std(batch_x, axis=reduce_axis)
            self.__running_mean = moment * self.__running_mean + (1 - moment) * _mean if not isinstance(
                self.__running_mean, type(None)) else _mean
            self.__running_std = moment * self.__running_std + (1 - moment) * _std if not isinstance(
                self.__running_std, type(None)) else _std
            batch_x = (batch_x - _mean) / (_std + self.EPSILON)

            feed_dict = {self.__image: batch_x, self.__label: batch_y, self.keep_prob: self.KEEP_PROB,
                         self.__size: batch_y.shape[0], self.t_is_train: True}

            _, train_loss, train_log_loss, train_accuracy = self.sess.run(
                [train_op, self.__loss, self.__log_loss, self.__accuracy], feed_dict)

            mean_train_accuracy += train_accuracy
            mean_train_loss += train_loss
            mean_train_log_loss += train_log_loss

            if step % self.__iter_per_epoch == 0 and step != 0:
                epoch = int(step // self.__iter_per_epoch)
                self.mean_x = self.__running_mean
                self.std_x = self.__running_std * (self.BATCH_SIZE / float(self.BATCH_SIZE - 1))

                mean_train_accuracy /= self.__iter_per_epoch
                mean_train_loss /= self.__iter_per_epoch
                mean_train_log_loss /= self.__iter_per_epoch

                feed_dict[self.__mean_accuracy] = mean_train_accuracy
                feed_dict[self.__mean_loss] = mean_train_loss
                feed_dict[self.__mean_log_loss] = mean_train_log_loss
                self.add_summary_train(feed_dict, epoch)

                del batch_x
                del batch_y

                # 测试 校验集 的 loss
                mean_val_accuracy, mean_val_loss, mean_val_log_loss = self.__measure(self.__val_set, 20)
                batch_val_x, batch_val_y = self.__val_set.next_batch(self.BATCH_SIZE)

                batch_val_x = (batch_val_x - self.mean_x) / (self.std_x + self.EPSILON)

                feed_dict = {self.__image: batch_val_x, self.__label: batch_val_y, self.keep_prob: 1.0,
                             self.__size: batch_val_y.shape[0], self.__mean_accuracy: mean_val_accuracy,
                             self.__mean_loss: mean_val_loss, self.__mean_log_loss: mean_val_log_loss,
                             self.t_is_train: False}
                self.add_summary_val(feed_dict, epoch)

                del batch_val_x
                del batch_val_y

                echo_str = '\n\t epoch: %d  train_loss: %.6f  train_log_loss: %.6f  train_accuracy: %.6f  ' \
                           'val_loss: %.6f val_log_loss: %.6f  val_accuracy: %.6f' % (epoch, mean_train_loss,
                                                                                      mean_train_log_loss,
                                                                                      mean_train_accuracy,
                                                                                      mean_val_loss, mean_val_log_loss,
                                                                                      mean_val_accuracy)

                mean_train_accuracy = 0
                mean_train_loss = 0

                condition_yes = False
                if self.LOSS_TYPE == 0:
                    mean_accuracy = self.VAL_WEIGHT * mean_val_accuracy + (1 - self.VAL_WEIGHT) * mean_train_accuracy
                    if best_val_accuracy < mean_accuracy:
                        best_val_accuracy = mean_accuracy
                        condition_yes = True
                else:
                    mean_log_loss = self.VAL_WEIGHT * mean_val_log_loss + (1 - self.VAL_WEIGHT) * mean_train_log_loss
                    if best_val_log_loss > mean_log_loss:
                        best_val_log_loss = mean_log_loss
                        condition_yes = True

                if condition_yes:
                    incr_val_log_loss_times = 0

                    self.echo('%s  best  ' % echo_str, False)
                    self.save_model_w_b()

                else:
                    incr_val_log_loss_times += 1
                    self.echo('%s  incr_times: %d \n' % (echo_str, incr_val_log_loss_times), False)

                    if incr_val_log_loss_times > self.MAX_VAL_ACCURACY_DECR_TIMES:
                        break

            else:
                del batch_x
                del batch_y

        self.close_summary()  # 关闭 TensorBoard

        # self.__test_set.start_thread()

        self.restore_model_w_b()  # 恢复模型
        self.rebuild_model()  # 重建模型
        self.get_loss()  # 重新 get loss
        self.__get_accuracy()
        self.__get_log_loss()

        self.init_variables()  # 重新初始化变量

        mean_train_accuracy, mean_train_loss, mean_train_log_loss = self.__measure(self.__train_set)
        mean_val_accuracy, mean_val_loss, mean_val_log_loss = self.__measure(self.__val_set)
        # mean_test_accuracy, mean_test_loss, mean_test_log_loss = self.__measure(self.__test_set)

        self.echo('train_accuracy: %.6f  train_loss: %.6f  train_log_loss: %.6f  ' % (mean_train_accuracy,
                                                                                      mean_train_loss,
                                                                                      mean_train_log_loss))
        self.echo('val_accuracy: %.6f  val_loss: %.6f  val_log_loss: %.6f  ' % (mean_val_accuracy,
                                                                                mean_val_loss, mean_val_log_loss))
        # self.echo('test_accuracy: %.6f  test_loss: %.6f  test_log_loss: %.6f  ' % (mean_test_accuracy,
        #                                                             mean_test_loss, mean_test_log_loss))

        self.__train_set.stop()  # 关闭获取数据线程
        self.__val_set.stop()  # 关闭获取数据线程
        # self.__test_set.stop()  # 关闭获取数据线程

        self.echo('\ndone')

    def use_model(self, np_image):
        if not self.__has_rebuild:
            self.restore_model_w_b()  # 恢复模型
            self.rebuild_model()  # 重建模型
            self.get_loss()  # 重新 get loss
            self.__get_accuracy()
            self.__get_log_loss()

            self.init_variables()  # 初始化所有变量
            self.__has_rebuild = True

        np_image = np.expand_dims(np_image, axis=0)

        np_image = (np_image - self.mean_x) / (self.std_x + self.EPSILON)

        feed_dict = {self.__image: np_image, self.keep_prob: 1.0, self.t_is_train: False}
        output = self.sess.run(self.__output, feed_dict)

        return output[0]

    def test(self):

        self.restore_model_w_b()  # 恢复模型
        self.rebuild_model()  # 重建模型

        self.get_loss()  # 重新 get loss
        self.__get_accuracy()
        self.__get_log_loss()

        self.echo('init_variables ... ')

        self.init_variables()  # 重新初始化变量
        self.__has_rebuild = True

        mean_train_accuracy, mean_train_loss, mean_train_log_loss = self.__measure(self.__train_set, 100)
        mean_val_accuracy, mean_val_loss, mean_val_log_loss = self.__measure(self.__val_set, 100)

        self.echo('\ntrain_accuracy: %.6f  train_loss: %.6f  train_log_loss: %.6f  \n' % (mean_train_accuracy,
                                                                                          mean_train_loss,
                                                                                          mean_train_log_loss))
        self.echo('\nval_accuracy: %.6f  val_loss: %.6f  val_log_loss: %.6f  ' % (mean_val_accuracy,
                                                                                  mean_val_loss, mean_val_log_loss))

        self.__train_set.stop()
        self.__val_set.stop()

        self.echo('\ndone')


o_vgg = VGG19(False, '2018_01_12_20_58_18')
o_vgg.run()
# o_vgg.test()
