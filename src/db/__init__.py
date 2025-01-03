from src.db.users.models import *
from src.db.users.schemas import *

from src.db.wish_lists.models import *
from src.db.wish_lists.schemas import *

from src.db.wishes.models import *
from src.db.wishes.schemas import *

from src.db.wish_list_members_secondary.models import *

User.model_rebuild()
Wish.model_rebuild()
WishList.model_rebuild()
