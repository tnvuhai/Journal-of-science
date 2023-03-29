import keras
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt


data_path = 'train'

directories = ['/Closed', '/Open']


batch_size = 128
train_datagen = ImageDataGenerator(horizontal_flip = True,
                                  rescale = 1./255,
                                  zoom_range = 0.2,
                                  validation_split = 0.1)

test_datagen = ImageDataGenerator(rescale = 1./255)

train_data_path = 'train'
test_data_path = 'test'

train_set = train_datagen.flow_from_directory(train_data_path, target_size = (24,24),
                                              batch_size = batch_size,
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_data_path, target_size = (24,24),
                                              batch_size = batch_size,
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')

classes = 2

model = Sequential()
model.add(Conv2D(32, (3,3), padding = 'same', input_shape = (24,24,1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(64, (3,3), padding = 'same', activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(128,(3,3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(64, activation = 'relu'))

model.add(Dense(classes, activation = 'softmax'))

print(model.summary())

model.compile(loss = 'categorical_crossentropy',optimizer = 'adam' , metrics = ['accuracy'])

model_path="yawn_detection1.h5"

checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', verbose=1,
                              save_best_only=True, mode='max')

callbacks_list = [checkpoint]

num_epochs = 10
training_steps=train_set.n//train_set.batch_size
validation_steps =test_set.n//test_set.batch_size

history = model.fit(train_set, epochs=num_epochs, steps_per_epoch=training_steps,validation_data=test_set,
                    validation_steps=validation_steps, callbacks = callbacks_list)
