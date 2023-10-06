from sqlmodel import SQLModel, Field


class ArticleTag(SQLModel, table=True):
    __tablename__ = 'articles_tags'

    article_id: int | None = Field(
        default=None, foreign_key='articles.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='tags.id', primary_key=True
    )


class ArticleDistrict(SQLModel, table=True):
    __tablename__ = 'articles_districts'

    article_id: int | None = Field(
        default=None, foreign_key='articles.id', primary_key=True
    )
    district_id: int | None = Field(
        default=None, foreign_key='districts.id', primary_key=True
    )
