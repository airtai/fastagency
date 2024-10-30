import sys

import mesop as me
import pytest

from fastagency.logging import get_logger
from fastagency.ui.mesop.firebase_auth import FirebaseAuth, FirebaseConfig
from fastagency.ui.mesop.main import DEFAULT_SECURITY_POLICY, MesopHomePage

logger = get_logger(__name__)


if sys.version_info >= (3, 10):
    from fastagency.ui.mesop import MesopUI

    class TestMesopHomePage:
        @pytest.fixture
        def firebase_auth(self):
            config = FirebaseConfig(
                api_key="test-key",
                auth_domain="test.firebaseapp.com",
                project_id="test-project",
                storage_bucket="test-bucket",
                messaging_sender_id="test-sender",
                app_id="test-app",
            )
            return FirebaseAuth(sign_in_methods={"google"}, config=config)

        @pytest.fixture
        def mesop_ui(self):
            return MesopUI()

        @pytest.fixture
        def base_policy(self):
            return me.SecurityPolicy(
                dangerously_disable_trusted_types=False,
                allowed_connect_srcs=["custom.domain.com"],
                allowed_script_srcs=["custom.script.com"],
            )

        class TestWithoutAuth:
            """Testing without auth provider, and with and without base security policy."""

            def test_with_security_policy(self, mesop_ui, base_policy):
                """Test scenario: No auth provider, base security policy provided.

                Expected: Should use the base security policy as-is.
                """
                homepage = MesopHomePage(
                    ui=mesop_ui,
                    security_policy=base_policy,
                )

                assert homepage._security_policy == base_policy
                assert homepage._security_policy.allowed_connect_srcs == [
                    "custom.domain.com"
                ]
                assert homepage._security_policy.allowed_script_srcs == [
                    "custom.script.com"
                ]

            def test_without_security_policy(self, mesop_ui):
                """Test scenario: No auth provider, no security policy provided.

                Expected: Should use the default security policy.
                """
                homepage = MesopHomePage(ui=mesop_ui)

                assert homepage._security_policy == DEFAULT_SECURITY_POLICY

        class TestWithAuth:
            """Testing with auth provider, and with and without base security policy."""

            def test_with_security_policy(self, mesop_ui, firebase_auth, base_policy):
                """Test scenario: Auth provider present, custom security policy provided.

                Expected: Should merge custom policy with Firebase requirements.
                """
                homepage = MesopHomePage(
                    ui=mesop_ui, security_policy=base_policy, auth=firebase_auth
                )

                assert set(homepage._security_policy.allowed_connect_srcs) == {
                    "*.googleapis.com",
                    "custom.domain.com",
                }
                assert set(homepage._security_policy.allowed_script_srcs) == {
                    "*.google.com",
                    "https://www.gstatic.com",
                    "https://cdn.jsdelivr.net",
                    "custom.script.com",
                }

            def test_without_security_policy(self, mesop_ui, firebase_auth):
                """Test scenario: Auth provider present, no security policy provided.

                Expected: Should use default policy merged with Firebase requirements.
                """
                homepage = MesopHomePage(ui=mesop_ui, auth=firebase_auth)

                assert set(homepage._security_policy.allowed_connect_srcs) == {
                    "*.googleapis.com"
                }
                assert set(homepage._security_policy.allowed_script_srcs) == {
                    "*.google.com",
                    "https://www.gstatic.com",
                    "https://cdn.jsdelivr.net",
                }
