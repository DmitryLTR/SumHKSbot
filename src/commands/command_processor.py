from abc import ABC, abstractmethod
from telegram import Update

class CommandProcessor(ABC):

    @abstractmethod
    def supports(self, command: str) -> bool:
        pass 
    
    @abstractmethod
    async def process(self, message: Update):
        pass
    
    @abstractmethod
    def can_access(self, user) -> bool:
        pass