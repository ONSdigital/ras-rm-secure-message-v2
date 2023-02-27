#!flask/bin/python
import os

from application import create_app

DEV_PORT = os.getenv("DEV_PORT", 5050)
app = create_app("Config")
app.run(debug=True, host="0.0.0.0", port=int(DEV_PORT))
