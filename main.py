from pathlib import Path
import re

path = Path("data/raw/transcript.txt")
text = path.read_text(encoding="utf-8").strip()

words = text.split()
chunks = []

i = 0
while i < len(words):
    chunk_words = words[i:i+512]
    chunk_text = ' '.join(chunk_words)

    chunks.append({
            'content': chunk_text,
            'order': len(chunks),
            'word_count': len(chunk_words),
            'start_word': i,
            'end_word': i + len(chunk_words) - 1
        })
    
    i += 512 - 10

chunks[-1]['is_last'] = True
print(f"Created {len(chunks)} chunks from {len(words)} total words")
first_chunk = chunks[0]['content']
print(f"First chunk preview: {first_chunk[:100]}...")