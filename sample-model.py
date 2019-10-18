import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re


module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
embed = hub.Module(module_url)
word = "Elephant"
sentence = "I am a sentence for which I would like to get its embedding."
paragraph = (
    "Universal Sentence Encoder embeddings also support short paragraphs. "
    "There is no hard limit on how long the paragraph is. Roughly, the longer "
    "the more 'diluted' the embedding will be.")
listOfQuestions = [word, sentence, paragraph]

with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    question_embeddings = session.run(embed(listOfQuestions))

    for i, message_embedding in enumerate(np.array(question_embeddings).tolist()):
        print("Message: {}".format(listOfQuestions[i]))
        print("Embedding size: {}".format(len(message_embedding)))
        message_embedding_snippet = ", ".join(
            (str(x) for x in message_embedding[:3]))
        print("Embedding: [{}, ...]\n".format(message_embedding_snippet))



