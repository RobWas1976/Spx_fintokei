import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SPX Sentiment Tool", layout="wide")
st.title("📊 SPX / ES Sentiment & Skew")

data = st.text_area("Wklej dane z Barchart tutaj:", height=200)

if data:
    try:
        clean_data = data.replace('“', '"').replace('”', '"')
        df = pd.read_csv(io.StringIO(clean_data), on_bad_lines='skip')
        df.columns = [c.replace('"', '').strip() for c in df.columns]
        
        for col in ['Strike', 'IV']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(r'[%,"]', '', regex=True).astype(float)
        
        if 'Type' in df.columns:
            # Obliczanie sentymentu
            avg_put_iv = df[df['Type'].str.contains('Put', case=False, na=False)]['IV'].mean()
            avg_call_iv = df[df['Type'].str.contains('Call', case=False, na=False)]['IV'].mean()
            
            st.divider()
            
            # Wskaźnik wizualny
            if avg_put_iv > avg_call_iv:
                st.error(f"📉 SENTYMENT: SPADKOWY (Risk-Off)")
                st.write(f"Rynek wycenia większy strach (Puty IV: {avg_put_iv:.2f}%) niż chciwość (Call IV: {avg_call_iv:.2f}%)")
            else:
                st.success(f"📈 SENTYMENT: WZROSTOWY (Risk-On)")
                st.write(f"Rynek obstawia wzrosty (Call IV: {avg_call_iv:.2f}%) bardziej niż spadki (Put IV: {avg_put_iv:.2f}%)")
            
            st.divider()
            
            # Wykres dla Putów (klasyczny Skew)
            df_puts = df[df['Type'].str.contains('Put', case=False, na=False)].sort_values('Strike')
            if not df_puts.empty:
                st.subheader("Wykres Skew (Put IV)")
                st.line_chart(df_puts.set_index('Strike')['IV'])
                
    except Exception as e:
        st.error(f"Błąd: {e}")
