"""Top-level package for automatic_file_manager."""

__author__ = """Youssef Briki"""
__email__ = "youssef.briki05@gmail.com"
__version__ = "0.0.1"

from .file import File
import glob
import os
import json

class FilesManager:    
    
    def __init__(self, path) -> None:
        self.path = path
        self.files_path = self.get_files_path()
        self.files_list = self.get_files() # in object File
        
    def get_files(self)  -> list[File]:
        """
        Returns a list of File objects

        Returns:
            list: List of File objects
        """
        return sorted(list(map(lambda x: File(x.split("/")[-1].split(".")[0], x.split("/")[-1].split(".")[1], x), self.get_files_path())))
    
    def get_files_path(self, extension:str = "pdf", datatype=list):
        """
        Return the path of all the files with the given extension in the given path
        and returns it as the datatype given.

        Args:
            path (str): the path
            extension (str, optional): extension of files we want. Defaults to "pdf".

        Returns:
            str: set/list of the directories of the files
        """
        return datatype(glob.glob(self.path + f"*.{extension}"))
        
    
    def delete_duplicate(self, file):
        with open(file, 'r') as f:
            f = json.load(f)
            
        # Store all the encodings in a list
        
        
        for file in f:
            if file["encoding_64"] in []:# list with encodings:
                pass
                # Delete or store: depending on the preference of the user         
            
    
    def setup(self, file): # Multithreading to make faster
        map(lambda x: x.write_into_json(file=file), self.files_list)
        
    """
    def move_files_title(self):
        for file in self.files_list:
            for word in file.name.split():
                assert move_file(word, file.path),"Keyword not found"
    
    def move_files_reader(self):
        for file in self.files_list:
            reader = PyPDF2.PdfReader(file.path)
            words = reader.pages[0].extract_text()
            assert move_file(words, file.path),"Keyword not found" # Après on fait try or except ensuite le LLM
            
    def move_file_title(self, file):
        for word in file.name.split():
            assert move_file(word, file.path),"Keyword not found"
    
    def move_files_llm(self):
        prompt = f"Here are the subjects: {subjects}"
    
    """
    def refresh(self):
        self.files_path = self.get_files_path()
        self.files_list = self.get_files()
        
    def sort_files(self, bynameasc=False, bynamedesc=False, bycdateasc=False,
                   bycdatedesc=False, bymdateasc=False, bymdatedesc=False) -> None:
        """
        Sorts the files based on the specified criteria.

        Args:
            bynameasc (bool, optional): Sort by name in ascending order. Defaults to False.
            bynamedesc (bool, optional): Sort by name in descending order. Defaults to False.
            bycdateasc (bool, optional): Sort by creation date in ascending order. Defaults to False.
            bycdatedesc (bool, optional): Sort by creation date in descending order. Defaults to False.
            bymdateasc (bool, optional): Sort by modification date in ascending order. Defaults to False.
            bymdatedesc (bool, optional): Sort by modification date in descending order. Defaults to False.
        """
        if bynameasc or bynamedesc:
            self.__sort_by_name(bynameasc)
        elif bycdateasc or bycdatedesc:
            self.__sort_by_cdate(bycdateasc)
        elif bymdateasc or bymdatedesc:
            self.__sort_by_mdate(bymdateasc)
    
        
            
    def __sort_by_name(self, asc=True):
        """
        Private methode to sort the files by name

        Args:
            asc (bool, optional): To sort by ascending order. Defaults to True.
        """
        self.files_list = sorted(self.files_list, reverse=not asc)
        
    def __sort_by_cdate(self, asc=True):
        """
        Private methode to sort the files by creation date

        Args:
            asc (bool, optional): To sort by ascending order. Defaults to True.
        """
        self.files_list = sorted(self.files_list, key=lambda x: x.cdate, reverse=not asc)
    
    def __sort_by_mdate(self, asc=True):
        """
        Private methode to sort the files by their last modification date

        Args:
            asc (bool, optional): To sort by ascending order. Defaults to True.
        """
        self.files_list = sorted(self.files_list, key=lambda x: x.mdate, reverse=not asc)
        
            
    
    

    
def move_file(words,file, subjects):
    for subject in subjects:
        if subject in words:
            os.rename(file.path, f"/mnt/c/Users/asus/Desktop/UdeM/automne 2023/{subject}/{file.name}.{file.extension}") # To edit
            return True
    return False
    

# prompt = """
# Can you speak french ?
# """



# response = ollama.generate(model='gemma:2b', prompt=prompt)
# print(response['response'])
