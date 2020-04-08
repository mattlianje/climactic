import pickle
import numpy as np


# input: array of strings containing mfcc data
# ouput: np array of predicted excitement
def predictExcitement(mfccVals):
  mfccArr = [mfccStrToArr(mfccStr) for mfccStr in mfccVals]
  modelFilePath = "datastore/models/excitement-models/svm_poly_1.sav"
  model = pickle.load(open(modelFilePath, 'rb'))
  y = model.predict(mfccArr)
  return np.array(y)


def mfccStrToArr(mfccStr):
    cleanedStr = mfccStr.replace('[', '').replace(']', '')
    str_arr = cleanedStr.split()
    result = list(map(lambda x: float(x), str_arr))
    return result
