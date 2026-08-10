"""Pure zip-packaging helpers for the admin bot (no Telegram deps → testable)."""
import zipfile


def has_2fa(twofa) -> bool:
    """True only when a real (non-empty) cloud password was recorded."""
    return bool((twofa or "").strip())


def build_export_zip(zip_path: str, session_path: str, session_arcname: str, twofa) -> str:
    """Write ``@username.zip`` containing the .session and, ONLY when the
    account actually has a 2FA password, a ``2fa.txt`` holding that password.

    Accounts with no 2FA get NO ``2fa.txt`` at all.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(session_path, arcname=session_arcname)
        if has_2fa(twofa):
            zf.writestr("2fa.txt", twofa)
    return zip_path
