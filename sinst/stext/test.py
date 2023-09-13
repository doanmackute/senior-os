import markdown
import pdfkit

long = '''
## Project Features

* Bare-bones: Only supports basic [CommonMark](https://commonmark.org/)
* "One-size-fits-all" style: Left-aligned, PDF-base14 fonts. Reasonably pretty, but if you want more control, see alternatives below.
* Headings are transformed to PDF bookmarks.
* File links are transformed into attachments with PDF links.
* Images links are transformed into embedded images with optional captions and width specifier.
* Minimal requirements
    - [commonmark](https://pypi.org/project/commonmark/)
    - [PyMuMDF](https://pypi.org/project/PyMuPDF/)
    - [click](https://pypi.org/project/click/)
'''


#markdown to html, to je easy
markdown_long = markdown.markdown(long)
pdfkit.from_string(markdown_long,'GfG.pdf')


