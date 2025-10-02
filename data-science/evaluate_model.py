import os
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def evaluate_model(shared_dir="/shared"):
    # Check if files exist and handle errors properly
    dataset_path = f"{shared_dir}/dataset.pkl"
    model_path = f"{shared_dir}/model.pkl"

    # Verify files exist
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset file not found at {dataset_path}")
        return

    if not os.path.exists(model_path):
        print(f"❌ Error: Model file not found at {model_path}")
        return

    # Check file size - empty files will cause EOFError
    if os.path.getsize(model_path) == 0:
        print(f"❌ Error: Model file at {model_path} is empty")
        return

    try:
        # Load processed dataset
        X, y = joblib.load(dataset_path)

        # Load trained model
        clf = joblib.load(model_path)

        # Split again to get test data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Evaluate model
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        print(f"📊 Loaded model accuracy: {acc:.4f}")
    except EOFError:
        print(f"❌ Error: The model file at {model_path} is corrupted or incomplete")
        print("Make sure the model training process completed successfully")
    except Exception as e:
        print(f"❌ Error during evaluation: {str(e)}")


if __name__ == "__main__":
    evaluate_model()
