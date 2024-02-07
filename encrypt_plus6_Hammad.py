
import os
import zipfile
try: import PyPDF2
except: 
    "pip install pypdf2"
    import PyPDF2
     
import json
import time
import shutil


class EncryptPlus:
    """
    This class encrypts all PDF files in the "Secret_In" folder and saves them to the "Secret_Sent" folder.
    It also compresses the "Secret_Sent" folder into a ZIP file named "PA6_Files.zip". Also set the password to pdfs
    """
    
    def __init__(self):
        """
        Initializes the class attributes.
        """
        
        self.FolderName = "Prog6"
        self.FolderPath = os.path.join(os.getcwd())
        self.secret_in_folder = "Secret_In"
        self.secret_sent_folder = "Secret_Sent"
        self.ProcessingTime = {}
        self.pdf_Password = "enigma"
        self.zipFileName = "PA6_Files.zip"
        self.ExtractFiles()
    
    def Encrypt(self):
        """
        Loop through all files in the directory including files in subdirectories
        Encrypts all PDF files in the "Secret_In" folder and saves them to the "Secret_Sent" folder.
        """
        for root, dirs, files in os.walk(self.secret_in_folder):
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    encrypted_file_name = f"encrypted_{file}"
                    print(f"\n\t\t\tProcessing: {file}")
                    self.ReadFiles(file_path, encrypted_file_name)
                    

    def ReadFiles(self, file_path, fileName):
        """
        Reads a PDF file, encrypts it, and saves it to a new file.
        """
        # Reading Files Inside Secret_in Folder
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writter = PyPDF2.PdfWriter()
            
            # Assigning Password to Pdf File
            writter.encrypt(self.pdf_Password)
            startTime = time.time()
            
            for page_num in range(len(reader.pages)):
                writter.add_page(reader.pages[page_num])

            self.WriteFiles(fileName, writter)
            endTime = time.time()
            processingTime = round(endTime - startTime, 2)
            self.ProcessingTime[fileName] = processingTime
            
            self.WriteCsv()
    
    def WriteFiles(self, fileName, writter):
        """
        Writes an encrypted PDF file to the "Secret_Sent" folder.
        """
        encrypted_pdf_path = os.path.join(self.secret_sent_folder, fileName)
        print(f"\t\t\tWritting Encrypted File {fileName}")
        with open(encrypted_pdf_path, 'wb') as encrypted_pdf_file:
            writter.write(encrypted_pdf_file)
    
    def ShowTimeProcessing(self):
        """
        Prints the encryption processing time for each file.
        """
        for filename, timeduration in self.ProcessingTime.items():
            print(f"\t\t\t  - {filename}  {timeduration}")
        
    def WriteCsv(self):
        """
        Saves the processing time data to a JSON file.
        """
        with open("time_fileHL.json", "w") as file: 
            json.dump(self.ProcessingTime, file)
    
    def CompressFolder(self):
        """
        Compresses the "Secret_Sent" folder into a ZIP file named "PA6_Files.zip".
        """
        output_zip_path = f'{self.FolderPath}/Secret_Sent.zip'
        shutil.make_archive(output_zip_path.split('.')[0], 'zip', os.path.join(os.getcwd(), "Secret_Sent"))
        print("\n\t\t\tSecret_Sent Compressed Successfully...")
    
    # Method To Extract Zip File
    def ExtractFiles(self):
        """
        Extracts the files from the ZIP file named "PA6_Files.zip". Printing the new files appeared after 
        unzipping the "PA6_Files.zip".
        """
    
        oldFiles = os.listdir()                                     # All Files in Dir Before Unzipping
        print(f"\n\t\t\tUnziping File [{self.zipFileName}]")
        zipFilePath = os.path.join(os.getcwd(), self.zipFileName)   # Zip File Path
        with zipfile.ZipFile(zipFilePath, 'r') as file:             # Reading Zip File
            file.extractall()                                       # Extrating All Files in Zip
        
        newFiles = os.listdir()                                     # All Files in Dir After Unzipping
        newFiles = [x for x in newFiles if x not in oldFiles]       # New Files in Dir After Unzipping (not in old)
        
        files = []                                                  
        for root, dirs, filenames in os.walk(os.getcwd()):          # Going Through All Files in Directory
            files.extend([filename for filename in filenames if filename not in oldFiles])  # Getting All New Files in Dir After Unzipping (not in old)
        
        for x in files: print(f"\t\t\t  - Zipped {x}")              # Printing The Files Extracted after Zipped 
        


if __name__ == "__main__":
    
    # Dashboard Header Message
    os.system("cls")
    print(f"\t\t\t{'-'*51}")
    print(f"\t\t\t---\t\t\tAIST 2120\t\t---")
    print(f"\t\t\t---\t\tProgramming Assignment 6\t---")
    print(f"\t\t\t---\t\t   Encryptinator Plus\t\t---")
    print(f"\t\t\t{'-'*51}")
    
    # Creating Object of Class
    encrypt = EncryptPlus()
    # Calling Encrypt Method
    encrypt.Encrypt()
    
    print("\n\t\t\tEncryption File Processing Time:\n")
    encrypt.ShowTimeProcessing()
    encrypt.CompressFolder()
    
    # Dashboard Complete Bottom Message
    print(f"\n\t\t\t{'-'*51}")
    print(f"\t\t\t---\t\tProgramming Assignment 6\t---")
    print(f"\t\t\t---\t\t   Encryptinator Plus\t\t---")
    print(f"\t\t\t---\t\t\tComplete\t\t---")
    print(f"\t\t\t{'-'*51}")
    
    input("\t\t\tPress Enter")

