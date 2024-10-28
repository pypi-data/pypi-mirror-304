from pandas import DataFrame
from sentence_transformers import SentenceTransformer

from ggd_py_utils.tracing.metrics import time_block

def embed_dataframe(
        corpus_path:str, 
        faiss_index_file:str,
        df_data_file:str,
        ingore_features_columns:list, 
        model:SentenceTransformer,
        features_field_name:str="Features"
    ) -> DataFrame:
    
    """
    Embed a DataFrame using a FastText model, and save the DataFrame with the embeddings to a file, and the Faiss index to another file.

    Parameters
    ----------
    corpus_path : str
        The path to the Parquet file containing the text data.
    faiss_index_file : str
        The path to save the Faiss index to.
    df_data_file : str
        The path to save the DataFrame to.
    ingore_features_columns : list
        The columns to ignore when defining the features.
    model : SentenceTransformer
        The SentenceTransformer model to use for embedding.
    features_field_name : str, optional
        The name of the feature column, by default "Features".

    Returns
    -------
    The vectorized Dataframe.
    """
    
    with time_block(block_name="Read Parquet"):
        from pandas import read_parquet

        df:DataFrame = read_parquet(path=corpus_path)
    
    with time_block(block_name="Define Features"):
        from ggd_py_utils.machine_learning.fasttext.unsupervised.data_preparation import define_features
        df:DataFrame = define_features(df=df, ignore=ingore_features_columns, features_field_name=features_field_name)
    
    with time_block(block_name="Clean Text"):
        from ggd_py_utils.machine_learning.data.cleaning import clean_text

        df["Features"] = df["Features"].apply(lambda x: clean_text(text=x))
    
    with time_block(block_name="Get Embeddings"):
        sentences: list = df["Features"].tolist()
        embeddings = model.encode(sentences=sentences, batch_size=42, show_progress_bar=True).tolist()

        df['Embeddings'] = embeddings

    with time_block(block_name="Transform Embeddings"):
        from numpy import array
        
        embeddings_matrix = array(df["Embeddings"].tolist()).astype('float32')

    with time_block(block_name="Normalize Embeddings"):
        from faiss import normalize_L2
        
        normalize_L2(embeddings_matrix)
    
    with time_block(block_name="Create Faiss Index"):
        model_dimensions:int = model.get_sentence_embedding_dimension()

        from faiss import IndexFlatIP

        index = IndexFlatIP(model_dimensions)
        
        index.add(embeddings_matrix)
    
    with time_block(block_name="Save Faiss Index"):
        from faiss import write_index

        write_index(index, faiss_index_file)
        
        from ggd_py_utils.tracing.file import get_file_size
    
        _, faiss_index_size = get_file_size(filename=faiss_index_file)

        print(f"FAISS index size: {faiss_index_size}")
    
    with time_block(block_name="Save DataFrame"):
        df.to_pickle(path=df_data_file)
        
        from ggd_py_utils.tracing.file import get_file_size
    
        _, df_data_file_size = get_file_size(filename=df_data_file)

        print(f"DataFrame size: {df_data_file_size}")

    return df