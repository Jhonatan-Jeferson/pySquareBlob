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
    print(account_info.storage_occupied)
    print(account_info.billing.extra_storage)
    print(account_info.billing.objects_price)
    print(account_info.billing.storage_price)
    print(account_info.billing.total_estimate)
    print(account_info.plan_included)

    # if you don't delete the variable called 'blob_client'
    # it will maintain your account info in cache
    # even if you try to call that property again
    new_account_info = await blob_client.account_info
    # Check the console

