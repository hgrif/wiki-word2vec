# Wiki Word2vec


Train a [gensim](https://radimrehurek.com/gensim/) word2vec model on Wikipedia.

Most of it is taken from [this blogpost](http://textminingonline.com/training-word2vec-model-on-english-wikipedia-by-gensim) and [this discussion](https://groups.google.com/forum/#!topic/gensim/MJWrDw_IvXw).
This repository was created mostly for trying out `make`, see __The gist__ for the important stuff.
Note that performance depends heavily on corpus size and chosen parameters (especially for smaller corpora).
Examples and parameters below are cherry-picked.


## Usage

Get the code for a language (see [here](https://meta.wikimedia.org/wiki/List_of_Wikipedias)).

Run `make` with the code as the value for `LANGUAGE` (or change the Makefile). 
For instance, try Swahili (sw):

```sh
make LANGUAGE=sw
```

### The gist

Ignore `make` and execute the following bash commands for Swahili:

```sh
mkdir -p data/sw/
wget -P data/sw/ https://dumps.wikimedia.org/swwiki/latest/swwiki-latest-pages-articles.xml.bz2
```

Train a model in Python:

```python
import multiprocessing
from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.word2vec import Word2Vec

wiki = WikiCorpus('data/sw/swwiki-latest-pages-articles.xml.bz2', 
                  lemmatize=False, dictionary={})
sentences = list(wiki.get_texts())
params = {'size': 200, 'window': 10, 'min_count': 10, 
          'workers': max(1, multiprocessing.cpu_count() - 1), 'sample': 1E-3,}
word2vec = Word2Vec(sentences, **params)
```

#### Example 1

Try the old man:king woman:? problem:

```python
female_king = word2vec.most_similar_cosmul(positive='mfalme mwanamke'.split(), 
                                           negative='mtu'.split(), topn=5,)
for ii, (word, score) in enumerate(female_king):
    print("{}. {} ({:1.2f})".format(ii+1, word, score))

1. malkia (0.97)
2. kambisi (0.93)
3. suleimani (0.93)
4. karolo (0.92)
5. koreshi (0.92)
```

Returning respectively queen (jackpot!), [Cambyses II](https://en.wikipedia.org/wiki/Cambyses_II) (a Persian king), [Solomon](https://en.wikipedia.org/wiki/Solomon) (king of Israel), [Karolo Mkuu?](https://sw.wikipedia.org/wiki/Karolo_Mkuu) (Charlemagne?) and [Cyrus](https://en.wikipedia.org/wiki/Cyrus_(name)) (a Persian King),


#### Example 2

What doesn't match: car, train or breakfast?

```python
print(word2vec.doesnt_match('gari treni mlo'.split()))

mlo
```


## Dependencies

* Python 3
* `pip install gensim`
