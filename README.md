# Textbook to pdf

converts online textbooks from websites like wsipnet.pl or nowaera.pl to pdfs

## Usage

* fill `textbook_urls.json` with textbook names and urls, `{}` in page url indicates page number
* fill `cookies.txt` with cookies that are required in order to download textbook
* check `textbook_to_pdf.py` -> `download_image` function to edit program specification
* run `python textbook_to_pdf.py` in your terminal

Your textbook will be saved in the same folder which you run the program