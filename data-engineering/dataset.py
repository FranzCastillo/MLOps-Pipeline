from sklearn.datasets import fetch_openml

def load_titanic():
    """Carga el dataset Titanic desde OpenML como DataFrame."""
    titanic = fetch_openml("titanic", version=1, as_frame=True)
    df = titanic.frame
    return df
