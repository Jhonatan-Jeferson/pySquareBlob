from pysquareblob import Client


async def main():

    # instantiate client passing your API key from dotenv or hardcoded
    blob_client = Client("API_key")

    # await for account info
    account_info = await blob_client.account_info
    # first time you call it, it will make a request
    # and show that log on terminal

    # now use it however you want
    print(account_info.objects)
    print(account_info.size)
    print(account_info.objectsPrice)
    print(account_info.storagePrice)
    print(account_info.totalEstimate)

    # if you don't delete the variable called 'blob_client'
    # it will maintain your account info in cache
    # even if you try to call that property again
    new_account_info = await blob_client.account_info
    # Check the console

