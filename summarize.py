import os
from langchain.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any, Tuple, Optional
import re
import nltk
from dotenv import load_dotenv

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


search = DuckDuckGoSearchResults()