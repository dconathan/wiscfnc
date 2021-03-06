"""
    Bag of Words object

    example:

        import load
        X_train, y_train, X_test, y_test = load(True, False, False, False)
        bow = BOW()
        bow.fit(X_train)
        X_bow = bow.transform(X_train)

    X_bow is a numpy array with shape = (len(X_train),len(bow.words)). 
    bow.words is accumulated by ./data/words-dict.pickle, which is generated anew in bow.fit(X_train) if it does not already exist

"""
import numpy as np
import pickle

class BOW:
    def __init__(self):
        pass

    def fit(self,X,y=None,new_pickle=False):
        # collect word dictionary (string keys with index values) from ./data/word-dict.pickle, or create it. If new_pickle is True, ./data/word-dict.pickle will be created or overwritten.
        try:
            if not new_pickle:
                self.words = pickle.load( open( "./data/word-dict.pickle", "rb" ))
        except:
            new_pickle = True

        if new_pickle:
            words = []
            for item in X:
                header,body = item[0],item[1]
                words += header + body
            words = list(set(words))
            words_dict = {}
            for i,w in enumerate(words):
                words_dict[w] = i
            pickle.dump(words_dict,open("./data/word-dict.pickle",'wb'))
            self.words = words_dict

        return self

    def transform(self,X,separate_vectors=False):
        '''
        Transform list of tuples X = (headline, article) into Bag of Words matrix

        inputs:
            - X = [(headline1,article1), (headline2,article2), ...]
            - separate_vectors (bool): if True, returns bowX = [headers_ndarray,articles_ndarray], else returns a single ndarray with combined header+article vectors per row

        outputs:
            - bowX = ndarray of shape (len(X),len(self.words)), each index of a row corresponds to the specific word in self.words and contains the number of instances of that word within the headline-article pair.

        '''
        headerX = np.zeros((len(X),len(self.words)))
        articleX = np.zeros_like(headerX)

        for i, x in enumerate(X):
            for word in x[0]:
                headerX[i,:] += self.bowVector(word)
            for word in x[1]:
                articleX[i,:] += self.bowVector(word)

        if separate_vectors:
            return [headerX,articleX]
        else:
            return headerX+articleX

    def fit_transform(self,X,y=None,new_pickle=False,separate_vectors=False):
        self.fit(X,y,new_pickle)
        output = self.transform(X,separate_vectors)
        return output


    def bowVector(self,word):
        # defines a vector of length len(self.words) that is zero-valued everywhere but where the input word string is found
        bow = np.zeros(len(self.words))
        try:
            bow[self.words[word]] = 1
        except:
            print('Word not found.')
        return bow


def test(n=10,use_fit_transform=True):
    '''
    Test BOW() object for n rows of the training dataset. 

    inputs:
        - n (int): number of rows of the training dataset to test BOW formulation on
        - use_fit_transform (bool): if True, test is done using the BOW.fit_transform() method, else use BOW.fit() then BOW.transform() separately
    '''

    import load

    X_train, y_train, X_test, y_test = load.load(True,False,False,False)
    bow = BOW()
    if not use_fit_transform:
        bow.fit(X_train,new_pickle=False)
        output = bow.transform(X_train[0:n])
        _using = 'fit() THEN tranform()'
    else:
        output = bow.fit_transform(X_train[0:n],new_pickle=False)
        _using = 'fit_transform()'
    print('Using {0}...\nWords found in each header/article\n'.format(_using),np.sum(output,axis=1))
    output = bow.fit_transform(X_train[0:n],new_pickle=False,separate_vectors=True)
    print('Words in each header, then words in each article\n{0}\n{1}'.format(np.sum(output[0],axis=1), np.sum(output[1], axis=1)))


if __name__=='__main__':
    n = 10
    use_fit_transform = True
    test(n,use_fit_transform)
