import fitz 
import re
import base64
import os


class ContentExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def replace_table_with_screenshot_path(self):
        # Open the PDF
        doc = fitz.open(self.pdf_path)
        text=self.pdf_path[20:-4]
        # Step 1: Convert the text to bytes
        text_bytes = text.encode('utf-8')
        
        # Step 2: Encode the bytes to Base64
        base64_bytes = base64.b64encode(text_bytes)
        encoded_string = base64_bytes.decode('utf-8')
        # Iterate through the pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Find tables on the page
            tables = page.find_tables()
            
            if tables:
                for i, table in enumerate(tables):
                    bbox_tuple = table.bbox  # Get the bounding box of the table
                    bbox=fitz.Rect(bbox_tuple)
                    # Capture the screenshot of the table with higher resolution
                    mat = fitz.Matrix(2, 2)  # Increase the zoom factor for higher resolution
                    pix = page.get_pixmap(matrix=mat, clip=bbox)
                    
                    # Save the screenshot to a file
                    screenshot_path = f"{encoded_string}_table_screenshot_{page_num}_{i}.png"
                    pix.save(screenshot_path)
                    
                    # Redact the text within the bounding box
                    page.add_redact_annot(bbox, fill=(1, 1, 1))
                    page.apply_redactions()
                    
                    # Insert the path of the screenshot as an annotation
                    page.insert_text((bbox.x0, bbox.y1 + 2), screenshot_path + " $identifiedTable", fontsize=12, color=(0, 0, 0),overlay=True)

        
        # Save the modified PDF
        doc.save("sample.pdf")

    def replace_tableword_with_url(self,text, url):
        # Define the URL tag
        url_tag = f'<a href="{re.escape(url)}">table</a>'
        url_tag = url_tag.replace('\\.png', '.png')
        
        # Find all occurrences of "table" (case insensitive)
        matches = re.findall(r'\btable\b', text, re.IGNORECASE)
        
        if len(matches) > 1:
            # Define phrases to check
            phrases = ["table below", "table above", "above table", "below table"]
            
            # Replace specific phrases first
            for phrase in phrases:
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                text = pattern.sub(lambda m: m.group().replace("table", url_tag), text)
        else:
            text = re.sub(r'\btable\b', url_tag, text, flags=re.IGNORECASE)
        
        return text
    
    def extract_content(self):
        self.replace_table_with_screenshot_path()
        try:
            # Open the PDF file
            doc = fitz.open("sample.pdf")
            name=self.pdf_path[20:-4]
            # Step 1: Convert the text to bytes
            text_bytes = name.encode('utf-8')
            
            # Step 2: Encode the bytes to Base64
            base64_bytes = base64.b64encode(text_bytes)
            encoded_string = base64_bytes.decode('utf-8')
            text = ""
            # Iterate over all pages in the PDF
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)  # Load the page
                blocks = page.get_text("dict")['blocks']  # Extract text blocks as a dictionary
        
                
                # Iterate through the blocks on the page
                for block_idx, block in enumerate(blocks):
                    if block['type'] == 0:  # Text block (type 0)
                        # Extract the lines in the block
                        for line in block['lines']:
                            line_text = " ".join([span['text'] for span in line['spans']])
                            text = text + "\n\n" + line_text

                    else:
                        # For non-text blocks (tables, images, etc.)
                        # print("Non-text block encountered (likely table or image). Taking screenshot.")
        
                        # Get the rectangle of the non-text block
                        block_rect = fitz.Rect(block['bbox'])
                        if (block_rect[2]-block_rect[0]) > 20.00  and (block_rect[3]-block_rect[1])> 20.00:
                            # Render the page as an image
                            pix = page.get_pixmap(clip=block_rect)  # Capture only the area of the non-text block
                            
                            # Save the image
                            img_path = f"{encoded_string}_screenshot_page_{page_num + 1}_block_{block_idx + 1}.png"
                            pix.save(img_path)
                            text = text + '\n' + "<a href=\"" + img_path + "\">Click Here</a>"
                        else:
                            text = text + ' '
        
            text_2 = text.split(" $identifiedTable")
            pattern = r'[A-Za-z]:\\(?:[A-Za-z0-9_ -]+\\)*[A-z0-9]+_table_screenshot_\d+_\d+\.png$|[A-Za-z]:\/(?:[A-Za-z0-9_ -]+\/)*[A-z0-9]+_table_screenshot_\d+_\d+\.png$'
            prepared_text = ""
            for i in text_2:
                match = re.search(pattern,i)
                captured_length = len(match.group(0)) if match else 0
                if captured_length == 0:
                    prepared_text = prepared_text + "\n\n" + i
                else:
                    tex = i[:-captured_length]
                    prepared_text = prepared_text + "\n\n" + self.replace_tableword_with_url(tex,match.group(0))

            return prepared_text

        except Exception as e:
            print(f"Error during text extraction: {e}")