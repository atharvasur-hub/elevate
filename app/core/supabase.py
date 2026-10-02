from typing import Optional
from supabase import Client, create_client
from app.core.config import settings

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """
    Returns an initialized Supabase Client if SUPABASE_URL and SUPABASE_KEY are provided.
    Used for Supabase Auth, Storage buckets, and Realtime events.
    """
    global _supabase_client
    if _supabase_client is None:
        if settings.SUPABASE_URL and settings.SUPABASE_KEY and settings.SUPABASE_KEY != "your-supabase-anon-or-service-role-key-here":
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase_client
