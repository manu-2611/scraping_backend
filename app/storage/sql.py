from storage.storage import StorageClass
from typing import Dict, Any
from settings import SQL_PORT, USERNAME, PASSWORD, DB_NAME, HOST
class SQLStorage(StorageClass):
    def __int__(self,):
        self.connection_string = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{SQL_PORT}/{DB_NAME}"

    def create(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("Extend the function to perform the working of this logic.")

    def get(self) -> Dict[str, Any]:
        raise NotImplementedError("Extend the function to perform the working of this logic.")
