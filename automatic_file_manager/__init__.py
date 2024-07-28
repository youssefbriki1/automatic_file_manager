"""Top-level package for automatic_file_manager."""

__author__ = """Youssef Briki"""
__email__ = "youssef.briki05@gmail.com"
__version__ = "0.0.1"

try:
    from .file import File
except:
    from file import File
import glob
import os
import json
from langchain import Ollama
        


        
class FilesManager:    
    
    def __init__(self, directories:list[str] = [], files:list[str] = []) -> None:
        self.files = []
        self.current_directory = os.getcwd()
        
        # Use multithreading to make faster & parallel processing
        for file in files:
            self.files.append(File(file.split("/")[-1].split(".")[0], file.split("/")[-1].split(".")[1], file))
        for directory in directories:
            files_in_dir = glob.glob(directory + "/*")
            self.files.extend(list(map(lambda x: File(x.split("/")[-1].split(".")[0], x.split("/")[-1].split(".")[1], x), files_in_dir)))
        
    
    def delete_duplicates(self) -> dict:
        files_encoding_list = [file.encoding_64 for file in self.files]
        duplicates = {}
        index = 0
        while files_encoding_list:
            if files_encoding_list[0] in files_encoding_list[1:]:
                os.remove(self.files.pop(index).full_path)
                files_encoding_list.pop(0)
                index += 1
            else:
                files_encoding_list.pop(0)
                index += 1
        print("Duplicates deleted")
        return duplicates
    
    def move_regex(self, settings:dict) -> None:
        """_summary_

        Args:
            settings (dict): _description_
        """
        for folder, regex in settings["Organize files"].items():
            # See if folder exists
            # Get current path
            if not os.path.exists(self.current_directory+"/"+folder):
                os.makedirs(self.current_directory+"/"+folder)
            for file in self.files:
                for exp in regex:
                    if exp in file.name:
                        os.rename(file.full_path, self.current_directory+"/"+folder+"/"+str(file))
        print("Files moved")
        
        
            
    def __set_up_llm(self):
        
        if settings["Organize LLM"][1] == "GPT 3.5":
            pass
            self.llm = ""
        elif settings["Organize LLM"][1] == "llama 2":
            pass
            self.llm = ""
        else:
            pass
            self.llm = ""

        
    def move_llm_title(self,settings:dict):
        ### TO DO / vérifier si installer sinon on installe
        
        self.__set_up_llm()
        
        # Continue prompt
        template = """
        You are a computer assistant and you are asked to help organize files
        through the title of the files. 
        Here are the folders the folders with their respected description {folders} 
        
        Output "None" if you can't tell through the title and you will be asked to read the content of the file
        Else respond with the name of the folder 
        
        
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        

        
        
        ###
        
        # Ask the LLM if it can detect what the content of it could be from the title / if it can't we go through it
        # If the file isn't readable we try to guess + pdf or word file
        from langchain_core.output_parsers import StrOutputParser

        generate_queries = (
            prompt 
            | self.llm(temperature=0)
            | StrOutputParser() 
            | (lambda x: x.split("\n"))
        )
        
        generate_queries.invoke({"folders":settings["Organize LLM"][0]}) # A verifier
        
    def move_llm_content(self,settings:dict) :
        
        """
        Add the settings part
        """
        template = """
        You are a computer assistant and you are asked to help organize files
        through the title of the files. 
        Here are the folders the folders with their respected description {folders} 
        
        Output "None" if you can't tell through the title and you will be asked to read the content of the file
        Else respond with the name of the folder 
        
        
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Check if document is pdf, give max 3 pages as input to it

        
        
        ###
        
        # Ask the LLM if it can detect what the content of it could be from the title / if it can't we go through it
        # If the file isn't readable we try to guess + pdf or word file
        from langchain_core.output_parsers import StrOutputParser

        generate_queries = (
            prompt 
            | self.llm(temperature=0)
            | StrOutputParser() 
            | (lambda x: x.split("\n"))
        )
        
        generate_queries.invoke({"folders":settings["Organize LLM"][0]}) # A verifier

        

        
    
    
    def __move_llm_workflow(self):
        """
        Use langgraph for this part
        
        
        """
        from typing import Annotated

        from typing_extensions import TypedDict

        from langgraph.graph import StateGraph, START, END
        from langgraph.graph.message import add_messages


        class State(TypedDict):
            # Messages have the type "list". The `add_messages` function
            # in the annotation defines how this state key should be updated
            # (in this case, it appends messages to the list, rather than overwriting them)
            messages: Annotated[list, add_messages]


        graph_builder = StateGraph(State)
        
    
                
                        
            
                        
                        
                            
        

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
        prompt = f"Here are the subjects: {subjects}"é
    
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

if __name__ == "__main__":
    import os

    current_directory = os.getcwd()
    print("Current Directory:", current_directory)



# response = ollama.generate(model='gemma:2b', prompt=prompt)
# print(response['response'])
