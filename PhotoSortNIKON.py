import os
import sys
from PIL import Image
from shutil import move
import rawpy
from io import BytesIO


def getImagesFromTerminalArgs():

    try:
        arg = sys.argv[1]
    except IndexError:
        print("Input filenames or a * for all photos in current folder.")
        return
        
    if sys.argv[1] == "*":
        input_args_images_list = []

        for file in os.listdir("./"):
            file = file.lower()
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".nef"):
                input_args_images_list.append(file)

    print(input_args_images_list)
    list_index = 0

    for image_filename in input_args_images_list:
        input_args_images_list[list_index] = input_args_images_list[list_index].strip(".\\")
        list_index += 1

    return input_args_images_list


def getImageInputMetadata_Date_JPG(input_image):
    image_input_name = input_image
    image_input_info = Image.open(image_input_name)
    
    try:
        return image_input_info._getexif()[36867] #Exif data for when image was taken (date + time)
    except KeyError:
        print(f"Invalid EXIF data for {input_image}")
        return None


def getImageInputMetadata_Date_RAW(input_raw):
    with rawpy.imread(input_raw) as raw:
        thumb = raw.extract_thumb()
        
        if thumb.format == rawpy.ThumbFormat.JPEG:

            with Image.open(BytesIO(thumb.data)) as img:
                exif_data = img._getexif()
                
            if exif_data.get(36867) == None:
                return exif_data.get(306)
            else:
                return exif_data.get(36867)
        
          # DateTimeOriginal tag


def formatDate(input_date):
    input_date_without_time = input_date.split()[0]
    formatted_date = input_date_without_time.replace(":", "_")

    return formatted_date


def createFolder(folder_name):
    os.mkdir(folder_name)
    return folder_name

def checkFileExist(filename):
    file_exists = os.path.exists(f".\\{filename}")
    
    return file_exists

def checkFolderExist(folder_name):
    return os.path.isdir(f".\\{folder_name}")

def copyFileToFolder(filename, folder_name):
    move(f".\\{filename}", f".\\{folder_name}\\{filename}")

def checkIfJPG(input_name):
    if input_name.endswith(".jpg"):
        return True

def processImageFiles(image_arg_list):

    for image_file in image_arg_list:
        if not checkFileExist(image_file):
            print(f"{image_file} does not exist, skipping...")
            continue
        
        if checkIfJPG(image_file):
            image_date = getImageInputMetadata_Date_JPG(image_file)
            if image_date == None:
                continue
        else:
            image_date = getImageInputMetadata_Date_RAW(image_file)

        image_date = formatDate(image_date)
        
        if not checkFolderExist(image_date):
             createFolder(image_date)
             print(f"Folder {image_date} for {image_file} created.")
        
        folder_name = image_date

        if checkFileExist(f"{folder_name}\\{image_file}"):
            print(f"{image_file} exists in {folder_name}, skipping...")
        
        else:
            copyFileToFolder(image_file, folder_name)
            print(f"{image_file} copied to {folder_name}")
      
if __name__ == "__main__":
    processImageFiles(getImagesFromTerminalArgs())