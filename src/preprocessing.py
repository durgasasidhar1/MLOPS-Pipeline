import os
import logging
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt')

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('data_preprocessing')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_file_path = os.path.join(log_dir, 'data_preprocessing.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s- %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def transform_text(text:str):
    '''Transform the input text by converting it into lower case, tokenizing, removing stop words and punctuations and stemming'''
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and  word not in string.punctuation]
    text = [ps.stem(word) for word in text]
    return " ".join(text)

def preprocess_df(df, text_column="text",target_column="target"):

    try:
        logger.debug("Starting the preprocessing of dataFrame")
        encoder = LabelEncoder()
        
        df[target_column] = encoder.fit_transform(df[target_column])
        logger.debug("Target column encoded")

        # Remove duplicate rows
        df = df.drop_duplicates(keep="first")
        logger.debug("duplicates removed")

        df[text_column] = df[text_column].apply(transform_text)

        logger.debug("Text column transformed")
        return df
    
    except KeyError as e:
        logger.error("Column not found %s",e)
        raise
    except Exception as e:
        logger.error("Unexpected error during text normalization %s",e)
        raise

def main(text_column="text", target_column='target'):
    
    try:
        train_data = pd.read_csv("./data/raw/train.csv")
        test_data = pd.read_csv('./data/raw/test.csv')
        logger.debug("data loaded properly")

        train_processed_data = preprocess_df(train_data,text_column, target_column)
        test_preprocessed_data = preprocess_df(test_data, text_column, target_column)

        data_path = os.path.join("./data","interim")
        os.makedirs(data_path, exist_ok=True)

        train_processed_data.to_csv(os.path.join(data_path, "train_preprocessed.csv"), index=False)
        test_preprocessed_data.to_csv(os.path.join(data_path, "test_preprocessed.csv"), index=False)

        logger.debug("preprocessed data saved to %s",data_path)
    
    except FileNotFoundError as e:
        logger.error("File not found %s",e)
        raise
    
    except pd.errors.EmptyDataError as e:
        logger.error("No data: %s",e)
        raise

    except Exception as e:
        logger.error("Failed to complete the data processing process %s",e)
        raise


if __name__ == "__main__":
    main()
