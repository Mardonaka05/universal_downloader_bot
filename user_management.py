# -*- coding: utf-8 -*-
"""
User management - MongoDB-free version
Works perfectly without any database!
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

# ========================================
# SIMPLE IN-MEMORY STORAGE (NO DATABASE)
# ========================================
in_memory_users = {}

# Try to get ADMIN_IDS
ADMIN_IDS = []
try:
    from config import ADMIN_IDS
except ImportError:
    logger.warning("Could not import ADMIN_IDS - using empty list")

logger.info("📝 User management initialized (in-memory mode)")


# ========================================
# USER FUNCTIONS
# ========================================

def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user from storage"""
    return in_memory_users.get(user_id)


def create_user(user_id: int, username: Optional[str] = None, 
                language: Optional[str] = None) -> Dict[str, Any]:
    """Create new user"""
    user_data = {
        "user_id": user_id,
        "username": username,
        "language": language,
        "created_at": datetime.now(),
        "last_active": datetime.now(),
        "downloads_count": 0,
        "is_admin": user_id in ADMIN_IDS,
        "is_banned": False
    }
    
    in_memory_users[user_id] = user_data
    logger.info(f"✅ User created: {user_id} (@{username})")
    return user_data


def update_user(user_id: int, username: Optional[str] = None, 
                language: Optional[str] = None) -> bool:
    """Update user data"""
    if user_id not in in_memory_users:
        create_user(user_id, username, language)
        return True
    
    update_data = {
        "last_active": datetime.now()
    }
    if username:
        update_data["username"] = username
    if language:
        update_data["language"] = language
    
    in_memory_users[user_id].update(update_data)
    return True


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


def is_user_banned(user_id: int) -> bool:
    """Check if user is banned"""
    user = get_user(user_id)
    return user.get("is_banned", False) if user else False


def increment_download_count(user_id: int) -> bool:
    """Increment download count"""
    if user_id in in_memory_users:
        in_memory_users[user_id]["downloads_count"] = \
            in_memory_users[user_id].get("downloads_count", 0) + 1
        return True
    return False


def get_total_users() -> int:
    """Get total users count"""
    return len(in_memory_users)


def get_active_users(days: int = 7) -> int:
    """Get active users in last N days"""
    cutoff = datetime.now() - timedelta(days=days)
    return sum(
        1 for u in in_memory_users.values()
        if u.get("last_active", datetime.min) >= cutoff
    )


def get_users_with_usernames() -> list:
    """Get users with usernames"""
    return [
        {
            "user_id": uid,
            "username": u.get("username"),
            "downloads_count": u.get("downloads_count", 0)
        }
        for uid, u in in_memory_users.items()
        if u.get("username")
    ]


def get_usage_stats() -> Dict[str, int]:
    """Get usage statistics"""
    total = len(in_memory_users)
    downloads = sum(u.get("downloads_count", 0) for u in in_memory_users.values())
    return {
        "total_users": total,
        "total_downloads": downloads
    }


# ========================================
# SUBSCRIPTION CHECKS (FREE VERSION)
# ========================================

async def check_channel_subscription(user_id: int, bot) -> bool:
    """Always returns True (FREE version)"""
    return True


def check_user_subscription(user_id: int, username: Optional[str] = None, 
                           language: Optional[str] = None) -> bool:
    """Always returns True (FREE version)"""
    return True