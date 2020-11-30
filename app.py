import joblib
import streamlit as st
from PIL import Image
import joblib

import nltk
nltk.download('punkt')
import spacy
from textblob import TextBlob
# gensim pkg
from gensim.summarization import summarize
# sumy pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def text_analyzer(my_text):
    # nlp = spacy.load('en_core_web_sm')
    nlp = joblib.load('asset/en_core_web_sm')
    docx = nlp(my_text)
    all_data = [ f"Tokens: {token.text}, \n Lemma: {token.lemma_}" for token in docx]
    return all_data

def entity_analyzer(my_text):
    # nlp = spacy.load('en_core_web_sm')
    nlp = joblib.load('asset/en_core_web_sm')
    docx = nlp(my_text)
    entities = [f"{entity.text}: {entity.label_}" for entity in docx.ents]
    return entities


def sumy_sumarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer('english'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = " ".join(summary_list)
    return result

def main():

    st.title("NLP-ify with streamlit")
    st.subheader("Natural Language Processing on a go")

    # Tokenization
    if st.checkbox("Show Tokens and Lemmatization"):
        st.subheader("Tokenize your text")
        message = st.text_area("Enter Your Text", "Type Here")
        if st.button("Analyze"):
            nlp_result = text_analyzer(message)
            st.json(nlp_result)

    # Name Entity
    if st.checkbox("Show Named Entities"):
        st.subheader("Extract Entities From Your Text")
        message = st.text_area("Enter Your Text", "Type Here")
        if st.button("Extract"):
            nlp_result = entity_analyzer(message)
            st.json(nlp_result)

    # Sentiment Analysis
    if st.checkbox("Show Sentiment Analysis"):
        st.subheader("Sentiment of Your Text")
        message = st.text_area("Enter Your Text", "Type Here")
        if st.button("Analyze"):
            blob = TextBlob(message)
            result_sentiment = blob.sentiment
            st.success(result_sentiment)

    # Text Summarization

    if st.checkbox("Show Text Summarization"):
        st.subheader("Summarize Your Text")
        message = st.text_area("Enter Your Text", "Type Here")
        summary = st.selectbox("Choose your summarizer", ('gensim', 'sumy'))
        if st.button("Summarize"):
            if summary == 'gensim':
                try:
                    st.text("Using Gensim...")
                    summary_result = summarize(message)
                    st.success(summary_result)
                except:
                    st.exception("Input must have more than one sentence.")
            elif summary == 'sumy':
                try:
                    st.text("Using Sumy...")
                    summary_result = sumy_sumarizer(message)
                    st.success(summary_result)
                except:
                    st.exception("Input correct things.")

    st.sidebar.subheader('About the App')
    st.sidebar.markdown('## NLP-ify App with Streamlit')
    st.sidebar.info("#### Get the Tokens of your words")
    st.sidebar.info("#### Get the Named-Entities of your words")
    st.sidebar.info("#### Get the Sentiment Analysis of your words")
    st.sidebar.info("#### Get the Summary of your words")
    
if __name__ == '__main__':
    main()