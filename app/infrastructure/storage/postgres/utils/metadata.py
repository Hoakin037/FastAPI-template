from app.shared.models import CoreModel

from .load_models import load_all_models

load_all_models()

target_metadata = CoreModel.metadata
