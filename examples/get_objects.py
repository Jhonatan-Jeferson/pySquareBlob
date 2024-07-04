from pysquareblob import Client


async def main():

    # instantiate client passing your API key from dotenv or hardcoded
    blob_client = Client("API_key")

    # await for object
    objects_list = await blob_client.objects
    # first time you call it, it will make a request
    # and show that log on terminal

    # now if you have uploaded something before run this function
    # it must have at least one item on this list
    print(objects_list)

    # so its just use the item
    try:
        first = objects_list[0]
        print(first.id)
        print(first.size)
        print(first.created_at)
        print(first.expires_at)
    except Exception:
        pass
        