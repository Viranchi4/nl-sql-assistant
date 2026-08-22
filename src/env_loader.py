from pathlib import Path
from dotenv import load_dotenv

def load_env(path: str = ".env"):
    """
    Load environment variables from a .env file in the repo root.
    Safe: does nothing if the file does not exist.
    """
    p = Path(path)
    if p.exists():
        load_dotenv(dotenv_path=p)
