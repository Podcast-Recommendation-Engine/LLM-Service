
class SemanticChunkingManager:
    def __init__(self, content: str, chunk_size: int, window_overlap: int) -> None:
        self.content = content
        self.chunk_size = chunk_size
        self.window_overlap = window_overlap

    def chunk_content(self):
        word_list = self.content.split()
        i = 0
        data = []

        while i < len(word_list):
            chunk = word_list[i : i + self.chunk_size]
            data.append({
                'order': len(data) + 1,
                'content': ' '.join(chunk),
                'is_last': False
            })
            i += self.chunk_size - self.window_overlap

        if data:
            data[-1]['is_last'] = True
        return data

    @property
    def stats(self):
        total_words = len(self.content.split())
        chunks = self.chunk_content()
        total_chunks = len(chunks)
        avg_chunk_size = round(total_words / total_chunks, 2) if total_chunks else 0

        return {
            "total_words": total_words,
            "total_chunks": total_chunks,
            "avg_chunk_size": avg_chunk_size
        }
