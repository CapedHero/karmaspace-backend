from datetime import datetime, timezone

from .models import PassphraseRecord


def verify_email_ownership_with_passphrase(email: str, passphrase: str) -> bool:
    try:
        passphrase_record = PassphraseRecord.objects.get(email=email, passphrase=passphrase)
    except PassphraseRecord.DoesNotExist:
        return False

    is_passphrase_expired = datetime.now(timezone.utc) > passphrase_record.expires_at
    if is_passphrase_expired:
        passphrase_record.delete()
        return False

    return True
