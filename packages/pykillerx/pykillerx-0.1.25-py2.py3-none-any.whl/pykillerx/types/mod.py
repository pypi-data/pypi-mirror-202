# library mod by @xtsea

class SendPhoto:
    def __init__(self, chat_id, ph, replywithme, caption=None):
        self.chat_id = chat_id
        self.ph = ph
        self.caption = caption
        self.replywithme = replywithme

    async def __call__(self, client):
        if self.caption is None:
            await client.send_photo(self.chat_id, photo=self.ph, reply_to_message_id=self.replywithme)
        else:
            await client.send_photo(self.chat_id, photo=self.ph, caption=self.caption, reply_to_message_id=self.replywithme)


class SendVideo:
    def __init__(self, chat_id, vd, replywithme, caption=None):
        self.chat_id = chat_id 
        self.vd = vd
        self.replywithme = replywithme
        self.caption = caption

    async def __call__(self, client):
        if self.caption is None:
            await client.send_video(self.chat_id, video=self.vd, reply_to_message_id=self.replywithme)
        else:
            await client.send_video(self.chat_id, video=self.vd, caption=self.caption, reply_to_message_id=self.replywithme)


class SendMessage:
    def __init__(self, chat_id, txt, replywithme):
        self.chat_id = chat_id
        self.txt = txt
        self.replywithme = replywithme

    async def __call__(self, client):
        await client.send_message(self.chat_id, text=self.txt, reply_to_message_id=self.replywithme)


class SendSticker:
    def __init__(self, chat_id, stkr, replywithme):
        self.chat_id = chat_id
        self.stkr = stkr
        self.replywithme = replywithme

    async def __call__(self, client):
        await client.send_sticker(self.chat_id, sticker=self.stkr, reply_to_message_id=self.replywithme)


class SendDocument:
    def __init__(self, chat_id, dmt, replywithme, caption=None):
        self.chat_id = chat_id
        self.dmt = dmt
        self.replywithme = replywithme
        self.caption = caption

    async def __call__(self, client):
        if self.caption is None:
            await client.send_document(self.chat_id, document=self.dmt, reply_to_message_id=self.replywithme)
        else:
            await client.send_document(self.chat_id, document=self.dmt, caption=self.caption, reply_to_message_id=self.replywithme)
