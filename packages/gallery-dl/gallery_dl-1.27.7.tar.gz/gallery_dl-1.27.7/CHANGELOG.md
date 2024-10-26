## 1.27.7 - 2024-10-25
### Extractors
#### Additions
- [civitai] add extractors for global `models` and `images` ([#6310](https://github.com/mikf/gallery-dl/issues/6310))
- [mangadex] add `author` extractor ([#6372](https://github.com/mikf/gallery-dl/issues/6372))
- [scrolller] add support ([#295](https://github.com/mikf/gallery-dl/issues/295), [#3418](https://github.com/mikf/gallery-dl/issues/3418), [#5051](https://github.com/mikf/gallery-dl/issues/5051))
#### Fixes
- [8chan] automatically detect `TOS` cookie name ([#6318](https://github.com/mikf/gallery-dl/issues/6318))
- [bunkr] update to new site layout ([#6344](https://github.com/mikf/gallery-dl/issues/6344), [#6352](https://github.com/mikf/gallery-dl/issues/6352), [#6368](https://github.com/mikf/gallery-dl/issues/6368))
- [bunkr] send proper `Referer` headers for file downloads ([#6319](https://github.com/mikf/gallery-dl/issues/6319))
- [civitai] add `uuid` metadata field & use it as default archive format ([#6326](https://github.com/mikf/gallery-dl/issues/6326))
- [civitai] fix "My Reactions" results ([#6263](https://github.com/mikf/gallery-dl/issues/6263))
- [civitai] fix `model` file download URLs for tRPC API
- [lensdump] fix extraction ([#6313](https://github.com/mikf/gallery-dl/issues/6313))
- [pixiv] make retrieving ugoira metadata non-fatal ([#6297](https://github.com/mikf/gallery-dl/issues/6297))
- [pixiv] fix exception when processing deleted `sanity_level` works ([#6339](https://github.com/mikf/gallery-dl/issues/6339))
- [urlgalleries] fix extraction
- [wikimedia] fix non-English Fandom/wiki.gg articles ([#6370](https://github.com/mikf/gallery-dl/issues/6370))
#### Improvements
- [8chan] support `/last/` thread URLs ([#6318](https://github.com/mikf/gallery-dl/issues/6318))
- [bunkr] support `bunkr.ph` and `bunkr.ps` URLs
- [newgrounds] support page numbers in URLs ([#6320](https://github.com/mikf/gallery-dl/issues/6320))
- [patreon] support `/c/` prefix in creator URLs ([#6348](https://github.com/mikf/gallery-dl/issues/6348))
- [pinterest] support `story` pins ([#6188](https://github.com/mikf/gallery-dl/issues/6188), [#6078](https://github.com/mikf/gallery-dl/issues/6078), [#4229](https://github.com/mikf/gallery-dl/issues/4229))
- [pixiv] implement `sanity_level` workaround for user artworks results ([#4327](https://github.com/mikf/gallery-dl/issues/4327), [#5435](https://github.com/mikf/gallery-dl/issues/5435), [#6339](https://github.com/mikf/gallery-dl/issues/6339))
#### Options
- [bluesky] add `quoted` option ([#6323](https://github.com/mikf/gallery-dl/issues/6323))
- [pixiv] add `captions` option ([#4327](https://github.com/mikf/gallery-dl/issues/4327))
- [reddit] add `embeds` option ([#6357](https://github.com/mikf/gallery-dl/issues/6357))
- [vk] add `offset` option ([#6328](https://github.com/mikf/gallery-dl/issues/6328))
### Downloaders
- [ytdl] implement explicit HLS/DASH handling
### Post Processors
- add `error` event
### Miscellaneous
- [cookies] convert Chromium `expires_utc` values to Unix timestamps
- [util] add `std` object to global eval namespace ([#6330](https://github.com/mikf/gallery-dl/issues/6330))
- add `--print` and `--print-to-file` command-line options ([#6343](https://github.com/mikf/gallery-dl/issues/6343))
- use child extractor fallbacks only when a non-user error occurs ([#6329](https://github.com/mikf/gallery-dl/issues/6329))
