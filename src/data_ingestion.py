import pandas as pd
import os
from sklearn.model_selection import train_test_split
import logging

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

#logger configurations

logger = logging.getLogger('data_ingestion')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_file_path = os.path.join(log_dir, 'data_ingestion.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

formatter =  logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_data(data_url:str) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_url)
        logger.debug("Data Loaded from %s",data_url)
        return df
    except pd.errors.ParserError as e:
        logger.error("Faild to parse CSV file %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error occured while loading the data %s",e)
        raise

def preprocess_data(df:pd.DataFrame) -> pd.DataFrame:
    """Preproces the data"""
    try:
        df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
        df.rename(columns={'v1':'target', 'v2':'text'}, inplace=True)
        logger.debug('Data Preprocessing completed')
        return df

    except KeyError as e:
        logger.error("Missing column in the DataFrame: %s",e)
        raise
    except Exception as e:
        logger.error("Unexcepted Error during preprocessing %s",e)
        raise

def save_data(train_data:pd.DataFrame, test_data:pd.DataFrame, data_path:str) -> None:
    """Save the train and test datasets"""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_path = os.path.join(raw_data_path, 'train.csv')
        test_path = os.path.join(raw_data_path, 'test.csv')
        train_data.to_csv(path_or_buf=train_path,index=False)
        test_data.to_csv(path_or_buf=test_path, index=False)
        logger.debug("Train and test data saved to %s", raw_data_path)
    except Exception as e:
        logger.error("Unexpected error while saving the data: %s",e)
        raise

def main():
    try:
        test_size = 0.3
        data_path = 'https://raw.githubusercontent.com/vikashishere/Datasets/refs/heads/main/spam.csv'
        df = load_data(data_url=data_path)
        final_df = preprocess_data(df)
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=2)
        save_data(train_data, test_data, data_path='data')

    except Exception as e:
        logger.error("Failed to complete the data ingestion process : %s",e)


if __name__ == "__main__":
    main()
    

