#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Author zhang
import tensorflow as tf

import unicodedata
import re
import os
import io
import time
import numpy as np
from tqdm import tqdm
import time
from datetime import timedelta



def preprocess_sentence(w):

    w = w.rstrip().strip()

    # 给句子加上开始和结束标记
    # 以便模型知道何时开始和结束预测
    w = '<start> ' + w + ' <end>'
    return w

# 1. 去除重音符号
# 2. 清理句子
# 3. 返回这样格式的单词对：[source, target]
def create_dataset(path, num_examples):
    lines = io.open(path, encoding='UTF-8').read().strip().split('\n')

    word_pairs = [[preprocess_sentence(w) for w in l.split('#')]  for l in lines[:num_examples]]

    return zip(*word_pairs)   #分解出每个list

def max_length(tensor):
    return max(len(t) for t in tensor)

def tokenize(lang):
  lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(
      filters='')
  lang_tokenizer.fit_on_texts(lang)

  tensor = lang_tokenizer.texts_to_sequences(lang)

  tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor,
                                                         padding='post') #默认取值最长

  return tensor, lang_tokenizer

def load_dataset(path, num_examples=None):
    # 创建清理过的输入输出对
    inpuit_text, targ_text = create_dataset(path, num_examples)

    input_tensor, input_tokenizer = tokenize(inpuit_text)
    target_tensor, targ_tokenizer = tokenize(targ_text)

    return input_tensor, target_tensor, input_tokenizer, targ_tokenizer



def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))

