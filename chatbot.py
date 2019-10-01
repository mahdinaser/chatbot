import json
import pandas as pd
import gzip
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

filename = 'opiates_0.txt'

SENTENCE_ENCODER_LARGE_ = "https://tfhub.dev/google/universal-sentence-encoder-large/3"

module_url = SENTENCE_ENCODER_LARGE_

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  import json
  with open('opiates_0.txt') as json_file:
    data = json.load(json_file)

  collection = []
  for d in data['opiates']:
      for item in d:
          value = d.get(item)[0]
          question = value.get('0_title')
          comments = value['comments'][0]
          answerlist=[]
          for comment in comments:
            answer = comments.get(comment)
            answerlist.append(answer)
          collection.append([question,answerlist[0]])


  # Create the pandas DataFrame
  df = pd.DataFrame(collection, columns=['question', 'answer'])

  return df


def init():
    global query, messages, reply,message_embeddings ,tf, embed ,graph
  #  print('Start the initialization ')
    df = getDF('%s' % filename)
    # Import the Universal Sentence Encoder's TF Hub module
    #embed = hub.Module(module_url)
    # Compute a representation for each message, showing various lengths supported.

    questionList = df['question'].astype(str).values.tolist()
    answerList = df['answer'].astype(str).values.tolist()

   # print('total questions',len(questionList),' total answers',len(answerList))

    messages = questionList
    reply = answerList
    tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.ERROR)



  #  print("start to load the model")
    graph = tf.Graph()

    with tf.Session(graph=graph) as session:
   # with tf.Session() as session:
        embed = hub.Module("%s" % SENTENCE_ENCODER_LARGE_)
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(messages))

   # print("initialization is over")



# Reduce logging output.


def cosine_similarity(v1, v2):
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2[0])
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1, v2[0]) / (mag1 * mag2)


def getChatResponse(query):
  #  print(query)

    with tf.Session(graph=graph) as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        query_embeddings = session.run(embed([query]))

    result = [cosine_similarity(x, query_embeddings) for x in message_embeddings]

  #  print(messages[np.argmax(result)])
    return (reply[np.argmax(result)])

if __name__ == '__main__':
  init()