import re
from collections import Counter

STOPWORDS = set("""
a an the and or but if while is are was were be been being to of in on
for with as by at from this that these those it its he she they them his
her their i you we me my your our not no can will would should could
do does did so than then there here what which who whom about into
over under again further out up down off above below between
""".split())


def generate_summary(text, num_sentences=3):
    """
    Simple extractive summarizer.
    Splits text into sentences, scores each sentence based on the
    frequency of important (non-stopword) words it contains, and
    returns the top-scoring sentences in their original order.
    """

    text = text.strip()

    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= num_sentences:
        return text

    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(w for w in words if w not in STOPWORDS)

    if not word_freq:
        return " ".join(sentences[:num_sentences])

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    sentence_scores = {}
    for sentence in sentences:
        score = 0
        sentence_words = re.findall(r'\w+', sentence.lower())
        for word in sentence_words:
            if word in word_freq:
                score += word_freq[word]
        # Normalize by sentence length to avoid bias toward long sentences
        sentence_scores[sentence] = score / (len(sentence_words) + 1)

    ranked_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )

    top_sentences = set(ranked_sentences[:num_sentences])

    # Preserve original order
    summary = " ".join(s for s in sentences if s in top_sentences)

    return summary