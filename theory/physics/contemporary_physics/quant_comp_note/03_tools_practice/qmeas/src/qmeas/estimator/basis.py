from qiskit.quantum_info import PauliList


class QubitwiseBasis:
    """逐比特对易测量基：从直方图恢复组内每个 Pauli 期望。

    测量基信息已在 rotation gate 中编码，本类只负责对 Z-basis 计数做
    奇偶校验，还原对应的 Pauli 期望值。

    后续可扩展为 PairBasis / GeneralBasis，对应纠缠对易组的恢复逻辑。
    """

    def recover(self, group, counts, shots):
        masks = self._build_masks(group)

        sums = {pauli: 0 for pauli in group}
        for bitstring, count in counts.items():
            outcome = int(bitstring, 2)
            for pauli in group:
                parity = (masks[pauli] & outcome).bit_count() & 1
                sums[pauli] += count * (-1 if parity else 1)

        return {pauli: s / shots for pauli, s in sums.items()}

    @staticmethod
    def _build_masks(pauli_list):
        masks = {}
        for pauli in pauli_list:
            support = pauli.x | pauli.z
            mask = 0
            for i, bit in enumerate(support):
                if bit:
                    mask |= 1 << i
            masks[pauli] = mask
        return masks
