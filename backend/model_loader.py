import pandas as pd
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), "xgboost_model.pkl")
xgb_model = joblib.load(model_path)

def preprocess(df):
    # Step 1: Convert attendance to float
    if 'attendance' in df.columns:
        df['attendance'] = df['attendance'].apply(
            lambda x: float(str(x).replace('%', '')) if isinstance(x, str) and '%' in x else float(x)
        )

    # Step 2: Split quizzes
    if 'quizzes' in df.columns:
        quizzes_split = df['quizzes'].astype(str).str.split(',', expand=True)
        df['quiz1'] = quizzes_split[0].astype(float)
        df['quiz2'] = quizzes_split[1].astype(float)
        df['quiz3'] = quizzes_split[2].astype(float)
        df.drop(columns=['quizzes'], inplace=True)

    # Step 3: Compute avg_quiz_score
    df['avg_quiz_score'] = df[['quiz1', 'quiz2', 'quiz3']].mean(axis=1)

    # Step 4: Rename attendance -> attendance_pct
    df.rename(columns={'attendance': 'attendance_pct'}, inplace=True)

    # Step 5: If performance_label is not in CSV, set dummy value (only needed if model expects it)
    if 'performance_label' not in df.columns:
        df['performance_label'] = 0  # dummy value (won't be used for prediction, just avoids crash)

    # Final columns
    return df[['avg_quiz_score', 'attendance_pct', 'performance_label']]


def predict(file_path):
    df = pd.read_csv(file_path, encoding="ISO-8859-1", on_bad_lines='skip')

    # Drop target label if present
    if 'performance' in df.columns:
        df = df.drop(columns=['performance'])

    df = preprocess(df)
    predictions = xgb_model.predict(df)
    df['prediction'] = predictions

    # Convert DataFrame to JSON list of dicts
    return df.to_dict(orient="records")
