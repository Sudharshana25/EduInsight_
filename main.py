from utils.data_preprocessing import load_and_preprocess_data

if __name__ == "__main__":
    file_path = "data/student_data.csv"  # Make sure this file exists
    df = load_and_preprocess_data(file_path)
    print("✅ Data Loaded & Preprocessed:")
    print(df.head())
