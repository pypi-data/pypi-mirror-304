"""basemetainformationtable.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any, Union

# Third-Party Packages #
from sqlalchemy import select, lambda_stmt
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

# Local Packages #
from .basetable import BaseTable


# Definitions #
# Classes #
class BaseMetaInformationTable(BaseTable):
    """A table for storing meta-information in a SQLAlchemy ORM model.

    This class extends the BaseTable class and provides additional methods for creating, retrieving, and updating
    meta-information entries in the table.

    Class Attributes:
        __tablename__: The name of the table.
        __mapper_args__: Mapper arguments for SQLAlchemy ORM configurations.
    """

    # Class Attributes #
    __tablename__ = "metainformation"
    __mapper_args__ = {"polymorphic_identity": "metainformation"}

    # Class Methods #
    @classmethod
    def create_information(
        cls,
        session: Session,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Creates or updates meta-information in the table.

        If an entry already exists, it updates the entry; otherwise, it inserts a new entry.

        Args:
            session: The SQLAlchemy session to use for the operation.
            entry: A dictionary representing the entry to create or update. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        if begin:
            with session.begin():
                result = session.execute(lambda_stmt(lambda: select(cls))).scalar()
                if result is None:
                    cls.insert(session=session, entry=entry, as_entry=True, begin=False, **kwargs)
                else:
                    result.update(entry, **kwargs)
        else:
            result = session.execute(lambda_stmt(lambda: select(cls))).scalar()
            if result is None:
                cls.insert(session=session, entry=entry, as_entry=True, begin=False, **kwargs)
            else:
                result.update(entry, **kwargs)

    @classmethod
    async def create_information_async(
        cls,
        session: AsyncSession,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Asynchronously creates or updates meta-information in the table.

        If an entry already exists, it updates the entry; otherwise, it inserts a new entry.

        Args:
            session: The SQLAlchemy async session to use for the operation.
            entry: A dictionary representing the entry to create or update. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        statement = lambda_stmt(lambda: select(cls))
        if begin:
            async with session.begin():
                result = (await session.execute(statement)).scalar()
                if result is None:
                    await cls.insert_async(session=session, entry=entry, as_entry=True, begin=False, **kwargs)
                else:
                    result.update(entry, **kwargs)
        else:
            result = (await session.execute(statement)).scalar()
            if result is None:
                await cls.insert_async(session=session, entry=entry, as_entry=True, begin=False, **kwargs)
            else:
                result.update(entry, **kwargs)

    @classmethod
    def get_information(
        cls,
        session: Session,
        as_entry: bool = True,
    ) -> Union[dict[str, Any], "BaseMetaInformationTable"]:
        """Retrieves meta-information from the table.

        Args:
            session: The SQLAlchemy session to use for the query.
            as_entry: If True, returns the entry as a dictionary; otherwise, returns the table object. Defaults to True.

        Returns:
            Union[dict[str, Any], BaseMetaInformationTable]: The meta-information entry, either as a dictionary or as a table object.
        """
        result = session.execute(lambda_stmt(lambda: select(cls))).scalar()
        return (result.as_entry() if as_entry else result) if result is not None else {}

    @classmethod
    async def get_information_async(
        cls,
        session: AsyncSession,
        as_entry: bool = True,
    ) -> Union[dict[str, Any], "BaseMetaInformationTable"]:
        """Asynchronously retrieves meta-information from the table.

        Args:
            session: The SQLAlchemy async session to use for the query.
            as_entry: If True, returns the entry as a dictionary; otherwise, returns the table object. Defaults to True.

        Returns:
            Union[dict[str, Any], BaseMetaInformationTable]: The meta-information entry, either as a dictionary or as a table object.
        """
        result = (await session.execute(lambda_stmt(lambda: select(cls)))).scalar()
        return (result.as_entry() if as_entry else result) if result is not None else {}

    @classmethod
    def set_information(
        cls,
        session: Session,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Sets meta-information in the table.

        Updates the existing entry with the provided information.

        Args:
            session: The SQLAlchemy session to use for the operation.
            entry: A dictionary representing the entry to update. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        if begin:
            with session.begin():
                session.execute(lambda_stmt(lambda: select(cls))).scalar().update(entry, **kwargs)
        else:
            session.execute(lambda_stmt(lambda: select(cls))).scalar().update(entry, **kwargs)

    @classmethod
    async def set_information_async(
        cls,
        session: AsyncSession,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Asynchronously sets meta-information in the table.

        Updates the existing entry with the provided information.

        Args:
            session: The SQLAlchemy async session to use for the operation.
            entry: A dictionary representing the entry to update. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
            **kwargs: Additional keyword arguments for the entry.
        """
        statement = lambda_stmt(lambda: select(cls))
        if begin:
            async with session.begin():
                (await session.execute(statement)).scalar().update(entry, **kwargs)
        else:
            (await session.execute(statement)).scalar().update(entry, **kwargs)
