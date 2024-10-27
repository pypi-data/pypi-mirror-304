# roswagger/__init__.py

# Made by RoSwagger Developers at roswagger.com
# Visit our creator program here for unrestricted access for free at
# discord.roswagger.com

import requests
import time
import json
import dateutil.parser
from datetime import datetime

def Swagger(endpoint, username):
    while True:
        response = requests.get(f"https://roswagger.com/get/{endpoint}/{username}")
        CoolSwag = response.json()
        
        if "error" in CoolSwag and "Please wait" in CoolSwag["error"]:
            wait_time = CoolSwag.get("timeLeft", 5)
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return CoolSwag

def swagify(date_string: str, format_type: str = 'f'):
    """
    Converts a date string to a Discord-compatible timestamp format.

    Args:
        date_string (str): The date in ISO 8601 format or similar.
        format_type (str): The desired Discord timestamp format (e.g., 't', 'T', 'd', 'D', 'f', 'F', 'R').

    Returns:
        str: JSON string with the timestamp and format description.
    """
    
    dt = dateutil.parser.isoparse(date_string)
    unix_timestamp = int(dt.timestamp())
    formats = {
        't': 'Short Time (ex., 9:06 PM)', 
        'T': 'Long Time (ex., 9:06:40 PM)', 
        'd': 'Short Date (ex., 02/27/2006)', 
        'D': 'Long Date (ex., February 27, 2006)', 
        'f': 'Short DateTime (ex., February 27, 2006 9:06 PM)', 
        'F': 'Long DateTime (ex., Monday, February 27, 2006 9:06 PM)', 
        'R': 'Relative Time (ex., 16 years ago)'
    }

    # Validate format_type
    if format_type not in formats:
        raise ValueError("Invalid format_type. Use one of the following: 't', 'T', 'd', 'D', 'f', 'F', 'R'.")

    # Create the formatted timestamp
    timestampifier = f"<t:{unix_timestamp}:{format_type}>"
    description = formats[format_type]
    example = dt.strftime('%Y-%m-%d %H:%M:%S')

    # Create JSON output
    result = {
        "original_date": date_string,
        "iso_format": dt.isoformat(),
        "formatted_timestamp": timestampifier,
        "description": description
    }
    
    return json.dumps(result, indent=4)

def all(username): return Swagger('all', username)
def userId(username): return Swagger('userId', username)
def lastOnline(username): return Swagger('lastOnline', username)
def creationDate(username): return Swagger('creationDate', username)
def thumbnail(username): return Swagger('thumbnail', username)
def rap(username): return Swagger('rap', username)
def verified(username): return Swagger('verified', username)
def pastUsernames(username): return Swagger('pastUsernames', username)
