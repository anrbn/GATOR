from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization
from pathlib import Path

from gator.utils import print_helpers as ph

def generate_ssh_key(username, comment="", new_priv_key=True):
    """
    Generate an SSH key pair.
    """
    try:
        base_dir = Path.home() / ".gator"
        base_dir.mkdir(exist_ok=True)

        priv_key_file = base_dir / "private_key.pem"
        pub_key_file = base_dir / "public_key.pub"

        if new_priv_key or not priv_key_file.exists():
            try:
                key = rsa.generate_private_key(
                    backend=crypto_default_backend(),
                    public_exponent=65537,
                    key_size=2048
                )
            except Exception as e:
                ph.print_error(f"Error generating private key: {e}")
                return None, None, None

            try:
                private_key = key.private_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PrivateFormat.PKCS8,
                    crypto_serialization.NoEncryption()
                ).decode('utf-8')
            except Exception as e:
                ph.print_error(f"Error serializing private key: {e}")
                return None, None, None

            try:
                with priv_key_file.open('w') as file:
                    file.write(private_key)
            except Exception as e:
                ph.print_error(f"Error writing private key to file: {e}")
                return None, None, None
        else:
            try:
                with priv_key_file.open('r') as file:
                    private_key = file.read()
            except Exception as e:
                ph.print_error(f"Error reading private key from file: {e}")
                return None, None, None

            try:
                key = serialization.load_pem_private_key(
                    private_key.encode(),
                    password=None,
                    backend=crypto_default_backend()
                )
            except Exception as e:
                ph.print_error(f"Error loading private key: {e}")
                return None, None, None

        try:
            public_key_data = key.public_key().public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH
            ).decode('utf-8')
        except Exception as e:
            ph.print_error(f"Error generating public key: {e}")
            return None, None, None

        formatted_public_key = f"{public_key_data} {comment}"
        # formatted_public_key = f"{username}:{public_key_data} {comment}"
        save_public_key = f"{public_key_data} {comment}"

        try:
            with pub_key_file.open('w') as file:
                file.write(save_public_key)
        except Exception as e:
            ph.print_error(f"Error writing public key to file: {e}")
            return None, None, None

        return private_key, formatted_public_key, str(priv_key_file)

    except Exception as e:
        ph.print_error(f"An unexpected error occurred: {e}")
        return None, None, None
