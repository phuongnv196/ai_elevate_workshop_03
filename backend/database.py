# ========== IMPORTS ==========
from tinydb import TinyDB, Query
from config.config import Config
import logging

# ========== LOGGER SETUP ==========
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Quản lý database tập trung"""
    
    def __init__(self, config=None):
        """Khởi tạo database manager"""
        if config is None:
            config = Config
        
        self.conversations_db = TinyDB(config.CONVERSATIONS_DB)
        self.messages_db = TinyDB(config.MESSAGES_DB)
        self.data_files_db = TinyDB(config.DATA_FILES_DB)
        
        logger.info(f"📊 Initialized databases:")
        logger.info(f"   - Conversations: {config.CONVERSATIONS_DB}")
        logger.info(f"   - Messages: {config.MESSAGES_DB}")
        logger.info(f"   - Data Files: {config.DATA_FILES_DB}")
    
    def get_conversations_db(self):
        """Lấy conversations database"""
        return self.conversations_db
    
    def get_messages_db(self):
        """Lấy messages database"""
        return self.messages_db
    
    def get_data_files_db(self):
        """Lấy data files database"""
        return self.data_files_db
    
    def close_all(self):
        """Đóng tất cả database connections"""
        self.conversations_db.close()
        self.messages_db.close()
        self.data_files_db.close()
        logger.info("📊 Closed all database connections")

# Global database manager instance
db_manager = DatabaseManager()
