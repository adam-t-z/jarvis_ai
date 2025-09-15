from huggingface_hub import HfApi
import os

api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_folder(
    folder_path="svm_model.pkl",
    repo_id="SifrAce/face_recognition",
    repo_type="model",
)
