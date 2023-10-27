from sqlmodel import SQLModel, Field


class ArticleDistrict(SQLModel, table=True):
    __tablename__ = 'articles_districts'

    article_id: int | None = Field(
        default=None, foreign_key='articles.id', primary_key=True
    )
    district_id: int | None = Field(
        default=None, foreign_key='districts.id', primary_key=True
    )


class UserDistrict(SQLModel, table=True):
    __tablename__ = 'users_districts'

    user_id: int | None = Field(
        default=None, foreign_key='users.id', primary_key=True
    )
    district_id: int | None = Field(
        default=None, foreign_key='districts.id', primary_key=True
    )
