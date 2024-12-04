## Render Markdown (mistletoe)
import mistletoe

SOURCE = '_source/index.md'
DESTINATION = '_rendered/index.html'

with open(SOURCE, 'r') as fin:
    rendered = mistletoe.markdown(fin)

with open(DESTINATION, 'w') as fout:  # Assumes folder exists
    fout.write(rendered)
