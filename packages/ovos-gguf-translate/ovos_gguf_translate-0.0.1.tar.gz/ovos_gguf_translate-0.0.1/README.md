# GGUF Translator

LLM powered translation plugin, [TowerInstruct-7B-v0.1](https://huggingface.co/Unbabel/TowerInstruct-7B-v0.1) is trained to handle several translation-related tasks, such as general machine translation (e.g., sentence- and paragraph-level translation, terminology-aware translation, context-aware translation), automatic post edition, named-entity recognition, gramatical error correction, and paraphrase generation. 

> **Languages**: English, Portuguese, Spanish, French, German, Dutch, Italian, Korean, Chinese, Russian


```python
tx = GGUFTranslator()
text = "The easiest way for anyone to contribute is to help with translations! You can help without any programming knowledge via the translation portal"
tx.translate(text, target="es-es")
# La forma más sencilla de contribuir es ayudando con las traducciones! Puedes ayudar sin ningún conocimiento de programación a través del portal de traducción
```