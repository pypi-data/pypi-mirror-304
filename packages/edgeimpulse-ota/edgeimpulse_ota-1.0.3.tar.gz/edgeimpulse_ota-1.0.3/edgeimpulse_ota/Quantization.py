import re
from collections import namedtuple
from struct import pack
from typing import Generator, Iterable


Quant = namedtuple("Quantization", "index, size, scale, zero")


class Quantization:
    """
    Match quantization data in Edge Impulse model.
    Patch format is (for each layer):
        index: 1 byte
        size: 2 bytes
        data: size * 8 bytes
            scale: 4 bytes (float)
            zero point: 4 bytes (int)
    """
    def __init__(self, contents: str):
        def eval_data(data: str, dtype) -> list:
            return [dtype(x) for x in eval("[" + re.sub(r'/\*.+?\*/', "", data) + "]")]

        scales = re.findall(r'TfArray<(\d+), float> quant(\d+)_scale = \{ \d+, \{([\s\S]+?)}', contents)
        zeros = re.findall(r'TfArray<(\d+), int> quant(\d+)_zero = \{ \d+, \{([\s\S]+?)}', contents)
        assert len(scales) > 0, "Can't find quantization data"
        assert len(scales) == len(zeros), "quantization data size mismatch"

        self.quants = [
            Quant(index=int(index1), size=eval(size1), scale=eval_data(s, float), zero=eval_data(z, int))
            if index1 == index2 and size1 == size2 else None
            for (size1, index1, s), (size2, index2, z) in zip(scales, zeros)
        ]

        for quant in self.quants:
            assert quant is not None, "quantization failed to match"
            assert len(quant.scale) == len(quant.zero), f"quantization data size mismatch at index {quant.index}"

    @property
    def bytes_size(self) -> int:
        return len(self.bytes)

    @property
    def iterator(self) -> Iterable:
        return self.quants

    @property
    def bytes(self):
        """
        Convert data to binary format
        :return:
        """
        packs = []

        for quant in self.iterator:
            data = [x for pair in zip(quant.scale, quant.zero) for x in pair]
            packs.append(pack(f">BH{'fi' * len(quant.scale)}", quant.index, quant.size, *data))

        return b"".join(packs)
