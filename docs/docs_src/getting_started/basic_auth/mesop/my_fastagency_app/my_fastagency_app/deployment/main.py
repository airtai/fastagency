from fastagency import FastAgency
from fastagency.ui.mesop import MesopUI
from fastagency.ui.mesop.auth.basic_auth import BasicAuth

from ..workflow import wf

auth = BasicAuth(
    # TODO: Replace `allowed_users` with the desired usernames and their
    # bcrypt-hashed passwords. One way to generate bcrypt-hashed passwords
    # is by using online tools such as https://bcrypt.online
    # Default password for all users is `password`
    allowed_users={
        "admin": "$2y$10$ZgcGQlsvMoMRmmW4Y.nUVuVHc.vOJsOA7iXAPXWPFy9DX2S7oeTDa",  # nosemgrep: generic.secrets.security.detected-bcrypt-hash.detected-bcrypt-hash
        "user@example.com": "$2y$10$ZgcGQlsvMoMRmmW4Y.nUVuVHc.vOJsOA7iXAPXWPFy9DX2S7oeTDa",  # nosemgrep: generic.secrets.security.detected-bcrypt-hash.detected-bcrypt-hash
    },
)

ui = MesopUI(auth=auth)


app = FastAgency(
    provider=wf,
    ui=ui,
    title="My FastAgency App",
)

# start the fastagency app with the following command
# gunicorn my_fastagency_app.deployment.main:app
