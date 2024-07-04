from pysquareblob import Client


async def main():

    # instantiate client passing your API key from dotenv or hardcoded
    blob_client = Client("API_key")

    # just get the list like you made on the get_objects test
    obj_list = await blob_client.objects

    # now pass the list you wanna remove to the method
    # for this example i'll just remove one
    remove_list = [obj_list[0]]
    request = await blob_client.delete_object(remove_list)

    print(request)