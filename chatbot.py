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
import glob
import os
import tensorflow as tf
import numpy as np
import os.path
from os import path

DATA_FILE = 'embedding.dat.npy'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

filename = 'opiates_0.txt'

SENTENCE_ENCODER_LARGE_ = "model/3"
SENTENCE_ENCODER_MEDIUM = "model/2"
module_url = SENTENCE_ENCODER_MEDIUM

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
modelInitialize = False
def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):

  path ="data"  # use your path
  all_files = glob.glob(path + "/opiates*.txt")

  li = []

  for filename in all_files:
      df2 = pd.read_csv(filename, index_col=None, header=0)
      li.append(df2)

  df = pd.concat(li, axis=0, ignore_index=True)
  df = df.groupby(['question'])['answer'].apply(lambda x: '||'.join(x)).reset_index()

  return df


def init():
    global query, listOfQuestions, listOfAnswers,question_embeddings ,tf, embed ,graph, session
    modelInitialize = False
  #  print('Start the initialization ')
    df = getDF('%s' % filename)
    # Import the Universal Sentence Encoder's TF Hub module
    #embed = hub.Module(module_url)
    # Compute a representation for each message, showing various lengths supported.

    questionList = df['question'].astype(str).values.tolist()
    answerList = df['answer'].astype(str).values.tolist()

    listOfQuestions = questionList
    listOfAnswers = answerList
    tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.ERROR)

    graph = tf.Graph()
    global embed, question_embeddings
    embed, question_embeddings  = method_name(listOfQuestions, tf, graph)

    graph2 = tf.Graph()
    with tf.Session(graph=graph2) as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])

    init2()

def method_name(messages, tf, graph):
    global session
    with tf.Session(graph=graph) as session:
        embed = hub.Module("%s" % SENTENCE_ENCODER_LARGE_)
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])

        if path.exists(DATA_FILE):
            message_embeddings = np.load(DATA_FILE)
        else:
             message_embeddings = session.run(embed(messages))
             np.save('embedding.dat',message_embeddings)
    return embed,message_embeddings


# print("initialization is over")



# Reduce logging output.


def cosine_similarity(v1, v2):
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2[0])
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1, v2[0]) / (mag1 * mag2)

def init2():
    # Create graph and finalize (finalizing optional but recommended).
    global embedded_text,text_input,session2
    g = tf.Graph()
    with g.as_default():
        # We will be feeding 1D tensors of text into the graph.
        text_input = tf.placeholder(dtype=tf.string, shape=[None])
        embed = hub.Module(SENTENCE_ENCODER_LARGE_)
        embedded_text = embed(text_input)
        init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    g.finalize()

    # Create session and initialize.
    session2 = tf.Session(graph=g)
    session2.run(init_op)

def newReq(input):
    result = session2.run(embedded_text, feed_dict={text_input:input})
    return result
    #print(result)

def request2(query):
    query_embeddings = newReq([query])  # query_embedding([query],session)

    result = [cosine_similarity(x, query_embeddings) for x in question_embeddings]

    response = listOfAnswers[np.argmax(result)]

    response = response.split("||")

    replies = newReq(response)  # query_embedding(response,session)

    response_matching = [cosine_similarity(x, query_embeddings) for x in replies]

    argmax = np.argmax(response_matching)
    # print("selected index",argmax)
    final_response = response[argmax]
    return (final_response)

def getChatResponse(query):



        #print("--- %s initialization seconds ---" % (time.time() - start_time))
        with tf.Session(graph=graph) as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])


            query_embeddings =  query_embedding([query],session)


            result = [cosine_similarity(x, query_embeddings) for x in question_embeddings]


            response = listOfAnswers[np.argmax(result)]

            response = response.split("||")

            replies = query_embedding(response,session)


            response_matching = [cosine_similarity(x, query_embeddings) for x in replies]

            argmax = np.argmax(response_matching)
            #print("selected index",argmax)
            final_response = response[argmax]
        return (final_response)


def query_embedding(query,session):
        query_embeddings = session.run(embed(query))
        return query_embeddings


if __name__ == '__main__':
  init()
