import streamlit as st
import psycopg2
import pandas as pd
import plotly.graph_objects as go
from config import DATABASE_CONFIG
import time

st.set_page_config(page_title="AeroStream Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- STYLE ---
st.markdown("""
<style>
    body {background-color: #f0f2f6;}
    h1 {color: #1f77b4; text-align: center; margin-bottom: 30px;}
    .metric-container {
        background: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 15px;
    }
    .chart-container {
        background: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

placeholder = st.empty()

# --- LOOP ---
while True:
    try:
        # Connexion DB
        conn = psycopg2.connect(**DATABASE_CONFIG)
        df = pd.read_sql("SELECT * FROM predictions ORDER BY timestamp DESC", conn)
        conn.close()

        with placeholder.container():
            st.markdown("<h1>📊 TWITTER US AIRLINE SENTIMENT DATASET</h1>", unsafe_allow_html=True)

            # --- METRICS ---
            col1, col2, col3 = st.columns(3)
            total_tweets = len(df)
            total_airlines = df['airline'].nunique()
            neg_count = (df['airline_sentiment'] == 'negative').sum()
            neg_pct = (neg_count / total_tweets * 100) if total_tweets > 0 else 0

            for col, title, value in zip([col1, col2, col3],
                                         ["COUNT OF TWEETS", "COUNT OF AIRLINES", "% NEGATIVE"],
                                         [total_tweets, total_airlines, f"{neg_pct:.1f}%"]):
                col.markdown(f'<div class="metric-container"><h3>{title}</h3><h1>{value}</h1></div>', unsafe_allow_html=True)

            # --- CHARTS ---
            col_left, col_right = st.columns(2)

            # Left charts
            with col_left:
                # Negative Reason
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown("<h3>NEGATIVE REASON COUNT</h3>", unsafe_allow_html=True)
                if 'negativereason' in df.columns:
                    negative_df = df[df['airline_sentiment'] == 'negative']
                    reason_counts = negative_df['negativereason'].value_counts().head(10)
                    fig_reasons = go.Figure(go.Bar(
                        x=reason_counts.values,
                        y=reason_counts.index,
                        orientation='h',
                        marker=dict(color='#1f77b4')
                    ))
                    fig_reasons.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig_reasons, use_container_width=True)
                else:
                    st.info("Aucune raison négative disponible")
                st.markdown('</div>', unsafe_allow_html=True)

                # Sentiment Pie
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown("<h3>COUNT OF SENTIMENT</h3>", unsafe_allow_html=True)
                sentiment_counts = df['airline_sentiment'].value_counts()
                colors = {'negative': '#ff6b6b', 'neutral': '#a8dadc', 'positive': '#4ecdc4'}
                fig_sentiment = go.Figure(go.Pie(
                    labels=sentiment_counts.index,
                    values=sentiment_counts.values,
                    hole=0.5,
                    marker=dict(colors=[colors.get(s, '#1f77b4') for s in sentiment_counts.index])
                ))
                fig_sentiment.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_sentiment, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Right charts
            with col_right:
                # Airline vs Sentiment
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown("<h3>AIRLINE VS SENTIMENT</h3>", unsafe_allow_html=True)
                airline_sentiment = pd.crosstab(df['airline'], df['airline_sentiment'])
                fig_airline = go.Figure()
                for sentiment in ['negative', 'neutral', 'positive']:
                    if sentiment in airline_sentiment.columns:
                        fig_airline.add_trace(go.Bar(
                            name=sentiment.capitalize(),
                            x=airline_sentiment.index,
                            y=airline_sentiment[sentiment],
                            marker_color=colors[sentiment]
                        ))
                fig_airline.update_layout(barmode='stack', height=300, margin=dict(l=20,r=20,t=20,b=20))
                st.plotly_chart(fig_airline, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Date vs Negative Sentiment
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown("<h3>DATE VS SENTIMENT</h3>", unsafe_allow_html=True)
                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                daily_sentiment = df[df['airline_sentiment']=='negative'].groupby('date').size().reset_index(name='count')
                fig_timeline = go.Figure(go.Scatter(
                    x=daily_sentiment['date'],
                    y=daily_sentiment['count'],
                    mode='lines+markers',
                    line=dict(color='#1f77b4', width=2)
                ))
                fig_timeline.update_layout(height=350, margin=dict(l=20,r=20,t=20,b=20))
                st.plotly_chart(fig_timeline, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur de connexion: {e}")

    time.sleep(5)
