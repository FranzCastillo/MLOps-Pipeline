from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from .dataset import load_titanic
from sklearn import set_config
from IPython.display import display

def build_pipeline():
    df = load_titanic()

    features = ["pclass", "sex", "age", "fare", "embarked"]
    target = "survived"

    X = df[features]
    y = df[target]

    numeric_features = ["age", "fare"]
    categorical_features = ["pclass", "sex", "embarked"]

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])

    return clf, X, y


def train_and_evaluate(test_size=0.2, random_state=42):
    clf, X, y = build_pipeline()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    return clf, score


def show_pipeline(clf):
    set_config(display="diagram")
    display(clf)