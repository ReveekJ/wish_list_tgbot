import datetime

import pytest

from src.db.users.crud import UserCRUD
from src.db.users.enums import GenderEnum
from src.db.users.schemas import User


@pytest.fixture
def user_crud():
    return UserCRUD()

@pytest.fixture
def sample_user():
    user = User(
        id=1,
        name='aaaa',
        username='bbb',
        birthdate=datetime.date.today(),
        gender=GenderEnum.MALE,
    )
    return user

def test_create_user(user_crud, sample_user):
    user_crud.create(sample_user)
    assert True # проверка на то что запустилось без ошибки
    user_crud.delete(sample_user.id)


def test_get_user(user_crud, sample_user):
    user_crud.create(sample_user)
    retrieved_user = user_crud.get_obj_by_id(sample_user.id)
    assert retrieved_user.id == sample_user.id
    user_crud.delete(sample_user.id)


def test_get_users(user_crud, sample_user):
    user_crud.create(sample_user)
    users = user_crud.get_all()
    assert len(users) == 1
    assert users[0].id == sample_user.id
    user_crud.delete(sample_user.id)


def test_update_user(user_crud, sample_user):
    user_crud.create(sample_user)
    updated_data = {"own_wish_lists": [], "member_wish_lists": []}
    updated_user = user_crud.update(sample_user.id, updated_data)
    assert updated_user.own_wish_lists == updated_data["own_wish_lists"]
    user_crud.delete(sample_user.id)

def test_delete_user(user_crud, sample_user):
    user_crud.create(sample_user)
    deleted_user = user_crud.delete(sample_user.id)
    assert deleted_user.id == sample_user.id
    assert user_crud.get_obj_by_id(sample_user.id) is None
