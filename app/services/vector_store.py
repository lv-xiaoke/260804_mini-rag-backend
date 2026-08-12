import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension 必须大于 0")

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts: list[str] = []

    @property
    def count(self) -> int:
        return self.index.ntotal

    def add(
        self,
        texts: list[str],
        vectors: list[list[float]],
    ) -> None:
        if not texts:
            raise ValueError("texts 不能为空")
        if len(texts) != len(vectors):
            raise ValueError("texts 和 vectors 的数量必须一致")

        matrix = np.asarray(vectors, dtype=np.float32)

        if matrix.ndim != 2:
            raise ValueError("vectors 必须是二维数组")
        if matrix.shape[1] != self.dimension:
            raise ValueError(
                f"向量维度应为 {self.dimension}，实际为 {matrix.shape[1]}"
            )

        matrix = np.ascontiguousarray(matrix) # FAISS 需要连续存放的内存数据
        faiss.normalize_L2(matrix)

        self.index.add(matrix)
        self.texts.extend(texts)  # extend 方法用于将新文本添加到现有列表中，保证不会形成嵌套列表