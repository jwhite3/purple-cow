import logging

from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from cow import __version__ as cow_version
from cow.app.models import Item

logger = logging.getLogger(__name__)

app = FastAPI(
    title='Purple Cow',
    version=f'{cow_version}',
    description='Moo!'
)

try:  # Serve sphinx docs if they exist; not sure that I'll have time to add the actual docs though
    app.mount("/design-docs", StaticFiles(directory="docs/_build", html=True), name="static")
except RuntimeError:
    pass

current_items: dict = {}


@app.get("/")
async def home():
    """Redirect requests to root to API documentation."""
    return RedirectResponse(url='/redoc')


@app.get('/items/', response_model=list[Item])
async def get_all_items(limit: int = 10) -> list[Item]:
    """Get all available items."""
    items = list(current_items.values())

    if limit:
        return items[:limit]

    return items


@app.post('/items/', response_model=Item)
async def add_item(item: Item) -> Item:
    # TODO: This is subject to race-condition; needs to be protected.
    if item.id in current_items:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Item with id, {item.id} already exists.")

    current_items[item.id] = item
    return item


@app.put('/items/', status_code=status.HTTP_201_CREATED)
async def put_items(items: list[Item]):
    """Set available items."""
    current_items.clear()
    current_items.update({item.id: item for item in items})


@app.delete('/items/')
async def delete_items():
    """Delete all items."""
    current_items.clear()


@app.get('/items/{item_id}', response_model=Item)
async def get_item(item_id: int) -> Item:
    """Get a particular item given an item id."""
    try:
        return current_items[item_id]
    except KeyError:
        # TODO: This exception is common and should be hoisted rather than duplicated
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id, {item_id} not found.")


@app.post('/items/{item_id}', response_model=Item)
def update_item(item_id: int, name: str = Body(embed=True)) -> Item:
    try:
        item = current_items[item_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id, {item_id} not found.")

    item.name = name

    return item


@app.delete('/items/{item_id}', response_model=Item)
def delete_item(item_id: int) -> Item:
    try:
        return current_items.pop(item_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id, {item_id} not found")
