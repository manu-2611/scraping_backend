from typing import Any, Dict

from settings import DB_NAME, HOST, PASSWORD, SQL_PORT, USERNAME
from storage.storage import StorageClass


class SQLStorage(StorageClass):
    def __int__(self,):
        self.connection_string = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{SQL_PORT}/{DB_NAME}"

    def create(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("Extend the function to perform the working of this logic.")

    def get(self) -> Dict[str, Any]:
        raise NotImplementedError("Extend the function to perform the working of this logic.")
