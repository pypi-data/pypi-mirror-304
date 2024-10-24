from __future__ import annotations

from digitalhub.entities._base._base.entity import Base


class Metadata(Base):
    """
    A class representing the metadata of an entity.
    Metadata is a collection of information about an entity thought
    to be modifiable by the user. The information contained in the
    metadata can be discordant with the actual state of the entity,
    for example the name of the entity in the database.
    """

    def __init__(
        self,
        project: str | None = None,
        name: str | None = None,
        version: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        created: str | None = None,
        created_by: str | None = None,
        updated: str | None = None,
        updated_by: str | None = None,
        embedded: bool | None = None,
        ref: str | None = None,
        **kwargs,
    ) -> None:
        self.project = project
        self.name = name
        self.version = version
        self.description = description
        self.labels = labels
        self.created = created
        self.updated = updated
        self.created_by = created_by
        self.updated_by = updated_by
        self.embedded = embedded
        self.ref = ref

        self._any_setter(**kwargs)

    @classmethod
    def from_dict(cls, obj: dict) -> Metadata:
        """
        Return entity metadata object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity metadata.

        Returns
        -------
        Metadata
            An entity metadata object.
        """
        return cls(**obj)
