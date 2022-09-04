import os

import dotenv

print(dir(dotenv))

dotenv.load_dotenv()

print(os.getenv("UID"))
