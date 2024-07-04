
def logs(message: str):

    """Just print logs of what the code is doing"""

    def decorator(func):

        """Decorator of logs"""

        async def wrapper(*args, **kwargs):

            """Wrapper of logs"""

            print(f"\033[33m{message}\033[0m")
            result = await func(*args, **kwargs)
            return result
        
        return wrapper
    
    return decorator