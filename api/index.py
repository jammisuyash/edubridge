# api/index.py
# ─────────────────────────────────────────────────────────────
# Vercel Serverless Entry Point
#
# Vercel looks for a file at api/index.py and expects it to
# expose a WSGI-compatible app called `app`.
#
# We just import our Flask app from the root app.py.
# Vercel handles all routing, HTTPS, and scaling automatically.
# ─────────────────────────────────────────────────────────────

import sys
import os

# Make sure the project root is on the Python path
# so "from modules.xxx import yyy" works correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: F401  — Vercel uses this `app` object
