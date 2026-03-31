import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SPX Skew Mobile", layout="centered")
st.title("📊 SPX / ES Skew Sentiment")

# Pole do wklejenia danych (Input Area)
st.subheader("Wklej tabelę z Barchart:")
user_input = st.text_area("Czekam na dane (Strike, IV)...", height=250)

if user_input:
    try:
        # Parsowanie danych w locie
        df = pd.read_csv(io.StringIO(user_input), sep=None, engine='python')
        
        # Obliczenie Skew (pierwszy wiersz IV minus ostatni wiersz IV)
        skew_val = df['IV'].iloc[0] - df['IV'].iloc[-1]
        
        # Wybór sentymentu (Thresholds)
        if skew_val > 0.05:
            res, col = "SHORT", "#FF4B4B"
        elif skew_val < -0.02:
            res, col = "LONG", "#00CC96"
        else:
            res, col = "NEUTRAL", "#FFA15A"
            
        # Wyświetlanie wyniku na iPhone
        st.markdown(f"""
            <div style="background-color:{col}; padding:30px; border-radius:15px; text-align:center;">
                <h1 style="color:white; margin:0; font-size:45px;">{res}</h1>
                <p style="color:white; font-size:18px;">Skew Delta: {skew_val:.4f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.line_chart(df.set_index('Strike')['IV'])
        
    except Exception as e:
        st.error("Błąd: Upewnij się, że tabela ma nagłówki 'Strike' i 'IV'.")
