# 3. Vault adapter interface (Python Protocol)
# Already embedded above as VaultAdapter, but here it is isolated:

from typing import Protocol, Dict, Any, List


class VaultAdapter(Protocol):
    """
    Interface for accessing subject-specific personal data vaults.
    Implementations may target Dropbox, S3, GDrive, etc.
    """

    def for_subject(self, subject_id: str) -> "VaultAdapter":
        """
        Return a subject-scoped instance of the adapter.
        """
        ...

    async def fetch_fields(
        self,
        fields: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fetch requested fields for the subject (no policy logic here).
        """
        ...

    async def list_inventory(self) -> Dict[str, Any]:
        """
        Return a structured inventory of all known PI for this subject.
        """
        ...