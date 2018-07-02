# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import numpy as np
import tensorflow as tf
import ClothesAnal as CAnal
import time
from operator import eq
#imagePath = '/tmp/test_chartreux.jpg'                                      # 추론을 진행할 이미지 경로
#modelFullPath = '/tmp/output_graph.pb'                                      # 읽어들일 graph 파일 경로
#labelsFullPath = '/tmp/output_labels.txt'                                   # 읽어들일 labels 파일 경로


def create_graph1(modelFullPath='/tmp/imagenet/output_graph.pb'):
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def ColorAnalysis(imagePath='/tmp/imagenet/Mywhite.jpg', modelFullPath='/tmp/imagenet/output_graph.pb' ,labelsFullPath='/tmp/imagenet/output_labels.txt'):
        answer = None

        if not tf.gfile.Exists(imagePath):
         tf.logging.fatal('File does not exist %s', imagePath)
         return answer

        image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
        create_graph1(modelFullPath)

        with tf.Session() as sess:

            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
            
            
        
        
        answer = labels[top_k[0]]
       
        
        if eq(answer,"b'gray'"):
            print("회색")
        elif eq(answer,"b'indigo'"):
            print("남색")
        elif eq(answer,"b'white'"):
            print("하얀색")
        elif eq(answer,"b'red'"):
            print("빨간색")
        elif eq(answer,"b'balck'"):
            print("검은색")
        elif eq(answer,"b'sky blue"):
            print("하늘색")
        elif eq(answer,"b'yellow"):
            print("노란색")
        elif eq(answer,"b'purple"):
            print("보라색")
        elif eq(answer,"b'orange"):
            print("주황색")


        
        
        return answer
        


        
    
def ClothesAnalysis():
    CAnal.main()
   
    
   

if __name__ == '__main__':
     ColorAnalysis()
     tf.reset_default_graph()
     CAnal.main()
     
    
   

   
   


  


