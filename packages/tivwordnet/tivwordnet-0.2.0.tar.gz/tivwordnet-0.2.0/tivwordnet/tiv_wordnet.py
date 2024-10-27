from tivwordnet_connector import TivWordnetConnector
from word import Word
from synset import Synset
from collections import defaultdict


class TivWordnet:
    """
    Klass we gba TivWordnet ken iyol ken database.
    """

    def __init__(self, dbcon):
        self.dbcon = dbcon
        self._load_info()

    def _load_info(self):
        synsets_db = self.dbcon.get_synsets()
        hypernyms_db = self.dbcon.get_hypernyms()
        self._synsets_by_sid, self._synsetids_by_lemma = self._process_synsets(synsets_db)
        self._hypersids_by_sid, self._hyposids_by_sid = self._process_hypernyms(hypernyms_db)

    def _process_synsets(self, synsets_db):
        synsets = {}
        synsetids_by_lemma = {}
        for sid, lemma, definition in synsets_db:
            synsetids_by_lemma.setdefault(lemma, set()).add(sid)
            synsets[sid] = (lemma, definition)
        return synsets, synsetids_by_lemma

    def _process_hypernyms(self, hypernyms_db):
        hyperonyms = {}
        hyponyms = {}
        for sid, hypersid in hypernyms_db:
            hyperonyms.setdefault(sid, set()).add(hypersid)
            hyponyms.setdefault(hypersid, set()).add(sid)
        return hyperonyms, hyponyms

    def _get_common(self, syn1, syn2, max_level, nym_fun):
        nyms1 = nym_fun(syn1._id, 0, max_level)
        nyms2 = nym_fun(syn2._id, 0, max_level)
        nymdct1 = {synset: level for level, synset in nyms1}
        nymdct2 = {synset: level for level, synset in nyms2}
        common_nyms = nymdct1.keys() & nymdct2.keys()
        common_nyms_ = [(self._synsets_by_sid[ch], nymdct1[ch],
                         nymdct2[ch]) for ch in common_nyms]
        return common_nyms_

    def _get_nyms_rec(self, synset, cur_level, to_level, nym_fun):
        hyps = {(cur_level, synset)}
        if cur_level < to_level:
            for hypsynset in nym_fun(synset):
                hyps.update(self._get_nyms_rec(hypsynset, cur_level + 1,
                                               to_level, nym_fun))
        return hyps

    def _get_hypersids(self, sid):
        return self._hypersids_by_sid.get(sid, set())

    def _get_hypernyms_rec(self, synset, cur_level, to_level):
        return self._get_nyms_rec(synset, cur_level, to_level,
                                  lambda x: self._get_hypersids(x))

    def _get_hyposids(self, sid):
        return self._hyposids_by_sid.get(sid, set())

    def _get_hyponyms_rec(self, synset, cur_level, to_level):
        return self._get_nyms_rec(synset, cur_level, to_level,
                                  lambda x: self._get_hyposids(x))

    def get_synsets(self, lemma):
        """A ve kpishi synsets a ya shima i ya ken a lemma we a mnyer.

        Args:
            lemma: string, or mnyer we i Tiv.

        Returns:
            Nyumun a synsets we a ya ken mnyer we.
        """
        sids = self._synsetids_by_lemma.get(lemma, set())
        return [self._synsets_by_sid[s] for s in sids]

    def get_hypernyms(self, synset):
        """A ve kpishi hypernyms ken logo i ken synset.
           A hypernym we a tiv er i ken logo i ken.
           Mkom, ga logo i mba a dog -> mammal ->
                               vertebrate -> animal,
           mkom we "mammal" a hypernym we tiv i ken logo i "dog".

        Args:
            synset: objekt Synset we a tsô hypernyms u hiran sha.

        Returns:
            Tor u Synset objekt.
        """
        sid = synset._id
        return {self._synsets_by_sid[s] for s in self._get_hypersids(sid)}

    def get_hyponyms(self, synset):
        """A ve kpishi hyponyms ken logo i ken synset.
           A hyponym we a tiv er i ken logo i ken.
           Mkom, ga logo i mba a dog -> mammal ->
                               vertebrate -> animal,
           mkom we "vertebrate" a hyponym we tiv i ken logo i "animal".

        Args:
            synset: objekt Synset we a tsô hyponyms u hiran sha.

        Returns:
            Tor u Synset objekt.
        """
        sid = synset._id
        return {self._synsets_by_sid[s] for s in self._get_hyposids(sid)}

    def get_common_hypernyms(self, syn1, syn2, max_level=10):
        """A ve kpishi hypernyms u logo i ken synsets syn1 ka syn2
           we tiv ka cur_min_level.

        Args:
            syn1: objekt Synset we a tsô hypernyms u hiran sha.
            syn2: objekt Synset we a tsô hypernyms u hiran sha.
            max_level: int, default=10, level we tiv
                ken a tsô hypernyms.

        Returns:
            A wua tor (level1, level2, hyper_synset), we a level1 ka level2 -- int.
        """
        return self._get_common(syn1, syn2, max_level, self._get_hypernyms_rec)

    def get_common_hyponyms(self, syn1, syn2, max_level=10):
        """A ve kpishi hyponyms u logo i ken synsets syn1 ka syn2
           we tiv ka cur_min_level.

        Args:
            syn1: objekt Synset we a tsô hyponyms u hiran sha.
            syn2: objekt Synset we a tsô hyponyms u hiran sha.
            max_level: int, default=10, level we tiv
                ken a tsô hyponyms.

        Returns:
            A wua tor (level1, level2, hypo_synset), we a level1 ka level2 -- int.
        """
        return self._get_common(syn1, syn2, max_level, self._get_hyponyms_rec)

    def _get_lowest_common_nyms(self, synset1, synset2, nym_fun, max_level=10):
        common_nyms = nym_fun(synset1, synset2, max_level=max_level)
        if common_nyms:
            min_level = min([a + b for cn, a, b in common_nyms])
            return [cn for cn in common_nyms if cn[1] + cn[2] == min_level]
        return []

    def get_lowest_common_hypernyms(self, synset1, synset2, max_level=10):
        """A ve kpishi hypernym u logo u ken synsets syn1 ka syn2
           we tiv ka cur_min_level.

        Args:
            syn1: objekt Synset we a tsô hypernym u hiran sha.
            syn2: objekt Synset we a tsô hypernym u hiran sha.
            max_level: int, default=10, level we tiv
                ken a tsô hypernym.

        Returns:
            A tor i logo we wegh ken hypernym.
        """
        return self._get_lowest_common_nyms(synset1, synset2,
                                            self.get_common_hypernyms,
                                            max_level)

    def get_lowest_common_hyponyms(self, synset1, synset2, max_level=10):
        """Mshin u kyume tsoton sha shom synset syn1 ken syn2
        sha awambe i oryev max_level.

        Args:
            syn1: ihura Synset, mshin u kyume tsoton sha shom.
            syn2: ihura Synset, mshin u kyume tsoton sha shom.
            max_level: int, default=10, awambe i oryev sha
                kyume tsoton.

        Returns:
            List ken tuple nge (level1, level2, hypo_synset), kwagh
                level1 ken level2 -- int, awambe kyume tsoton sha
                    syn1 ken syn2 sha,
                hypo_synset -- ihura Synset, kyume tsoton sha
                    synset syn1 ken syn2 sha.
        """
        return self._get_lowest_common_nyms(synset1, synset2,
                                            self.get_common_hyponyms,
                                            max_level)

    def populate_data(self, word_data, hypernym_data):
        """Mshin i gbenda orusu sha database."""
        # Gbenda synset ken hypernym
        print("Ior synsets ken hypernyms...")
        self.dbcon.insert_synsets(word_data)
        self.dbcon.insert_hypernyms(hypernym_data)

        # Hundu orusu a la a gbenda shaa
        print("Hundu orusu a la a gbenda shaa...")
        self.dbcon.display_all_data()
