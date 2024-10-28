from circomlibpy.poseidon import PoseidonHash


class MerkleTree:
    height: int = 8
    hashes: list[int]

    def __init__(self, leafs: list[list[int]], height: int = 8):
        self.height = height or self.height

        self.size = 2 ** height
        self.log = 1 + height

        # TODO: check len(leafs) > height

        poseidon = PoseidonHash()
        leaf_len = len(leafs[0])
        # TODO: check every leafs len

        self.hashes = [0] * (self.size * 2 - 1)
        for i in range(self.size * 2 - 2, -1, -1):
            if i > self.size - 2:
                if i - self.size + 1 < len(leafs):
                    self.hashes[i] = poseidon.hash(leaf_len, leafs[i - self.size + 1])
                else:
                    self.hashes[i] = 0
            else:
                self.hashes[i] = poseidon.hash(2, [self.hashes[i * 2 + 1], self.hashes[i * 2 + 2]])

    @property
    def root(self) -> int:
        return self.hashes[0]

    def gen_proof(self, leaf_pos: int) -> tuple[list[int], list[int]]:
        path = [0] * (self.log - 1)
        order = [0] * (self.log - 1)

        index = leaf_pos + self.size - 1
        i = 0
        while index:
            path[i] = self.hashes[index + 1 if index % 2 else index - 1]
            order[i] = 1 - index % 2
            index = (index - 1) // 2
            i += 1

        return path, order
