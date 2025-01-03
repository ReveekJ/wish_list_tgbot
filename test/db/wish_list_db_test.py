import pytest
from src.db.wish_lists.crud import WishListCRUD
from src.db.wish_lists.schemas import WishList

@pytest.fixture
def wish_list_crud():
    return WishListCRUD()

@pytest.fixture
def sample_wish_list():
    wish_list = WishList(
        id=1,
        user_id=1,
        members=[],
        wishes=[]
    )
    return wish_list

def test_create_wish_list(wish_list_crud, sample_wish_list):
    wish_list_crud.create(sample_wish_list)
    assert True  # Check that it runs without error
    wish_list_crud.delete(sample_wish_list.id)

def test_get_wish_list(wish_list_crud, sample_wish_list):
    wish_list_crud.create(sample_wish_list)
    retrieved_wish_list = wish_list_crud.get(sample_wish_list.id)
    assert retrieved_wish_list.id == sample_wish_list.id
    wish_list_crud.delete(sample_wish_list.id)

def test_get_all_wish_lists(wish_list_crud, sample_wish_list):
    wish_list_crud.create(sample_wish_list)
    wish_lists = wish_list_crud.get_all()
    assert len(wish_lists) == 1
    assert wish_lists[0].id == sample_wish_list.id
    wish_list_crud.delete(sample_wish_list.id)

def test_update_wish_list(wish_list_crud, sample_wish_list):
    wish_list_crud.create(sample_wish_list)
    updated_data = {"members": [], "wishes": []}
    updated_wish_list = wish_list_crud.update(sample_wish_list.id, updated_data)
    assert updated_wish_list.members == updated_data["members"]
    assert updated_wish_list.wishes == updated_data["wishes"]
    wish_list_crud.delete(sample_wish_list.id)

def test_delete_wish_list(wish_list_crud, sample_wish_list):
    wish_list_crud.create(sample_wish_list)
    deleted_wish_list = wish_list_crud.delete(sample_wish_list.id)
    assert deleted_wish_list.id == sample_wish_list.id
    assert wish_list_crud.get(sample_wish_list.id) is None
