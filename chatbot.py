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
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

filename = 'opiates_0.txt'

SENTENCE_ENCODER_LARGE_ = "model/3"
SENTENCE_ENCODER_MEDIUM = "model/2"
module_url = SENTENCE_ENCODER_MEDIUM

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):

  path ="data\\"  # use your path
  all_files = glob.glob(path + "/opiates*.txt")

  li = []

  for filename in all_files:
      df2 = pd.read_csv(filename, index_col=None, header=0)
      li.append(df2)

  df = pd.concat(li, axis=0, ignore_index=True)


  # directory = os.fsencode("C:\\Users\\mahdi\\PycharmProjects\\chatbot")
  # collection = []
  # for file in os.listdir(directory):
  #     filename = os.fsdecode(file)
  #     if filename.endswith("0.txt"):
  #         #print(filename)
  #         with open(filename) as json_file:
  #           data = json.load(json_file)
  #
  #         for d in data['opiates']:
  #             for item in d:
  #                 value = d.get(item)[0]
  #                 question = value.get('0_title')
  #                 comments = value['comments'][0]
  #                 answerlist=[]
  #                 for comment in comments:
  #                   answer = comments.get(comment)
  #                   answerlist.append(answer)
  #                 collection.append([question,answerlist])
  #
  #
  # # Create the pandas DataFrame
  # df = pd.DataFrame(collection, columns=['question', 'answer'])

  df = df.groupby(['question'])['answer'].apply(lambda x: '||'.join(x)).reset_index()

  return df


def init():
    global query, listOfQuestions, listOfAnswers,question_embeddings ,tf, embed ,graph
  #  print('Start the initialization ')
    df = getDF('%s' % filename)
    # Import the Universal Sentence Encoder's TF Hub module
    #embed = hub.Module(module_url)
    # Compute a representation for each message, showing various lengths supported.

    questionList = df['question'].astype(str).values.tolist()
    answerList = df['answer'].astype(str).values.tolist()

   # print('total questions',len(questionList),' total answers',len(answerList))

    listOfQuestions = questionList
    listOfAnswers = answerList
    tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.ERROR)



  #  print("start to load the model")
    graph = tf.Graph()
    global embed, question_embeddings
    embed, question_embeddings  = method_name(listOfQuestions, tf, graph)


def method_name(messages, tf, graph):
    with tf.Session(graph=graph) as session:
        embed = hub.Module("%s" % SENTENCE_ENCODER_LARGE_)
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        #message_embeddings = session.run(embed(messages))
        message_embeddings = np.load('embedding.dat.npy')
        #np.save('embedding.dat',message_embeddings)
    return embed,message_embeddings


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

    query_embeddings = query_embedding([query])
    result = [cosine_similarity(x, query_embeddings) for x in question_embeddings]
    response = listOfAnswers[np.argmax(result)]
    question = listOfQuestions[np.argmax(result)]

    print("question ",question)

    # get the most approporate response
    #print("before",response)
    response= response.replace("[",'')
    response = response.replace("]",'')
    response = response.replace("\"", '\'')
    #response = response.split(", '")
    #print("after", response)


    response = response.split("||")

    print('length of responses',len(response))

    replies = query_embedding(response)
    response_matching = [cosine_similarity(x, query_embeddings) for x in replies]

    argmax = np.argmax(response_matching)
    print("selected index",argmax)
    final_response = response[argmax]
    return (final_response)


def query_embedding(query):
    with tf.Session(graph=graph) as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        query_embeddings = session.run(embed(query))
    return query_embeddings


if __name__ == '__main__':
  init()