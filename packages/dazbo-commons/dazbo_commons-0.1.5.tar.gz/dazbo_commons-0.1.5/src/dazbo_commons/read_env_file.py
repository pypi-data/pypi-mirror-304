""" 
Author: Darren
Date: 11/01/2022

Look for .env files, read variables from it,
and store as environment variables.

It looks for .env file in the current working directory where the script is being run from,
then checks up to three parent directories.

Then we check for env vars that have been loaded, e.g.

get_envs_from_file() # read env variables from a .env file, if we can find one
it not os.getenv('SOME_VAR'):
    os.environ['SOME_VAR'] = getpass('Enter your sensitive var: ')
"""
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)

def get_envs_from_file() -> bool:
    """ Look for .env files, read variables from it, and store as environment variables """
    potential_path = ".env"
    for _ in range(3):
        logger.debug("Trying .env at %s", os.path.realpath(potential_path))
        if os.path.exists(potential_path):
            logger.info("Using .env at %s", os.path.realpath(potential_path))
            load_dotenv(potential_path, override=True, verbose=True)
            return True
        
        potential_path = os.path.join('..', potential_path)
   
    logger.warning("No .env file found.")
    return False
