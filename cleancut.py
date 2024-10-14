import os, sys, re, shutil
from PIL import Image

def remove_exif(file_pathname: str, out_path: str) -> bool:
    
    print("Removing EXIF from file: " + file_pathname)

    if not os.path.isfile(file_pathname):
        print("File does not exist: " + file_pathname)
        return False
        
    try:
        im = Image.open(file_pathname)

        fields_to_keep = ('transparency', )
        exif_fields = list(im.info.keys())
        for k in exif_fields:
            if k not in fields_to_keep:
                del im.info[k]

        out_pathname = os.path.join(out_path, os.path.basename(file_pathname))
        im.save(out_pathname, exif=None)
        
        im.close()
    except Exception as e:
        print("Error reading image file " + file_pathname)
        return False
        
    return True

def batch_remove_exif(in_folder: str, out_folder: str) -> bool:
    
    if not os.path.isdir(in_folder):
        print("Input folder does not exist: " + in_folder)
        return False
        
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    
    for file in os.listdir(in_folder):
        pathname = os.path.join(in_folder, file)
    
        if os.path.isfile(pathname):
            ext_without_dot = os.path.splitext(file)[1][1:]
            if ext_without_dot == "png":
                remove_exif(pathname, out_folder)
        elif os.path.isdir(pathname):
            batch_remove_exif(pathname, os.path.join(out_folder, file))
    
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python cleancut.py input_folder output_folder")        
        return
    
    in_folder = sys.argv[1]
    out_folder = sys.argv[2]
    batch_remove_exif(in_folder, out_folder)
    print("Done")

if __name__ == "__main__":
    main()
