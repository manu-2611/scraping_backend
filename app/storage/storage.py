from typing import Any, Dict


class StorageClass:
    def create(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("Extend the function to perform the working of this logic.")

    def get(self) -> Dict[str, Any]:
        raise NotImplementedError("Extend the function to perform the working of this logic.")
