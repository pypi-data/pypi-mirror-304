# circomlibpy
Circom libs in Python

## Obtaining a Poseidon hash from two elements:

```python
from circomlibpy.poseidon import PoseidonHash

poseidon = PoseidonHash()
hash = poseidon.hash(2, [12345, 67890])
```

## Constructing a Merkle tree based on Poseidon hashes:

```python
from circomlibpy.merkle_tree import MerkleTree

leafs: list[int] = [
    [1, 2, 3],
    [11, 22, 33],
]
mtree = MerkleTree(leafs)
path, order = mtree.gen_proof(index=0)

print(f'Root: {mtree.root}')
print(f'Path: {path}')
print(f'Order: {order}')
```