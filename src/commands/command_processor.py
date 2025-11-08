from abc import ABC, abstractmethod
from telegram import Update

class CommandProcessor(ABC):

    @abstractmethod
    def supports(self, command: str, context) -> bool:
        pass 
    
    @abstractmethod
    async def process(self, message: Update, context):
        pass
    
    @abstractmethod
    def can_access(self, user) -> bool:
        pass