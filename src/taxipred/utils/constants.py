from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"
MODEL_PATH = PROJECT_ROOT / "model.joblib"
FEATURES_PATH = PROJECT_ROOT / "feature_names.joblib"