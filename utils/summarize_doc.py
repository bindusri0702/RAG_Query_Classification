# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# model_name = "t5-base"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# def summarize_doc(text):
#     summary = summarizer(text, max_length=500, min_length=50, do_sample=False)
#     return summary[0]['summary_text']



from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
LANGUAGE = "english"

def summarize_doc(text, SENTENCES_COUNT = 50):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary_string = " ".join([str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)])
    return summary_string