

# Python 3 code to rename multiple 
# files in a directory or folder
 
# importing os module
import os
 
# Function to rename multiple files
def main():

    folder = "H:/FMF/MAGISTERIJ/Modelska2/Zakljucna/video/"
    filename = "premik1_"
   
    #folder = "xyz"
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"premik1_{1000+int(count)}.jpg"
        src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        dst =f"{folder}/{dst}"
         
        # rename() function will
        # rename all the files
        os.rename(src, dst)
 
# Driver Code
if __name__ == '__main__':
     
    # Calling main() function
    main()