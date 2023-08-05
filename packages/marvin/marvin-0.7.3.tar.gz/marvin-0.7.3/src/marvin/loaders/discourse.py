from typing import Callable, Dict

import httpx
import pendulum
from pydantic import BaseModel, Field, validator

import marvin
from marvin.loaders.base import Loader
from marvin.models.documents import Document
from marvin.models.metadata import Metadata


def should_include_post(post: dict) -> bool:
    """Return whether the post should be included in the results."""
    return post["accepted_answer"]


class DiscoursePost(BaseModel):
    """Discourse post."""

    base_url: str
    id: int
    category_id: int
    cooked: str
    created_at: pendulum.DateTime
    topic_id: int
    topic_slug: str
    topic_title: str

    @property
    def url(self) -> str:
        """Return the URL for the post."""
        return f"{self.base_url}/t/{self.topic_slug}/{self.topic_id}"


class DiscourseLoader(Loader):
    """Loader for Discourse posts."""

    source_type: str = Field(default="discourse")

    url: str = Field(default="https://discourse.prefect.io")
    n_posts: int = Field(default=50)
    request_headers: Dict[str, str] = Field(default_factory=dict)
    include_post_filter: Callable[[dict], bool] = Field(default=should_include_post)

    @validator("request_headers", always=True)
    def auth_headers(cls, v):
        """Add authentication headers if a Discourse token is available."""
        if not (api_key := marvin.settings.DISCOURSE_API_KEY.get_secret_value()):
            marvin.get_logger().warning(
                "No Discourse API key found - some endpoints may be inaccessible. You"
                " can set `DISCOURSE_API_KEY` and `DISCOURSE_API_USERNAME` in your"
                " environment."
            )
        v.update(
            {
                "Api-Key": api_key,
                "Api-Username": marvin.settings.DISCOURSE_API_USERNAME,
            }
        )
        return v

    async def load(self) -> list[Document]:
        """Load Discourse posts."""
        documents = []
        for post in await self._get_posts():
            documents.extend(
                await Document(
                    text=post.cooked,
                    metadata=Metadata(
                        source=self.source_type,
                        title=post.topic_title,
                        link=post.url,
                        created_at=post.created_at.timestamp(),
                    ),
                ).to_excerpts()
            )
        return documents

    async def _get_posts(self) -> list[DiscoursePost]:
        """Get posts from a Discourse forum."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/posts.json", headers=self.request_headers
            )
            response.raise_for_status()
            return [
                DiscoursePost(base_url=self.url, **post)
                for post in response.json()["latest_posts"]
                if self.include_post_filter(post)
            ]
