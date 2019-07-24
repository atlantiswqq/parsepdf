# _*_ coding:utf-8 _*_
# Author:Atlantis
# Date:2019-07-25

import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class ParsePDF(object):
    def __init__(self, pdf_folder):
        """
        :param pdf_folder:the path for pdf files,you know.
        """
        self.pdf_folder = pdf_folder

    def get_pdf_names(self) -> list:
        names = os.listdir(self.pdf_folder)
        return names

    def parse(self,path:str):
        fp = open(path,"rb")
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        result = x.get_text()
                        print(result)

    def main(self):
        names = self.get_pdf_names()
        for name in names:
            abs_path = os.path.join(self.pdf_folder,name)
            self.parse(abs_path)


if __name__ == '__main__':
    pd = ParsePDF("./static")
    pd.main()
