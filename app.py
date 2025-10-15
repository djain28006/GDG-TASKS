# app.py
import streamlit as st
import pandas as pd
import joblib

# Compatibility shim: some pipelines saved with scikit-learn 1.6.1 include
# a private helper type _RemainderColsList inside sklearn.compose._column_transformer.
# Newer or different installs may not expose it which causes unpickling to fail
# with AttributeError. Define a small placeholder class if it's missing so the
# object can be unpickled. If you re-train/re-save the pipeline using your
# current scikit-learn version, you can remove this shim.
try:
    import sklearn.compose._column_transformer as _ct
    if not hasattr(_ct, '_RemainderColsList'):
        class _RemainderColsList(list):
            pass
        _ct._RemainderColsList = _RemainderColsList
except Exception:
    # If sklearn isn't available yet or import fails, we ignore and let joblib
    # raise a clearer error when loading.
    pass

# ----------------------
# Load trained pipeline
# ----------------------
pipe = joblib.load('f1_finish_pipeline.pkl')  # pipeline includes preprocessing

st.set_page_config(page_title="F1 Finish Predictor", layout="wide")
st.title("🏁 F1 Finish Predictor")
st.markdown("""
Predict whether a driver is likely to **FINISH** (`target_finish=1`) or **NOT FINISH** (`target_finish=0`) a race.
Provide a few key race features below.
""")

# ----------------------
# Define dropdown options (replace with values from training)
# ----------------------
driver_options = ["Lewis Hamilton", "Max Verstappen", "Charles Leclerc", "Fernando Alonso"]
circuit_options = ["Silverstone", "Monza", "Circuit Paul Ricard", "Suzuka"]
country_options = ["UK", "Italy", "France", "Japan"]
year_options = [2023, 2024, 2025]

# ----------------------
# User inputs
# ----------------------
st.subheader("Driver & Circuit")
driver = st.selectbox("Driver", options=driver_options)
circuit = st.selectbox("Circuit", options=circuit_options)
country = st.selectbox("Country", options=country_options)
year = st.selectbox("Year", options=year_options)

st.subheader("Race Features")
grid = st.number_input("Starting grid position", min_value=1, max_value=30, value=10)
laps = st.number_input("Laps completed", min_value=0, max_value=200, value=52)
milliseconds = st.number_input("Race time in ms (optional)", min_value=0, value=0)
fastestLap = st.number_input("Fastest lap number", min_value=0, max_value=500, value=30)
rank = st.number_input("Fastest lap rank", min_value=0, max_value=1000, value=1)
fastestLapSpeed = st.number_input("Fastest lap speed (km/h)", min_value=0.0, value=200.0, step=0.1)

# ----------------------
# Predict button
# ----------------------
if st.button("Predict"):
    # Build input dataframe (same order as training)
    input_df = pd.DataFrame({
        'grid':[grid],
        'laps':[laps],
        'milliseconds':[milliseconds],
        'fastestLap':[fastestLap],
        'rank':[rank],
        'fastestLapSpeed':[fastestLapSpeed],
        'name':[driver],
        'circuitId':[circuit],
        'country':[country],
        'year':[year]
    })

    # Predict using saved pipeline
    pred = pipe.predict(input_df)[0]
    prob = pipe.predict_proba(input_df)[0][1]

    # Show results
    st.markdown("### Prediction")
    if pred == 1:
        st.success(f" Predicted: FINISH\nProbability: {prob:.3f}")
    else:
        st.error(f" Predicted: NOT FINISH\nProbability: {prob:.3f}")

    # Optional: show input used
    st.markdown("#### Input features used:")
    st.table(input_df.T.rename(columns={0:'Value'}))
