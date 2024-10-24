#LexStruct_PDF

This is an efficient python library build to extract the contents(text,images,tables) from a pdf.

It accepts one argument i.e. path of your pdf.

How to use:-

from LexStruct_PDF import ContentExtractor

obj  = ContentExtractor("pdf to your path")
extracted_text = obj.extract_content()