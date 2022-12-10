from discord import ApplicationCommandError

class NotEnoughVaultCapacity(ApplicationCommandError):
    """Raised when vault capacity is max or not enough"""

class NotEnoughWallet(ApplicationCommandError):
    """Raised when wallet is not enough for transaction"""

class WalletEmpty(ApplicationCommandError):
    """Raised when wallet == 0"""

class NotEnoughVault(ApplicationCommandError):
    """Raised when vault is not enough for transaction"""

class VaultEmpty(ApplicationCommandError):
    """Raised when vautl == 0"""

class InvalidAmount(ApplicationCommandError):
    """Raised when amount is not a valid number/str"""