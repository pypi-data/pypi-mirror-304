import re

# Farhan Ali ✨
# i.farhanali.dev@gmail.com 💌


def parse(cookies: str, delimiter: str = ";") -> dict:
    """ 
    Parses a cookie string and returns a dictionary of cookies. 
    If the cookie string is invalid, an empty dictionary is returned. 
    Just a little magic to make things sweeter! 🍪
    """
    # Doing my magic here to extract key-value pairs! 🎩✨
    # Trim any leading or trailing delimiters from the cookie string
    cookies = cookies.strip(delimiter)
    matches = re.findall(fr"\s*(.*?)=(.*?){delimiter}\s*", cookies)
    
    parsed = {}
    if not matches:
        return parsed
    
    for match in matches:
        if len(match) == 2:
            parsed[match[0].strip()] = match[1].strip()
    
    return parsed


def encode(cookies: dict) -> str:
    """
    Encodes a dictionary of cookies into a cookie string format. 
    Returns the final string representation of the cookies. 
    Let’s turn these cookies into a yummy string! 😋
    """
    # Time to turn my cookie dictionary into a cute string! 🥳
    encoded = []

    for name, value in cookies.items():
        encoded.append(f"{name}={value}")
    
    return "; ".join(encoded)
