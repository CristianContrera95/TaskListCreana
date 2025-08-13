from contextlib import asynccontextmanager
from logging import getLogger
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions.database import NotFound

logger = getLogger(__name__)


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AsyncCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for async CRUD operations using AsyncSession.
    Args:
        ModelType: SQLModel entity (same model used to create Table in db)
        CreateSchemaType: Pydantic model with same required fields as ModelType
        UpdateSchemaType: Pydantic model with same fields as ModelType

    """

    def __init__(self, model: type[ModelType], session: AsyncSession):
        """
        Initialize CRUD instance with database session.
        Args:
            model: SQLModel model class for the CRUD operations.
            session: SQLAlchemy Session object for database operations.
        """

        self.model = model
        self.session = session

    @asynccontextmanager
    async def safe_transaction(self):
        """Async context manager for safe DB transactions."""
        try:
            yield self.session
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
        finally:
            await self._ensure_clean_state()

    async def _ensure_clean_state(self) -> None:
        if self.session.in_transaction():
            logger.warning("Cleaning up incomplete transaction")
            await self.session.rollback()

    def _get_model_relations(self) -> list[str]:
        return list(self.model.__sqlmodel_relationships__.keys())

    def _add_relations(self, statement):
        relations: list[str] = self._get_model_relations()
        for relation in relations:
            statement = statement.options(selectinload(getattr(self.model, relation)))
        return statement

    async def create(
        self, db_obj: CreateSchemaType, fields_to_exclude: set | None = None
    ) -> ModelType | None:
        try:
            async with self.safe_transaction() as session:
                obj = self.model(**db_obj.model_dump(exclude=fields_to_exclude))
                session.add(obj)
                await session.flush()
                await session.refresh(obj)
                return self.model(**obj.model_dump())
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Failed to create {self.model.__name__}: {db_obj}")
            logger.exception(e)
            return None

    async def execute_stmt(self, statement, with_relations=True):
        try:
            statement = self._add_relations(statement) if with_relations else statement
            result = await self.session.exec(statement)
            return result
        except SQLAlchemyError as e:
            logger.error(f"Failed to execute statement: {statement}")
            logger.exception(e)
            raise

    async def update_by_id(
        self,
        db_obj_id: UUID,
        obj_updater: UpdateSchemaType,
        fields_to_exclude: set | None = None,
    ) -> ModelType | None:
        try:
            async with self.safe_transaction() as session:
                db_obj = await self.get_by_id(db_obj_id)
                if not db_obj:
                    raise NotFound(f"Not found {self.model.__name__}: with id: {db_obj_id}")

                obj_data = obj_updater.model_dump(
                    exclude=fields_to_exclude,
                    exclude_unset=True,
                    exclude_defaults=True,
                    exclude_none=True,
                )

                for field, value in obj_data.items():
                    setattr(db_obj, field, value)

                session.add(db_obj)
                await session.flush()
                await session.refresh(db_obj)
                return self.model(**db_obj.model_dump(mode="json"))
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Failed to update {self.model.__name__}-{db_obj_id}:{obj_updater}"
            )
            logger.exception(e)
            return None

    async def delete_by_id(self, _id: UUID | str) -> bool:
        try:
            async with self.safe_transaction() as session:
                db_obj = await self.session.get(self.model, _id)
                await session.delete(db_obj)
                await self.session.commit()
                return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Failed to delete {self.model.__name__}: {_id}")
            logger.exception(e)
            return False

    async def get_by_id(
        self, _id: UUID | str, with_relations: bool = True
    ) -> ModelType | None:
        stmt = select(self.model)

        stmt = self._add_relations(stmt) if with_relations else stmt

        stmt = stmt.where(getattr(self.model, "id") == _id)  # noqa: B009

        result = await self.session.exec(stmt)  # type: ignore
        return result.one_or_none()

    async def get_list(
            self, with_relations: bool = True
    ) -> list[ModelType]:
        """
        Use filters base from app.schemas.filters.base
        or inherited class to apply filters
        """
        stmt = select(self.model)
        # if filters:
        #     stmt = filters.apply(stmt)

        stmt = self._add_relations(stmt) if with_relations else stmt

        result = await self.session.exec(stmt)
        return list(result.all()) if result is not None else []

    # async def count(self, filters: BaseFilter | None = None) -> int:
    #     stmt = select(func.count()).select_from(self.model)
    #     if filters:
    #         stmt = filters.apply(stmt, paginate=False, sort=False)
    #     result = await self.session.exec(stmt)
    #     return result.one() if result is not None else 0
