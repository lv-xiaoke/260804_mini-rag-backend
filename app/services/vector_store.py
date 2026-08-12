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
        
    def search(
            self,
            query_vector: list[float],
            top_k: int = 3,
        ) -> list[tuple[str, float]]:
            if not query_vector:
                raise ValueError("query_vector 不能为空")
            if top_k <= 0:
                raise ValueError("top_k 必须大于 0")
            if self.count == 0:
                return []

            query_matrix = np.asarray(
                [query_vector],
                dtype=np.float32,
            )

            if (
                query_matrix.ndim != 2
                or query_matrix.shape[1] != self.dimension
            ):
                actual_dimension = (
                    query_matrix.shape[1]
                    if query_matrix.ndim == 2
                    else "未知"
                )
                raise ValueError(
                    f"查询向量维度应为 {self.dimension}，"
                    f"实际为 {actual_dimension}"
                )

            query_matrix = np.ascontiguousarray(query_matrix)
            faiss.normalize_L2(query_matrix)

            k = min(top_k, self.count)
            scores, indices = self.index.search(query_matrix, k)

            results: list[tuple[str, float]] = []

            for index, score in zip(indices[0], scores[0]):
                if index < 0:
                    continue

                results.append(
                    (
                        self.texts[int(index)],
                        float(score),
                    )
                )

            return results

