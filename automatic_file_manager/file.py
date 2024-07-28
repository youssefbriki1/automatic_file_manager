import base64
import json
import os
from time import ctime

class File:
    def __init__(self, name, extension, path):
        self.path = path
        self.name = name
        self.extension = extension
        self.full_path = self.path + str(self)
        self.encoding_64 = self.encode_pdf_to_base64()
        self.cdate = os.path.getctime(self.full_path)
        self.mdate = os.path.getmtime(self.full_path)
        self.write_into_json()

        
    def encode_pdf_to_base64(self):
        # Read the PDF file in binary mode
        with open(self.full_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        # Encode the PDF data to base64
        base64_encoded_data = base64.b64encode(pdf_data)
        
        # Convert bytes to string
        base64_encoded_str = base64_encoded_data.decode('utf-8')
        
        return base64_encoded_str


    def __str__(self) -> str:
        return self.name + "." + self.extension
        
    def __repr__(self) -> str:
        return str(self)
    
    def __lt__(self, other) -> bool:
        return self.name < other.name

    def __eq__(self, other) -> bool:
        return self.name == other.name
    
    def __contains__(self, other) -> bool:
        return str(other) in self.name
    
    def is_file_existing(self):
        return os.access(self.full_path, os.F_OK)

    def is_file_readable(self):
        return os.access(self.full_path, os.R_OK)

    
    def write_into_json(self, file="files.json"): # Should Add metadata 
        """
        Storing the file information into a json file

        Args:
            file (str, optional): _description_. Defaults to "files.json".
        """
        dico = {}
        dico[self.name] = {"full name": str(self),
                           "extension":self.extension,
                           "path":self.path,
                           "full path" : self.full_path,
                           "encoding_64":self.encoding_64,
                           "creation date":ctime(self.cdate),
                           "modification date":ctime(self.mdate)
                           }
        with open(file, "w") as f:
            json.dump(dico, f)
    
                
