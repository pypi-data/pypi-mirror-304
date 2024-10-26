

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class DatabaseMethods:
    def __init__(self, db: AsyncSession):
        self.db = db

    # READ methods
    async def get_list(self, model):
        """Retrieve a list of elements from database."""
        result = await self.db.execute(select(model))
        item_list = result.unique().scalars().all()
        return item_list

    async def get_list_statement_result(self, stmt):
        """Execute given statement and return list of items."""
        result = await self.db.execute(stmt)
        item_list = result.unique().scalars().all()
        return item_list

    async def get_element_statement_result(self, stmt):
        """Execute statement and return a single item."""
        result = await self.db.execute(stmt)
        item = result.scalar()
        return item

    async def get_element_by_id(self, model, element_id):
        """Retrieve any DB element by id."""
        if element_id is None:
            return None
        element = await self.db.get(model, element_id)
        return element

    # DELETE method
    async def delete_element_by_id(self, model, element_id):
        """Delete any DB element by id."""
        element = await self.get_element_by_id(model, element_id)
        if element is not None:
            await self.db.delete(element)
            await self.db.commit()
        return element