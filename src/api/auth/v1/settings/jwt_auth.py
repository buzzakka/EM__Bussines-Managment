from pathlib import Path

AUTH_PATH: Path = Path(__file__).parent


class JWTAuthSettings:
    private_key_path: Path = AUTH_PATH / 'certs' / 'private.pem'
    public_key_path: Path = AUTH_PATH / 'certs' / 'public.pem'
    algorithm: str = 'RS256'

