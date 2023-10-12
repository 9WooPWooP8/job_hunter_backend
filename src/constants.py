from enum import Enum

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL)

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION)
