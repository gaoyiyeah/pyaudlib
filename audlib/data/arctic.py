"""Datasets derived from the CMU ARCTIC datbase.

According to the authors, The CMU_ARCTIC databases were constructed at the
Language Technologies Institute at Carnegie Mellon University as phonetically
balanced, US English single speaker databases designed for unit selection
speech synthesis research.

See http://festvox.org/cmu_arctic/index.html for more information.
"""

from .dataset import AudioDataset
from .datatype import AudioPitch
from ..io.audio import audioread


class ARCTIC1(AudioDataset):
    """Generic dataset framework CMU_ARCTIC.

    The database on disk should have the following structure:
    path/to/ARCTIC
    ├── cmu_us_bdl_arctic  <-- speaker bdl
    │   ├── COPYING
    │   ├── etc
    │   ├── orig  <-- wav directory with audio in chan1 and egg in chan2
    │   └── README
    └── cmu_us_slt_arctic  <-- speaker slt
        ├── COPYING
        ├── etc
        ├── orig
        └── README
    """
    def __init__(self, root, sr=None, egg=False, filt=None, transform=None):
        """Instantiate an ARCTIC dataset.

        Parameters
        ----------
        root: str
            The root directory of WSJ0.
        sr: int
            Sampling rate. ARCTIC is recorded at 32kHz.
        egg: bool
            Include the EGG signal at channel 2.
        transform: callable(AudioPitch) -> AudioPitch
            User-defined transformation function.

        Returns
        -------
        An instance `arctic` that has the following properties:
            - len(arctic) == number of usable audio samples
            - arctic[idx] == an AudioPitch instance

        See Also
        --------
        dataset.AudioDataset, datatype.AudioPitch

        """
        def _audioread(path):
            """Read audio as specified by user."""
            sig, ssr = audioread(path, sr=sr)
            if egg:
                out = AudioPitch(sig[0], ssr, egg=sig[1])
            else:
                out = AudioPitch(sig[0], ssr)

            return out
        super(ARCTIC1, self).__init__(root, filt=filt, read=_audioread,
                                      transform=transform)
        self.sr = sr

    def __repr__(self):
        """Representation of ARCTIC."""
        return r"""{}({}, sr={}, egg={}, transform={})
        """.format(self.__class__.__name__, self.root, self.sr, self.egg,
                   self.filt, self.transform)
