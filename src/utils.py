import yaml
import logging
import os
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)


log_dir = "logs"
os.makedirs("logs", exist_ok=True)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_file_path = os.path.join(log_dir, "utils.log")

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_configurations(path:str):
    try:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        logger.debug("Parameters retrived from %s",path)
        return config
    
    except FileNotFoundError as e:
        logger.error("File not found %s",e)
        raise
    except Exception as e:
        logger.error("Unexcepted error occured during retriving the parameters %s",e)
        raise

