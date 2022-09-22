"""
Unit test for application start-up.
"""

import logging

from sounder.sounder_app import SoundAnalyser

log = logging.getLogger(__name__)


def test_startup():
    # Run application main class.
    s_app = SoundAnalyser()

    # Check application name and version.
    assert s_app._app_name == "sounder"
    assert s_app._app_version == "0.0.1"
