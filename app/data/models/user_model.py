from app.database import db
from app.data.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(100), nullable=False, index=True)

    def __repr__(self):
        return f"<UserModel id={self.id} name='{self.name}'>"
