import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# OpenAI API Key
openai.api_key = "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"


def analyze_sentiment(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant. Classify the sentiment as Positive, Negative, or Neutral along with a confidence score and detected emotions as well as show what this sentiment means and also give detailed information on the user behavious"},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]

def lead_scoring(name, email, company, engagement_level, purchase_intent):
    prompt = f"""
    Given the following lead details:
    - Name: {name}
    - Email: {email}
    - Company: {company}
    - Engagement Level: {engagement_level} (Low, Medium, High)
    - Purchase Intent: {purchase_intent} (Low, Medium, High)
    
    Provide a lead score from 0 to 100 along with reasoning.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a lead scoring assistant. Score the lead based on engagement and purchase intent, providing reasoning."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit App
st.title("AI-Driven Sentiment & Lead Scoring App")

# Sentiment Analysis Section
st.header("Sentiment Analysis")
st.write("Enter a sentence below to analyze its sentiment:")
text_input = st.text_area("Input Text")

if st.button("Analyze Sentiment"):
    if text_input.strip():
        with st.spinner("Analyzing..."):
            sentiment_result = analyze_sentiment(text_input)
        st.success("Analysis Complete!")
        st.write("### Sentiment Analysis Result:")
        st.write(sentiment_result)
    else:
        st.warning("Please enter some text before analyzing.")

# CSV Upload for Bulk Sentiment Analysis
st.header("Bulk Sentiment Analysis from CSV")
file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    # Automatically detect the text column
    text_column = None
    for col in df.columns:
        if "text" in col.lower():
            text_column = col
            break
    
    if text_column:
        st.write("### Preview of Uploaded Data:")
        st.write(df.head())

        if st.button("Analyze Sentiments in CSV"):
            with st.spinner("Analyzing sentiments..."):
                df_subset = df.head(5)  # Take only the first 10 rows
                df_subset["Sentiment Analysis"] = df_subset[text_column].apply(analyze_sentiment)
            
            st.success("Sentiment Analysis Complete!")
            st.write(df_subset)
            
            # Sentiment Count Plot
           
    else:
        st.error("CSV must contain a column related to text!")


# Lead Scoring Section
st.header("AI-Driven Lead Scoring")
st.write("Enter lead details to get a score:")

name = st.text_input("Name")
email = st.text_input("Email")
company = st.text_input("Company")
engagement_level = st.selectbox("Engagement Level", ["Low", "Medium", "High"])
purchase_intent = st.selectbox("Purchase Intent", ["Low", "Medium", "High"])

if st.button("Get Lead Score"):
    if name and email and company:
        with st.spinner("Scoring lead..."):
            lead_score = lead_scoring(name, email, company, engagement_level, purchase_intent)
        st.success("Lead Scoring Complete!")
        st.write("### Lead Score & Insights:")
        st.write(lead_score)
    else:
        st.warning("Please fill all fields before scoring.")
