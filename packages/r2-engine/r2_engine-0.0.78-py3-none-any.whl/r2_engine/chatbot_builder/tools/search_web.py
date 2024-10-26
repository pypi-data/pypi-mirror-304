from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
search = GoogleSerperAPIWrapper()

@tool
def search_web(query):
    """Útil cuando necesitas buscar en la web"""

    return search.run(query)

