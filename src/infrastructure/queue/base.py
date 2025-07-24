from abc import ABC, abstractmethod

# class BaseQueue(ABC):
#     @abstractmethod
#     def publish(self, channel: str, message: str):
#         """发布消息到指定频道"""
#         pass
#
#     @abstractmethod
#     def subscribe(self, channel: str):
#         """订阅指定频道的消息"""
#         pass


class BaseQueue(ABC):
    @abstractmethod
    async def publish(self, channel: str, message: str):
        """发布消息到指定频道"""
        pass

    @abstractmethod
    async def subscribe(self, channel: str):
        """订阅指定频道的消息"""
        pass