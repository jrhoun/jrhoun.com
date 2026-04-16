import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, path)
            
            # Preserve permissions by creating ZipInfo manually
            st = os.stat(full_path)
            zinfo = zipfile.ZipInfo.from_file(full_path, rel_path)
            zinfo.compress_type = zipfile.ZIP_DEFLATED
            
            # Shift the mode by 16 bits to place it in the upper 2 bytes
            # which is where standard unix unzippers look for permissions
            zinfo.external_attr = (st.st_mode & 0xFFFF) << 16
            
            print(f"Zipping {rel_path} (mode: {oct(st.st_mode)})")
            
            with open(full_path, 'rb') as f:
                ziph.writestr(zinfo, f.read())

if __name__ == '__main__':
    zip_path = '/home/jrhoun/projects/jrhoun.com/jrhoun-theme.zip'
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipdir('/home/jrhoun/projects/jrhoun.com/custom-theme', zipf)
    print("FINISHED ZIPPING - PERMISSIONS PRESERVED")
