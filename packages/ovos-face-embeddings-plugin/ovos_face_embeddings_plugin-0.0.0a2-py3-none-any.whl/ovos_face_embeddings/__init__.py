import os.path
from typing import Optional, Union

import face_recognition
import numpy as np
from ovos_chromadb_embeddings import ChromaEmbeddingsDB
from ovos_config.locations import get_xdg_cache_save_path
from ovos_plugin_manager.templates.embeddings import EmbeddingsDB
from ovos_plugin_manager.templates.embeddings import FaceEmbeddingsStore
from ovos_utils.log import LOG


class FaceEmbeddingsRecognitionPlugin(FaceEmbeddingsStore):
    def __init__(self, db: Optional[Union[EmbeddingsDB, str]] = None):
        if db is None:
            db_path = get_xdg_cache_save_path("chromadb")
            os.makedirs(db_path, exist_ok=True)
            db = f"{db_path}/face_prints"
        if isinstance(db, str):
            LOG.info(f"Using chromadb as face embeddings store: {db}")
            db = ChromaEmbeddingsDB(db)
        super().__init__(db)

    def get_face_embeddings(self, frame: np.ndarray) -> np.ndarray:
        return face_recognition.face_encodings(frame)[0]


if __name__ == "__main__":
    # Example usage:
    a = "/home/miro/PycharmProjects/ovos-user-id/a1.jpg"
    a2 = "/home/miro/PycharmProjects/ovos-user-id/a2.jpg"
    b = "/home/miro/PycharmProjects/ovos-user-id/b.jpg"

    f = FaceEmbeddingsRecognitionPlugin()

    e1 = face_recognition.load_image_file(a)
    e2 = face_recognition.load_image_file(a2)
    b = face_recognition.load_image_file(b)

    f.add_face("arnold", e1)
    f.add_face("silvester", b)
    print(f.query(e1))
    print(f.query(e2))
    print(f.query(b))
