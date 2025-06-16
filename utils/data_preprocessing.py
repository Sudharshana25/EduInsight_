import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(path):
    df = pd.read_csv(path)

    # 🔥 Drop ID columns that won't help in ML
    if 'student_id' in df.columns:
        df.drop('student_id', axis=1, inplace=True)

    # 🧹 Drop missing rows
    df.dropna(inplace=True)

    # 🎯 Encode categorical columns (skip performance_label)
    label_encoders = {}
    for col in df.select_dtypes(include=["object"]).columns:
        if col != "performance_label":
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

    return df
