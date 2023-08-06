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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types

class AddStickerToSet:
    async def add_sticker_to_set(
        self: "pyrogram.Client",
        set_short_name: str,
        sticker: str,
        emoji: str = "🤔",
    ) -> "types.StickerSet":
        """Get info about a stickerset.

        .. include:: /_includes/usable-by/users-bot.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

            sticker (``str`` | ``BinaryIO``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass a file path as string to upload a new file that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

        Returns:
            :obj:`~pyrogram.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.add_sticker_to_set("mypack1", "/home/myuser/file.png")
        """
        file = None

        if isinstance(sticker, str):
            if os.path.isfile(sticker):
                file = await self.save_file(sticker, progress=progress, progress_args=progress_args)
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
            file = await self.save_file(sticker, progress=progress, progress_args=progress_args)
            media = raw.types.InputDocument(
                id=file.id,
                access_hash=file.access_hash,
                file_reference=file.file_reference
            )

        r = await self.invoke(
            raw.functions.messages.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                sticker=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ]
            )
        )

        return types.StickerSet._parse(r.set)
