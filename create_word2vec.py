#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
USAGE: %(program)s TEXT_INPUT WORD2VEC_OUTPUT TEXT_OUTPUT

Example script for training a word2vec model. Parameters for word2vec should be
optimized per language. TEXT_OUTPUT, true of false, if vectors should be outputted to a text file.
"""

import logging
import multiprocessing
import os
import sys
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("Running %s" % ' '.join(sys.argv))

    # Check and process input arguments.
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    inp, outp, veco = sys.argv[1:4]

    max_length = 0
    with open(inp, 'r') as f:
        for line in f.readlines():
            max_length = max(max_length, len(line))
    logger.info("Max article length: {} words.".format(max_length))

    params = {
        'size': 400,
        'window': 10,
        'min_count': 10,
        'workers': max(1, multiprocessing.cpu_count() - 1),
        'sample': 1E-5,
        }

    word2vec = Word2Vec(LineSentence(inp, max_sentence_length=max_length),
                        **params)
    word2vec.save(outp)

    if veco:
        word2vec.save_word2vec_format(outp + '.model.txt', binary=False)
