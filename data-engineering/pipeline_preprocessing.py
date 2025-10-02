from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib
from dataset import load_titanic

def build_preprocessor():
    numeric_features = ["age", "fare"]
    categorical_features = ["pclass", "sex", "embarked"]

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )
    return preprocessor

def run_preprocessing(output_dir="/shared"):
    df = load_titanic()
    X = df[["pclass", "sex", "age", "fare", "embarked"]]
    y = df["survived"]

    preprocessor = build_preprocessor()
    X_transformed = preprocessor.fit_transform(X)

    # Save artifacts
    joblib.dump(preprocessor, f"{output_dir}/preprocessor.pkl")
    joblib.dump((X_transformed, y), f"{output_dir}/dataset.pkl")
    print("✅ Preprocessing complete. Artifacts saved in /shared")

if __name__ == "__main__":
    run_preprocessing()
