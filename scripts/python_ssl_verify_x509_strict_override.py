import os
import ssl

if os.environ.get("SSL_VERIFY_X509_STRICT", "true").lower() == "false":
    original = ssl.create_default_context

    def patched(*args, **kwargs):
        ctx = original(*args, **kwargs)
        ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
        return ctx

    ssl.create_default_context = patched
    ssl._create_default_https_context = patched
