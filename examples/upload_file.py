from pysquareblob import Client


async def main():

    # instantiate client passing your API key from dotenv or hardcoded
    blob_client = Client("API_key")

    # you just have to call the upload method passing the relative path
    # and passing the name you want
    # in this example i will pass the kyojuro_rengoku.jpg 
    # it is in examples folder
    # and it name will be my_image
    uploaded_object = await blob_client.upload_object(file='examples/kyojuro_rengoku.jpg', name="my_image_rengoku")
    print(uploaded_object)

    # OBS.: You can also pass a bytes, bytesIO or BufferedIOBase object instead of a path string
    # You'll need to pass the mimetype in this case. The library will try to guess the mimetype but it's not guaranteed to work always
