from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rfeed import (
    Category,
    Enclosure,
    Feed,
    Guid,
    Image,
    Item,
    iTunes,
    iTunesItem,
    iTunesOwner,
)

from nrk_psapi.const import LOGGER as _LOGGER, NRK_RADIO_BASE_URL
from nrk_psapi.utils import get_image

from .extensions import (
    Podcast,
    PodcastChapters,
    PodcastImages,
    PodcastImagesImage,
    PodcastPerson,
)

if TYPE_CHECKING:
    from nrk_psapi import NrkPodcastAPI
    from nrk_psapi.models import (
        Episode,
        PodcastSeries,
    )
    from nrk_psapi.models.rss import EpisodeChapter


@dataclass
class NrkPodcastFeed:
    api: NrkPodcastAPI
    """API instance."""
    base_url: str = NRK_RADIO_BASE_URL
    """Base URL. Defaults to NRK_RADIO_BASE_URL."""

    @staticmethod
    async def build_episode_chapters(episode: Episode) -> list[EpisodeChapter]:
        return [
            {
                "title": index_point.title,
                "startTime": index_point.start_point.total_seconds(),
            }
            for index_point in episode.index_points
        ]

    async def build_episode_item(self, episode: Episode, series_data: PodcastSeries) -> Item | None:
        """Build a :class:`rfeed.rfeed.Item` for an episode."""

        _LOGGER.debug("Building episode item: %s", episode.episode_id)
        manifest = await self.api.get_playback_manifest(episode.episode_id, podcast=True)
        episode_file = manifest.playable.assets[0] or None
        if episode_file is None:  # pragma: no cover
            _LOGGER.debug("Episode file not found: %s", episode.episode_id)
            return None
        file_stat = await self.api.fetch_file_info(episode_file.url)
        _LOGGER.debug("File stat: %s", file_stat)

        extensions = []
        if episode.index_points:  # pragma: no cover
            chapters_url = f"{self.base_url}/{series_data.id}/{episode.episode_id}/chapters.json"
            extensions.append(PodcastChapters(chapters_url, "application/json+chapters"))

        return Item(
            title=episode.titles.title,
            description=episode.titles.subtitle,
            guid=Guid(episode.id, isPermaLink=False),
            enclosure=Enclosure(
                url=episode_file.url,
                type=file_stat["content_type"],
                length=file_stat["content_length"],
            ),
            pubDate=episode.date,
            extensions=[
                Podcast(
                    people=[PodcastPerson(name=", ".join(p.name), role=p.role) for p in episode.contributors]
                    if episode.contributors
                    else None,
                ),
                iTunesItem(
                    author=episode.contributors,
                    duration=episode.duration.total_seconds(),
                ),
                *extensions,
            ],
        )

    async def build_podcast_rss(self, podcast_id: str, limit: int | None = None) -> Feed:
        """Build a complete RSS feed for a podcast.

        The RSS feed is returned as a :class:`rfeed.rfeed.Feed` object and can be rendered as
        XML using the :meth:`rfeed.rfeed.Feed.rss` method.
        """

        podcast = await self.api.get_podcast(podcast_id)
        _LOGGER.debug("Building RSS feed for %s (%s)", podcast_id, type(podcast))

        episodes = await self.api.get_podcast_episodes(podcast.series.id, page_size=limit)

        _LOGGER.debug("Found %s episodes", len(episodes))
        if limit is not None:
            episodes = episodes[:limit]

        feed_attrs = {
            "link": f"{self.base_url}/{podcast.series.id}",
        }
        itunes_attrs = {}
        extensions = [
            PodcastImages([PodcastImagesImage(i.url, i.width) for i in podcast.series.image]),
        ]

        if series_image := get_image(podcast.series.image):
            feed_attrs["image"] = Image(
                url=series_image.url,
                width=series_image.width,
                title=podcast.series.title,
                link=feed_attrs["link"],
            )
            itunes_attrs["image"] = series_image.url

        return Feed(
            title=podcast.series.title,
            description=podcast.series.titles.subtitle,
            generator="",
            docs="",
            language="no",
            categories=Category(podcast.series.category.name, podcast.series.category.id),
            copyright="NRK",
            extensions=[
                Podcast(
                    guid=podcast.series.id,
                ),
                iTunes(
                    author="NRK",
                    # subtitle=(description[:255] + '..') if len(description) > 255 else description,
                    summary=podcast.series.titles.subtitle,
                    explicit="clean",
                    owner=iTunesOwner(
                        name="NRK",
                        email="nrkpodcast@nrk.no",
                    ),
                    categories=podcast.series.category.name,
                    **itunes_attrs,
                ),
                *extensions,
            ],
            items=[
                await self.build_episode_item(episode, series_data=podcast.series) for episode in episodes
            ],
            **feed_attrs,
        )
