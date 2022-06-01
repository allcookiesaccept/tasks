from unidecode import unidecode
import pandas as pd
from sklearn.cluster import KMeans
from nltk.corpus import stopwords




"""## Tokenization

We now tokenize each of our keywords.  
To do so, we'll transform our queries into bags of words, by simply splitting the strings.  

Let's define a function that transforms a string to a bag of words, with a few extras:  
- we'll use `unidecode` to encode our strings to ASCII, thus removing special characters and accents,  
- we'll convert all characters to lowercase,  
- we'll add an option to filter out a list of stopwords,  
- we'll add an other option to filter out shorter words (single characters for example).  """

def do_tokens(key: str, stopwords=None, char_limit=1):
    """
    Transforms sentence to list of tokens.
    Basic: transform special characters to ascii + lowercase.
    Options:
    - remove stopwords (provide list of stopwords)
    - set minimum length for tokens: will remove any shorter token.
    Returns sorted tokens
    """

    # key = unidecode(str(key)).lower()
    key = str(key).lower()
    tokens = key.split(' ')

    if char_limit > 1:
        tokens = [str(word) for word in tokens if len(word) >= char_limit]

    if stopwords is not None:
        tokens = [word for word in tokens if word not in stopwords]

    tokens = set(tokens)
    tokens = sorted(tokens)

    return tokens


def do_vector(keyword, vocabulary):
    """
    Calculates vector of keyword on given vocabulary.

    Returns vector as a list of values.
    """
    vector = []

    for word in vocabulary:
        if word in keyword:
            vector.append(1)
        else:
            vector.append(0)

    return vector


if __name__ == '__main__':

    # russian_stopwords = stopwords.words("russian")

    keywords = pd.read_csv('datasets/k-mean_clusterization_dataset.csv', delimiter=';', header=1)

    keywords['Токены'] = keywords['Запросы'].apply(lambda x: do_tokens(x, stopwords=None, char_limit=3)).astype(str)

    vocab = sorted(set(keywords["Токены"].explode()))

    keywords["Вектор"] = keywords["Токены"].apply(lambda x: do_vector(x, vocab))
    # print(keywords.head())

    kmeans = KMeans(n_clusters=100, random_state=0).fit(keywords['Вектор'].to_list())
    keywords['kmeans'] = list(kmeans.labels_)
    print(keywords.head(10))

    print(keywords.groupby("kmeans")["Запросы"].count())