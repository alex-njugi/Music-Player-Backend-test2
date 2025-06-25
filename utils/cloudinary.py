import os
import cloudinary , cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_mp3(file):
    result =cloudinary.uploader.upload(
        file,
        resource_type ="video",
        format= "mp3"
    )
    
    return result.get("secure_url")