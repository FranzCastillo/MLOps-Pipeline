import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(shared_dir="/shared"):
    # Load processed data
    X, y = joblib.load(f"{shared_dir}/dataset.pkl")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(f"🎯 Model accuracy: {score:.4f}")

    # Save trained model
    joblib.dump(clf, f"{shared_dir}/model.pkl")
    print("✅ Model trained and saved at /shared/model.pkl")

if __name__ == "__main__":
    train_model()
