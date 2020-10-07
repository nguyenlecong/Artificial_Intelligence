#import tensorflow as tf

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

'''Xây dựng graph'''
x = tf.Variable(3, name="x")
y = tf.Variable(4, name="y")
z = tf.constant(2)

f = x*x*y + y + z
#f = x*x*y + y + 2
#f = tf.add(tf.add(tf.multiply(tf.multiply(x,x), y), y), 2)
'''Chạy mô hình'''
'''C1'''
sess = tf.Session()
sess.run(x.initializer)
sess.run(y.initializer)
result = sess.run(f)
print("==============")
print(result) #42
sess.close()

'''C2'''
# with tf.Session() as sess:
#     x.initializer.run()
#     y.initializer.run()
#     result = f.eval()
#     print(result)

'''khởi tạo tất cả các biến'''
# init = tf.global_variables_initializer()

# with tf.Session() as sess:
#     init.run()
#     result = f.eval()