import uuid

class Helpers:
    """
    A utility class providing helper methods for UUID generation and data conversion.
    """
    
    @staticmethod
    def uuid4() -> str:
        """
        Generate a random UUID (Universally Unique Identifier).

        :return : A string representation of a random UUID (UUID version 4).
        """
        
        return str(uuid.uuid4())
