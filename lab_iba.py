# -*- coding: utf-8 -*-
"""lab_IBA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tBFdYqGlb-I992iTSGpXomYkVXqrmL3J

Есть N бандитов, для каждого есть число -100<x<100, которое подаётся на вход функции pullBandit
def pullBandit(bandit): #Сгенерировать случайное число
   result = np.random.randn(1) 
   if result > bandit: #Выигрыш 
        return 1 
   else: #Проигрыш 
        return -1
Значение результата используется в качестве награды.
Политика RL: policy gradient (лучше если это будет vanilla, без модификаций)
Задача найти номер лучшего бандита
"""

import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

bandits = [0.2,-0.1,-0.2,-5]
#bandits = [0.2,-3,-0.2,-5] 
#при примерно равных 2 и 4 стабильно отлает предпочтение 2ому
#немного лечится увеличением рандома параметром е (который в начале вообще хотел выпилить) но это вносит бОльший шанс ошибки "не-2" (например выберет 3)
num_bandits = len(bandits)
def pullBandit(bandit): #Сгенерировать случайное число
    result = np.random.randn(1)
    if result > bandit: #Выигрыш
        return 1
    else: #Проигрыш
        return -1

tf.reset_default_graph()

weights = tf.Variable(tf.ones([num_bandits]))
chosen_action = tf.argmax(weights,0)


reward_holder = tf.placeholder(shape=[1],dtype=tf.float32)
action_holder = tf.placeholder(shape=[1],dtype=tf.int32)
responsible_weight = tf.slice(weights,action_holder,[1])
loss = -(tf.log(responsible_weight)*reward_holder)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
update = optimizer.minimize(loss)

total_episodes = 1000 
total_reward = np.zeros(num_bandits) 
e = 0.3

init = tf.initializers.global_variables()

with tf.Session() as sess:
    sess.run(init)
    i = 0
    while i < total_episodes: 
       # рандом, который необходим для хоть какого-то выхода из ситуаций с примерно равными значениями
        if np.random.rand(1) < e:
            action = np.random.randint(num_bandits)
        else:
            action = sess.run(chosen_action)
        
        reward = pullBandit(bandits[action]) 
        
        _,resp,ww = sess.run([update,responsible_weight,weights], feed_dict={reward_holder:[reward],action_holder:[action]})
        
        total_reward[action] += reward
        if i % 50 == 0:
            print ("Step "+str(i)+" current points:"+ str(total_reward))
        i+=1
print (str(np.argmax(ww)+1))

