#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
from typing import Union, BinaryIO, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.file_id import FileId


class CreateStickerSet:
    async def create_sticker_set(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        title: str,
        short_name: str,
        sticker: Union[str, BinaryIO],
        emoji: str = "🤔",
        masks: bool = None,
        animated: bool = None,
        videos: bool = None,
        emojis: bool = None
    ) -> Optional["types.Message"]:
        """Send generic files.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the Stickerset owner.
                For you yourself you can simply use "me" or "self" (users only).

            title (``str``):
                Stickerset name, 1-64 chars

            short_name (``str`` | ``BinaryIO``, *optional*):
                Short name of sticker set, to be used in sticker deep links.
                Can contain only english letters, digits and underscores.
                Must begin with a letter, can't contain consecutive underscores and, if called by a bot, must end in "_by_<bot_username>".
                <bot_username> is case insensitive. 1-64 characters.

            sticker (``str`` | ``BinaryIO``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass a file path as string to upload a new file that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

            masks (``bool``, *optional*):
                Whether this is a mask stickerset.

            animated (``bool``, *optional*):
                Whether this is a animated stickerset.

            videos (``bool``, *optional*):
                Whether this is a videos stickerset.

            emojis (``bool``, *optional*):
                Whether this is a emojis stickerset.

        Returns:
            :obj:`~pyrogram.types.StickerSet` | ``None``: On success, the StickerSet is returned.

        Example:
            .. code-block:: python

                # Send document by uploading from local file
                await app.create_sticker_set("me", "My First Pack", "myfirstpack", "/home/myuser/file.png")
        """
        file = None

        if isinstance(sticker, str):
            if os.path.isfile(sticker):
                file = await self.save_file(sticker)
                media = raw.types.InputDocument(
                    id=file.id,
                    access_hash=file.access_hash,
                    file_reference=file.file_reference
                )
            elif re.match("^https?://", sticker):
                raise ValueError(f"Url is not supported!")
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference
                )
        else:
            file = await self.save_file(sticker)
            media = raw.types.InputDocument(
                id=file.id,
                access_hash=file.access_hash,
                file_reference=file.file_reference
            )

        r = await self.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id),
                title=title,
                short_name=short_name,
                stickers=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ],
                masks=masks,
                animated=animated,
                videos=videos,
                emojis=emojis
            )
        )

        return types.StickerSet._parse(r.set)
