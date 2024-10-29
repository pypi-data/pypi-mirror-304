import pymupdf
from pathlib import Path
from numpy import load
from .ReadFile import ymTools 
from concurrent.futures import ThreadPoolExecutor
from pandas import DataFrame

class parsePDF():
    def __init__(self , byts_path=False):
        pymupdf.TOOLS.mupdf_display_errors(False)

        if not ymTools('PyMuTools_1.0.8'):
            raise
        self.byts_path= Path(byts_path).glob('*')
 
    def getPdfData(self, how='default'):
        results= {}
        for np_file in self.byts_path:
            np_file= load(np_file, allow_pickle=True).item()
            for url, values in np_file.items():
                try:
                    if how == 'line':
                        results[url]= self.GetLines(values)
                    elif how == 'table':
                        results[url]= self.GetTables(values)
                    elif how == 'block':
                        results[url]= self.GetBlocks(values)
                    else:
                        results[url]= self.GetDefault(values)
                except:
                    pass
        return results
    
    def GetLines(self, content):
        with pymupdf.open(stream=content) as doc:
            words = (sorted(page.get_text_words(), key= lambda x: x[3])  for page in doc.pages())
            page_lines=[]
            for page in words:
                page_words={}
                #here got the words which share the same line
                for word in page:
                    curent_botom_postion= int(word[3])
                    if curent_botom_postion+2 in page_words:
                        page_words[curent_botom_postion+2].append(word)
                    elif curent_botom_postion-2 in page_words:
                        page_words[curent_botom_postion-2].append(word)
                    elif curent_botom_postion+1 in page_words:
                        page_words[curent_botom_postion+1].append(word)
                    elif curent_botom_postion-1 in page_words:
                        page_words[curent_botom_postion-1].append(word)
                    elif curent_botom_postion in page_words :   
                        page_words[curent_botom_postion].append(word) 
                    else:
                        page_words[curent_botom_postion]= [word]
                #here after got all words which share same line,each line are dict words
                #so here sort words in the same line by left postion
                page_values= (sorted(line, key= lambda x: x[0]) for line in page_words.values())
                #here got the word text 
                page_lines.append(tuple(' '.join(word[4] for word in line) for line in page_values))
            return page_lines

    def GetBlocks(self, content):
        with pymupdf.open(stream=content) as doc:
            words = [page.get_text_words()  for page in doc.pages()]
            pages_data= {}
            def extract_lines_blocks(page_tuble):
                page_dict = DataFrame(page_tuble[1])
                page_dict[3]= page_dict[3].astype(int) 
                #page_dict= page_dict.sort_values([5,6,3,0])#this is the updated if not right just remove it
                #page_dict= page_dict.sort_values([3,0])
                def noramlize_line(x):
                    unique_lines= page_dict[3].unique()
                    if x+2 in unique_lines:
                        return x+2
                    elif x+1 in unique_lines:
                        return x+1
                    return x
                page_dict[3]= page_dict[3].apply(noramlize_line)
                lines= page_dict.groupby(3)[5].unique().explode().reset_index().drop_duplicates(subset=5)#this lines for block
                lines[6]= lines[5].apply(lambda x: page_dict[4][page_dict[5]==x].tolist())#this lines for block
                page_line= lines.groupby(3)[6].sum().apply(lambda x: ' '.join(x)).tolist()#this for get data for each unique line
                pages_data[page_tuble[0]]= page_line
            with ThreadPoolExecutor() as executor:
                executor.map(extract_lines_blocks, enumerate(words)) 
            if pages_data:   
                return pages_data
            pages_data[0]=[]
            return pages_data

    def Sort_Pages_Lines(dict_data):
        return {pdf:[data[key] for key in sorted(data.keys())] for pdf, data in dict_data.items()}

    def GetDefault(self, content):
        with pymupdf.open(stream=content) as doc:
            return tuple(page.get_text()  for page in doc.pages())
    def GetTables(self, content):
        with pymupdf.open(stream=content) as doc:
            return {idex:tuple(table.to_pandas() for table in page.find_tables()) for idex, page in enumerate(doc.pages())}
        