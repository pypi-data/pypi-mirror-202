# TTS Arranger

A set of classes that simplify arranging text fragments with multiple speakers and processing it using coqui.ai TTS.

# Examples

```python
#!/usr/bin/python3
from tts_arranger import (TTS_Chapter, TTS_Item, TTS_Project,
                          TTS_Simple_Writer, TTS_Writer)

# Simple example using Simple Writer (using a simple list of TTS items)

tts_items = []

tts_items.append(TTS_Item('This is a test', 'p330'))
tts_items.append(TTS_Item('This is a test with another speaker and a fixed minimum length', 'ED\n', length=10000))
tts_items.append(TTS_Item(length=2000))  # Insert pause

simple_writer = TTS_Simple_Writer(tts_items)
simple_writer.synthesize_and_write('/tmp/tts_arranger_example_output/test2.mp3')

# English example using tts_models/en/vctk/vits (with multispeaker support)

items1 = []
items1.append(TTS_Item('This is a test:', speaker_idx=0))
items1.append(TTS_Item('This is another test:',  speaker_idx=1))

items2 = []
items2.append(TTS_Item('Another test',  speaker_idx=0))
items2.append(TTS_Item('This is getting boring!',  speaker_idx=1))

chapter = []
chapter.append(TTS_Chapter(items1, 'Chapter 1'))
chapter.append(TTS_Chapter(items2, 'Chapter 2'))

project = TTS_Project(chapter, 'Projektname', 'Dies ist ein Untertitel', author='Ein Autor', lang_code='de')

writer = TTS_Writer(project, '/tmp/tts_arranger_example_output/')
writer.synthesize_and_write(project.author + ' - ' + project.title)
```