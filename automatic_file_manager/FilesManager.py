try:
    from .file import File
except:
    from file import File

import platform
import glob
import os
import json
from langchain import Ollama
        


        
class FilesManager:    
    
    def __init__(self, directories:list[str] = [], files:list[str] = []) -> None:
        self.files = []
        self.current_directory = os.getcwd()
        self.seperator = "/" if platform.system() == 'Linux' else f"\\"  # For linux, update for windows too 
        
        # Use multithreading to make faster & parallel processing
        for file in files:
            self.files.append(File(file.split(self.seperator)[-1].split(".")[0], file.split(self.seperator)[-1].split(".")[1], file))
        for directory in directories:
            files_in_dir = glob.glob(directory + self.seperator + "*")
            self.files.extend(list(map(lambda x: File(x.split(self.seperator)[-1].split(".")[0], x.split(self.seperator)[-1].split(".")[1], x), files_in_dir)))
        
    
    def delete_duplicates(self) -> dict:
        """
        Delete duplicates files based on their encoding
        """
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
        """
        Moving files based on the regex provided in the settings

        Args:
            settings (dict): Regex dict
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
        self.llm = Ollama(model="llama3", temperature=0)


    def use_llm(self, settings:dict):
        for file in self.files:
            if folder_name := self.__move_llm_title(file, settings):
                print(f'{file.name} moved to {folder_name} from the title')
            elif folder_name_content := self.__move_llm_content:
                print(f'{file.name} moved to {folder_name} from the content')
            else:
                print(f'Not able move the file {file.name}')

                
        
    def __move_llm_title(self,file:File, settings:dict) -> str:
        ### TO DO / vérifier si installer sinon on installe
        
        self.__set_up_llm()
        
        # Continue prompt
        template = """
        You are a computer assistant and you are asked to help organize files
        through the title of the files. 
        Here are the folders with their respected description {folders} 
        Here is the file's name: {file}
        
        Output "None" if you can't tell through the title and you will be asked to read the content of the file
        Else respond with the name of the folder 
        
        
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        from langchain_core.output_parsers import StrOutputParser

        generate_queries = (
            prompt 
            | self.llm
            | StrOutputParser() 
            | (lambda x: x.split("\n"))
        )
        
        return generate_queries.invoke({"folders":settings["Organize LLM"][0], "files":file.name}) # A verifier
        
    def __move_llm_content(self,file:File, settings:dict) :
        from langchain_community.document_loaders import PyPDFLoader
        template = """
        You are a computer assistant and you are asked to help organize files
        through the title of the files. 
        Here are the folders the folders with their respected description {folders}.
        Here are 3 pages of the file's content: {content}
        
        Output "None" if you can't tell through the title and you will be asked to read the content of the file
        Else respond with the name of the folder 
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        loader = PyPDFLoader("", extract_images=True)
        pages = loader.load()
        content:str = ""
        for i in range(max(3,len(pages))):
            content += pages[i].page_content
        from langchain_core.output_parsers import StrOutputParser

        generate_queries = (
            prompt 
            | self.llm
            | StrOutputParser() 
            | (lambda x: x.split("\n"))
        )
        
        return generate_queries.invoke({"folders":settings["Organize LLM"][0], "content":content}) # A verifier    
    
    def __watchdog():
    
