"""Phone Value Object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    """
    Phone Value Object.

    Immutable value object that ensures phone validity.
    Supports Brazilian phone format.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate phone format on initialization."""
        cleaned = self._clean_phone(self.value)
        if not self._is_valid_phone(cleaned):
            raise ValueError(f"Invalid phone number: {self.value}")

        # Store the cleaned version
        object.__setattr__(self, 'value', cleaned)

    @staticmethod
    def _clean_phone(phone: str) -> str:
        """Remove non-numeric characters from phone."""
        # Optimization: Use filter + isdigit instead of regex for better performance
        return ''.join(filter(str.isdigit, phone))

    @staticmethod
    def _is_valid_phone(phone: str) -> bool:
        """
        Validate Brazilian phone number.

        Valid formats:
        - Landline: (XX) XXXX-XXXX (10 digits)
        - Mobile: (XX) 9XXXX-XXXX (11 digits)
        """
        # Check if phone has 10 or 11 digits
        if len(phone) not in [10, 11]:
            return False

        # If 11 digits, third digit must be 9 (mobile)
        if len(phone) == 11 and phone[2] != '9':
            return False

        return True

    def formatted(self) -> str:
        """Return formatted phone number."""
        if len(self.value) == 10:
            # Landline: (XX) XXXX-XXXX
            return f"({self.value[:2]}) {self.value[2:6]}-{self.value[6:]}"
        else:
            # Mobile: (XX) 9XXXX-XXXX
            return f"({self.value[:2]}) {self.value[2:7]}-{self.value[7:]}"

    def __str__(self) -> str:
        return self.formatted()

    def __repr__(self) -> str:
        return f"Phone('{self.formatted()}')"
