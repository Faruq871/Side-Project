# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = ""

# Load the latest version
df = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS,"olistbr/brazilian-ecommerce",file_path)

# sources : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce