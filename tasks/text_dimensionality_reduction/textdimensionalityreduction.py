import csv
import string
from gensim.models import Doc2Vec
from gensim.models.deprecated.doc2vec import LabeledSentence
import pandas as pd
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import numpy as np

from ..models import Task


class LabeledLineSentence(object):
    def __init__(self, sentences):
        self.sentences = sentences
    def __iter__(self):
        for i in range(len(self.sentences)):
            yield LabeledSentence(words=self.sentences[i], tags=['SENT_%s' % i])

#getting rid of the string punctuation
#https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
def cleanseWords(separatedWords):
    for i, word in enumerate(separatedWords):
        word = word.lower()
        word = word.translate(str.maketrans('', '', string.punctuation))
        separatedWords[i] = word
    #return separatedWords

def gatherSentences(gatheredWords):
        tasksList = Task.objects.values_list("task_name")
        rowNumber = 0
        for row in tasksList:
            #check if row isnt empty
            if len(row) != 0:
                currentSentence = row[0]#access the tuple content(task_name)
                separatedWords = currentSentence.split(" ")
                #get rid of interpunction to lower letters
                cleanseWords(separatedWords)
                gatheredWords.append(LabeledSentence(words = separatedWords, tags=["SENT_"+str(rowNumber)]))
                rowNumber += 1

def createSentenceVectors(gatheredWords, model):
    sentenceVectors = []
    vocab = list(model.wv.vocab)
    #count average of word vectors to create a sentence vector
    for sentence in gatheredWords:
        sentenceVector = np.zeros((100, ), dtype='float32')
        countWords = 0
        for word in sentence[0]:
            if word in vocab:
                sentenceVector = np.add(sentenceVector, model[word])
        if countWords != 0:
            sentenceVector = np.divide(sentenceVector, countWords)
        sentenceVectors.append(sentenceVector)
    return sentenceVectors

def sentencesTo2D():
    wordsListInSentence = []

    #for testing purposes(it is used to load only few first row data)

    gatheredWords = []
    gatherSentences(gatheredWords)


    #load Doc2Vec model
    model = Doc2Vec.load("tasks/text_dimensionality_reduction/doc2vecmodel")

#https://stackoverflow.com/questions/43776572/visualise-word2vec-generated-from-gensim
    #vocab = list(model.wv.vocab)
    #X = model[vocab]#it may be used if want to visualise word vectors not sentences

    sentenceVectors = createSentenceVectors(gatheredWords, model)

    print("end of counting vectors")

    #prepare TSNE
    tsne = TSNE(n_components=2)
    #X_tsne = tsne.fit_transform(X)
    X_tsne = tsne.fit_transform(sentenceVectors)

    #join sentences so they will be as label for points
    sentencesAdHoc = []
    for sentence in gatheredWords:
        sentencesAdHoc.append(" ".join(sentence[0]))


    df = pd.DataFrame(X_tsne, index=sentencesAdHoc, columns=['x', 'y'])
    #print(df)
    chartValuesDictionary = {
        "x": df['x'].tolist(),
        "y": df['y'].tolist(),
        "labels": sentencesAdHoc,
    }

    return chartValuesDictionary

if __name__ == "__main__":
    sentencesTo2D()
