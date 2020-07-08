# -*- coding: utf-8 -*-
"""Alzheimer_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1912E7kyVO3vleAAX-T-mARe8dHFCBisr
"""

from google.colab import drive
drive.mount('/content/drive')

"""**Importing the libraries.**"""

# Commented out IPython magic to ensure Python compatibility.
#For display.
# %matplotlib inline

# For GPU proecessing.
import torch

import tensorflow as tf

!curl -s https://course.fast.ai/setup/colab | bash
!pip install git+https://github.com/mogwai/fastai_audio.git@0.1

from torchvision.models import resnet34, resnet50 #Deep Learning models

import torchaudio

from torchaudio import transforms

from IPython.display import Audio

import numpy as np

# For Processing the audio.
import fastai
from fastai.imports import *
from fastai.basics import *
from fastai.metrics import accuracy
from fastai.torch_core import *
from fastai.vision import *
fastai.__version__

from fastai import *

from audio import *  
from fastai.basics import *

# Loading the Dataset.
train_dataset_path = Path('/content/drive/My Drive/ADReSS-IS2020-data/train/Full_wave_enhanced_audio')
control_path = dataset_path/'control'
dementia_path = dataset_path/'Dementia'

"""**Pre-Processing**"""

# Sorting the data into two classes (Control and Dementia)
label_pat = r'/(control|Dementia)'

# Test Data Directory where test audio is stored
Test_data_directory = '/content/drive/My Drive/ADReSS-IS2020-data/train/test_cd'

# Speech Augmentation on Training Data.
config_Train = AudioConfig()
config_Train.downmix = True # Converting into Mono audio.
config_Train.resample_to = 44100 # Resample the audio in a particular sampling rate.
config_Train.segment_size = 60000 # Restricting the audio length to 60sec.
config_Train.f_max = 22050 
config_Train.cache = False
config_Train.max_to_pad = 60000 # If the audio length is not 60sec then pad the audio so that length become 60sec.
config_Train.cache = False

# Converting the training audio according to the augmentation need.
audio_data = AudioList.from_folder(path=dataset_path, config = config_Train).split_by_rand_pct(.2, seed=4).label_from_re(label_pat).databunch(bs=8)



# Speech Augmentation on Test Data.
config_Test = AudioConfig()
config_Test.downmix = True # Converting the audio into Mono tone.
config_Test.resample_to = 44100 # Resample the audio in a particular sampling rate(44100)
config_Test.max_to_pad = 60000 # If the audio length is not 60sec then pad the audio so that length become 60sec.
config_Test.segment_size = 60000 # Restricting the audio length to 60sec.

# Converting the test data according to the augmentation need.
test_data = AudioList.from_folder(path = Test_data_directory, config = config_Test )

test_data

# Adding the test data to training set.
# Here the label of test data is set to None.
audio_data.add_test(test_data)

# Overview 
audio_data

"""**Initialise the Deep Learning Model**"""

# Initialize GPU for processing.
audio_data.device = torch.device('cuda')

# Fitting the audio data to the model.
# Here we are using Resenet18 pre-trained model for classification.
learner = audio_learner(audio_data)

"""**Fits the model**"""

# Model processing.
learner.fit_one_cycle(1)

"""**Prediction**"""

# Getting the class of test data.
# Here 0.0: There are no symptoms of Dementia in the audio.
# Here 1.0: Audio shows the symptoms of Dementia.
classes = learner.validate(audio_data.test_dl)

result = (classes[0].astype(int))*100

if result == 0:
  print("The audio shows the symptoms of Dementia")
else:
  print("The audio does not show the symptoms of Dementia")