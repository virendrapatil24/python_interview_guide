# Deep Dive: SpaCy

Industrial-strength Natural Language Processing (NLP). Unlike NLTK (academic/teaching), SpaCy is built for production speed and ease of use.

---

## 1. The Processing Pipeline

When you call `nlp("text")`, it runs a pipeline:
**Tokenizer** -> **Tagger** -> **Parser** -> **NER** -> ...

```python
import spacy

# Load English model (optimized binary)
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
```

---

## 2. Token Attributes

Tokens are not just strings. They contain linguistic features.
*   `.lemma_`: Base form (doing -> do).
*   `.pos_`: Part of speech (VERB, NOUN).
*   `.is_stop`: Is it a stop word (the, is, at)?

---

## 3. Named Entity Recognition (NER)

SpaCy excels at extracting real-world objects.

```python
for ent in doc.ents:
    print(ent.text, ent.label_)
# Apple ORG
# U.K. GPE
# $1 billion MONEY
```

---

## 4. Word Vectors

SpaCy (medium/large models) allows similarity comparison using GloVe/Word2Vec.
`token1.similarity(token2)`
