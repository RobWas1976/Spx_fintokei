import streamlit as st
import pandas as pd
import io

st.title("📊 SPX / ES Option Skew")

data = st.text_area("Wklej dane z Barchart tutaj:", height=300)

if data:
    try:
        # Naprawa cudzysłowów iPhone'a i wczytanie danych
        clean_data = data.replace('“', '"').replace('”', '"')
        df = pd.read_csv(io.StringIO(clean_data), on_bad_lines='skip')
        
        # Czyszczenie nagłówków
        df.columns = [c.replace('"', '').strip() for c in df.columns]
        
        # Konwersja Strike i IV na liczby (usuwanie przecinków i %)
        for col in ['Strike', 'IV']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(r'[%,"]', '', regex=True).astype(float)
        
        # Filtrowanie i rysowanie wykresu dla PUTów
        if 'Type' in df.columns:
            df_puts = df[df['Type'].str.contains('Put', case=False, na=False)].sort_values('Strike')
            if not df_puts.empty:
                st.line_chart(df_puts.set_index('Strike')['IV'])
                st.success("Wykres wygenerowany!")
        else:
            st.error("Błąd: Nie znaleziono kolumny 'Type'. Skopiuj tabelę z nagłówkami.")
            
    except Exception as e:
        st.error(f"Techniczny błąd: {e}")
