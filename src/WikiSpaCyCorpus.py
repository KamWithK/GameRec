#!/usr/bin/env python
# coding: utf-8

import spacy, bz2

from gensim.corpora import WikiCorpus
from gensim.corpora.wikicorpus import filter_wiki, extract_pages
from gensim.corpora.wikicorpus import IGNORED_NAMESPACES

class WikiSpacyCorpus(WikiCorpus):
    def lemmatize_and_tokenize(self, content):
        nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

        # Note that only accepting verbs and nouns effectively removes all miscellaneous characters
        # Without this more conditions need to be added
        token_is_valid = lambda token: not token.is_stop and token.prefix_ != "_" and 2 <= len(token.lemma_) <= 15 and token.pos_ is ("VERB" or "NOUN")

        for game in content:
            doc = nlp(game)

            if len(doc) >= self.article_min_tokens:
                yield [token.lemma_ for token in doc if token_is_valid(token)]

    def get_texts(self):
        is_ignored = lambda title: any(title.startswith(ignore + ':') for ignore in IGNORED_NAMESPACES)
        pages = [filter_wiki(page[1]) for page in extract_pages(open(self.fname)) if not is_ignored(page[0])]
        return self.lemmatize_and_tokenize(pages)
