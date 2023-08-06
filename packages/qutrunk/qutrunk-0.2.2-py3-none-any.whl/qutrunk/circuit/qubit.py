from .bit import Bit


class QuBit(Bit):
    """A quantum bit.

    Args:
        qreg(Qureg): A quantum register containing the bit.
        index (int): The index of the bit in its containing register.

    Raises:
        TypeError: If the provided register is not a Qureg object.
    """

    def __init__(self, qreg=None, index=None):
        """Creates a quantum bit."""
        from .qureg import Qureg

        if not isinstance(qreg, Qureg):
            raise TypeError(
                f"QuBit needs a Qureg and {type(qreg).__name__} was provided."
            )

        super().__init__(qreg, index)
        if qreg is not None:
            self.circuit = qreg.circuit
