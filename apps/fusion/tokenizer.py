from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
#from nltk.collocations import BigramCollocationFinder
#from nltk.metrics import BigramAssocMeasures

mystopwords = []
mystopwords += stopwords.words('english')
mystopwords += ['the', 'and', 'of', 'ca', 'pre', 'st', 'rd', 'a', 'the'] 
def extract_words(mytext):
    '''Extract features to use in our tags. We want to pull all the words in our input
    and grab the most significant bigrams to add to the mix as well.
    '''

    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(str(mytext).lower().translate(None, '[].&-()!@#$%^&*{};":,<>/?'))
    tokens = [x for x in tokens if x not in mystopwords and len(x) > 2]
    
#    bigram_finder = BigramCollocationFinder.from_words(tokens)
#    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
#
#    for bigram_tuple in bigrams:
#        x = "%s %s" % bigram_tuple
#        tokens.append(x)

    result =  tokens
    return result