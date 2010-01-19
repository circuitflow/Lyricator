""" unigram-level reference implementation for
   textual affect sensing using omcs """

import cPickle,os

class emotuslite:

    __author__ = "hugo@media.mit.edu"	
    __license__ = "http://creativecommons.org/licenses/by-nc-sa/2.5/"

    def __init__(self):

        # variables
        self.lookup_anew = {} 
        self.omcs_affective_words = {} 
        self.stopwords = {}

        # build emotuslite db only once
        if not os.path.exists('emotuslite.pickle'):
            self.load_anew_file()
            self.load_stopwords()
            self.load_omcs_affective_words()
            stuff = [self.lookup_anew,self.omcs_affective_words,self.stopwords]
            cPickle.dump(stuff,open('emotuslite.pickle','w'))
        else:
            stuff = cPickle.load(open('emotuslite.pickle'))
            self.lookup_anew,self.omcs_affective_words,self.stopwords = stuff
        return
    
    def appraise_document(self,text):
        """ 1) tokenizes document
         2) filters out stopwords
         3) spots anew and omcs-affective words
         4) calcs overall valence-arousal-dominance
         """
        # omitted to prevent errors -OM
        # text = text.encode('ascii','ignore') # handle latin1 letters 
        text = text.lower()
        text = text.replace('.',' . ').replace(',',' , ').replace('!',' ! ').replace('?',' ? ') # tokenization for dummies
        toks = text.split()
        toks = filter(lambda tok: not self.stopwords.has_key(tok), toks)
        cumulative_vad_scores = []
        for word in toks:
            # recognize anew words
            if self.lookup_anew.has_key(word):
                cumulative_vad_scores.append(self.lookup_anew[word])
                continue
            # recognize omcs words
            elif self.omcs_affective_words.has_key(word):
                cumulative_vad_scores.append(self.omcs_affective_words[word])
        # avg all the cumulative vads for
        # document-level affect
        document_vad = self._avg_triples(cumulative_vad_scores)
        return document_vad

            
    def load_omcs_affective_words(self):

        """Tokenizes the OMCS sentences into words.
        builds the following affective words db:
          key: word_in_omcs
          value: avg valence-arousal-dominance

        The purpose is to use OMCS words to expand
        the recognition vocabulary for affect.

        If an anew word is found in the sentence,
        every non-stopworded word in that sentence
        is given the affect of the anew word times
        a discount (e.g. 25%)
        """

        filename = 'omcsraw.txt'
        sentences = open(filename).read().split('\n\n')
        for i in range(len(sentences)):
            if i%10000==0: print "loading %s omcs sentences"%i
            
            sentence = sentences[i]
            sentence = sentence.lower()
            sentence = sentence.replace('.',' . ').replace(',',' , ').replace('!',' ! ').replace('?',' ? ') # tokenization for dummies
            words = filter(lambda word: not self.stopwords.has_key(word),
                           sentence.split())
            # what is the avg. affect value of sentence?
            anew_words_in_sentence = filter(lambda word: self.lookup_anew.has_key(word),
                   words)
            if not anew_words_in_sentence:
                continue
            values = map(lambda anew_word: self.lookup_anew[anew_word],
                anew_words_in_sentence)
            sentence_value = self._avg_triples(values)
            discount = 0.25
            discounted_sentence_value = map(lambda x:discount*x,
                                            sentence_value)

            # propagate affect to words in sentence
            for word in words:
                if not self.omcs_affective_words.has_key(word):
                    self.omcs_affective_words[word] = []
                self.omcs_affective_words[word].append(discounted_sentence_value)
        # now produce a single avg'ed vad for each word
        for word in self.omcs_affective_words.keys():
            self.omcs_affective_words[word] = self._avg_triples(self.omcs_affective_words[word])
        
        return
    
    def load_stopwords(self):
        """reads in the 500 common stopwords file"""

        filename = 'stopwords.txt'
        stopwords = open(filename).read().split('\n')
        # read stopwords into dict for efficency
        self.stopwords = dict(zip(stopwords,[None]*len(stopwords)))
        return
        
    def load_anew_file(self):
        """Loads the ANEW affective norms database into
        a dictionary whose keys are words and values
        are a triple: (valence,arousal,dominance)"""
        
        filename = 'anew-androgynous.txt'
        lines = open(filename).read().split('\n')
        for line in lines:
            word,no,v,v_std,a,a_dev,d,d_dev,freq=line.split()
            # need to normalize v,a,d
            # remap ranges (0,10) ==> (-1,1)
            vad = map(lambda x: (x-5)/5.0, (float(v),float(a),float(d)))
            self.lookup_anew[word]=vad
        return

    def _avg_triples(self,triples):
        """utility function to calc the arithmetic
        mean of a list of triples"""
        return map(lambda x:sum(x)*1.0/len(x),zip(*triples))

############################### 
# Modified by Owen Meyers for use with lyricator.sh
###############################
if __name__ == '__main__':
	
    import sys
    e = emotuslite()
    if '.py' not in sys.argv[-2].lower():
        doc = open(sys.argv[-2],'r').read()
        score = e.appraise_document(doc)
        
        # Threshold values (pleasure = 0.0843..., arousal = 0.0125...) come from analyzing
        # the PAD scores of several thousand songs and finding the midpoint of these values

        if (score[0] > 0.0843264048824253) and (score[1] > 0.0125793907208737):
            emotionality="engaging"
        elif (score[0] > 0.0843264048824253) and (score[1] < 0.0125793907208737):
            emotionality="soothing"
        elif (score[0] < 0.0843264048824253) and (score[1] < 0.0125793907208737):
            emotionality="boring"
        elif (score[0] < 0.0843264048824253) and (score[1] > 0.0125793907208737):
            emotionality="angry"
        else:
            emotionality="unknown"
        
        print "Here are the results for (" + str(sys.argv[-2]) + "):"
        print "<pleasure> %s"%score[0]
        print "<arousal> %s"%score[1]
        print "<dominance> %s"%score[2]
        print ""
        print "These lyrics are %s"%emotionality
        
        # By default, lyric scores are written to 'scores.txt'

        if sys.argv[-1]:
	   # write results to file 
               f1=open(sys.argv[-1], 'a')      
               f1.write(str(sys.argv[-2]) + "\t" + str(emotionality) + "\t" + str(score) + '\n')
               f1.close()

    else:
        print '<interactive mode on>'
        print '<enter a sentence and press enter>'
        while 1:
            sentence = raw_input('> ')
            score = e.appraise_document(sentence)
            score = map(lambda x:round(x,4),score)
            print "[pleasure: %s], [arousal: %s], [dominance: %s]"%(score[0],score[1],score[2])
