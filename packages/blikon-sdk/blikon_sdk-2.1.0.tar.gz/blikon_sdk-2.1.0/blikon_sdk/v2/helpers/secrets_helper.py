from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError, ResourceNotFoundError


def _get_client() -> SecretClient:
    try:
        # The Key Vault URL
        key_vault_name = "blikon-key-storage"
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
        # 'DefaultAzureCredential' will handle authentication automatically
        credential = DefaultAzureCredential()
        # Create client for Azure Key Vault
        return SecretClient(vault_url=key_vault_uri, credential=credential)
    except AzureError as e:
        raise Exception("Failed to create Key Vault client") from e
    except Exception as e:
        raise Exception("Unexpected error creating Key Vault client") from e


def get_secret(key: str):
    """
    Security function that retrieves secret variable from Azure Key Vault.
    For 'localhost' use Azure CLI authentication through terminal: 'az login'.
    :param key: The name of the Azure Key Vault secret.
    :return: The value of the secret variable.
    """
    # Create client for Azure Key Vault
    client: SecretClient = _get_client()
    try:
        # Retrieve the secret from the Key Vault
        retrieved_secret = client.get_secret(key)
        return retrieved_secret.value  # Return the value of the secret
    except ResourceNotFoundError:
        raise ValueError(f"Secret '{key}' not found in Key Vault")
    except Exception as e:
        raise RuntimeError(f"An error occurred while retrieving the secret: {str(e)}")


def validate_usename_and_password(username: str, password: str):
    """
    Function that checks if the username and password are valid.
    :param username: The username.
    :param password: The password.
    :return: True if the username and password are valid, False otherwise.
    """
    # Create client for Azure Key Vault
    client: SecretClient = _get_client()
    try:
        # Retrieve the secret from the Key Vault
        username_value = client.get_secret("SDK-API-USER").value
        password_value = client.get_secret("SDK-API-USER-PASSWORD").value
        if username == username_value and password == password_value:
            return True
        return False
    except ResourceNotFoundError:
        raise ValueError(f"Username and password secrets not found in Key Vault")
    except Exception as e:
        raise RuntimeError("An error occurred while retrieving the username and password secrets")
