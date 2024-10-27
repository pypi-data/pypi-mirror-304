class Word:
    """Or u er u lemma ken mi na aka.

    Lemma mba u mson u or, ken mi mba u asen kwagh 
    mban or a mi or (wan Tiv). Mbadue soron Tiv:
       - "Or": or ken mbala mba u ngu moho.
       - "Or": mbai mba ngu ungbian ma ior, we wa ga yan.
       - "Taver": mda u kpa aka ase, ka or mba ma kwagh u we nan ga wan 
       we ga kpishi ngu nan we inongu.

    Mbande:
        lemma (): mhen u lemma (mson u or).
        definition (): mhen u mi na aka u or (ikyaren or).
    """

    def __init__(self, word):
        self._lemma, self._definition = word

    def lemma(self):
        """Mhen u lemma.

        Args:
            Kpa se

        Returns:
            mson ga - mson u or.
        """
        return self._lemma

    def definition(self):
        """Mhen u mi na aka u or.

        Args:
            Kpa se

        Returns:
            mson ga - mhen mi na ikyaren u or.
        """
        return self._definition

    def __eq__(self, other):
        return (self._lemma == other._lemma and
                self._definition == other._definition)

    def __hash__(self):
        return hash(self._lemma) + hash(self._definition)

    def __str__(self):
        str_ = '{0} {1}'
        return str_.format(self._lemma, self._definition)
