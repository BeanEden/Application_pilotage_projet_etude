import os
import base64

def convert_images_to_base64(src_dir, dest_dir):
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Check if source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory not found: {src_dir}")
        return

    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        
        # Skip directories (including the base64 destination directory if it's inside images)
        if os.path.isdir(file_path):
            continue
            
        try:
            with open(file_path, "rb") as image_file:
                # Read the binary content and convert to base64 string
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
            # Determine output filename (saving as .txt)
            base_name, ext = os.path.splitext(filename)
            dest_file_path = os.path.join(dest_dir, f"{base_name}.txt")
            
            with open(dest_file_path, "w") as dest_file:
                dest_file.write(encoded_string)
                
            print(f"Converted {filename} to {dest_file_path}")
        except Exception as e:
            print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    # Get absolute paths relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_directory = os.path.join(current_dir, "images")
    destination_directory = os.path.join(source_directory, "base64")
    
    print(f"Starting conversion...")
    print(f"Source: {source_directory}")
    print(f"Destination: {destination_directory}")
    
    convert_images_to_base64(source_directory, destination_directory)
    print("Done!")
