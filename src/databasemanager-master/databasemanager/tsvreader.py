#==================================================#
# Authors: Amir H. Ansari <amirans65.ai@gmail.com> #
# License: BSD (3-clause)                          #
#==================================================#

class TSVReader():
    _comment_char = '#'
    _tab_char = '\t'
    
    @staticmethod
    def __read_all_lines(path):
        with open(path) as f:
            lines = [line.rstrip('\n').rstrip('\r') for line in f]
        return lines
    
    @staticmethod
    def read_rows(path, remove_empty_rows=True):
        lines = TSVReader.__read_all_lines(path)
        if(remove_empty_rows):
            lines = [l for l in lines if len(l) != 0]            
        comments = [l for l in lines if (len(l)>0 and l[0] == TSVReader._comment_char)]
        lines = [line for line in lines if (len(line) ==0 or line[0] != TSVReader._comment_char)]
        return lines,comments

    @staticmethod
    def read_tsv(path, remove_empty_rows=True, apply_strip=True, max_column=-1):
        if(max_column>-1):
            max_column -= 1 #max_column is str.split returns (max_column+1) columns!!
        lines,comments = TSVReader.read_rows(path, remove_empty_rows)
        lines = [TSVReader._remove_multiple_tab(line) for line in lines]
        tsv_rows = []
        for line in lines:
            line = line.strip()
            if(len(line)==0):
                continue
            ll = line.split(TSVReader._tab_char,max_column)
            if(apply_strip):
                ll = [l.strip() for l in ll]
            tsv_rows.append(ll)
        return tsv_rows,comments
        
    @staticmethod
    def _remove_multiple_tab(lines):
        while(lines.find(TSVReader._tab_char*2)>-1):
            lines = lines.replace(TSVReader._tab_char*2,TSVReader._tab_char)
        return lines
