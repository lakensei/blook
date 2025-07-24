from ..base import BaseQueue


# class RedisQueue(BaseQueue):
#     def __init__(self, url: str):
#         self.client = redis.from_url(url)
#
#     def publish(self, channel: str, message: str):
#         self.client.publish(channel, message)
#
#     def subscribe(self, channel: str):
#         pubsub = self.client.pubsub()
#         pubsub.subscribe(channel)
#         return pubsub


class RedisQueue(BaseQueue):
    def __init__(self, url: str):
        self.url = url
        self.client = None

    async def connect(self):
        self.client = await aioredis.from_url(self.url)

    async def publish(self, channel: str, message: str):
        if not self.client:
            await self.connect()
        await self.client.publish(channel, message)

    async def subscribe(self, channel: str):
        if not self.client:
            await self.connect()
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub



    # def __init__(self, url: str):
    #     self.client = redis.from_url(url)
    #     self.executor = ThreadPoolExecutor()
    #
    # async def publish(self, channel: str, message: str):
    #     loop = asyncio.get_event_loop()
    #     await loop.run_in_executor(self.executor, self.client.publish, channel, message)
    #
    # async def subscribe(self, channel: str):
    #     loop = asyncio.get_event_loop()
    #     pubsub = await loop.run_in_executor(self.executor, self.client.pubsub)
    #     await loop.run_in_executor(self.executor, pubsub.subscribe, channel)
    #     return pubsub