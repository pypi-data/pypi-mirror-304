from ragpipe.encoders import Encoder

class BGE_M3:
    #https://github.com/FlagOpen/FlagEmbedding/tree/master/FlagEmbedding/BGE_M3
    #https://github.com/milvus-io/pymilvus/blob/master/examples/hello_hybrid_sparse_dense.py
    pass

class MixbreadEncoder(Encoder):
    #https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1

    @classmethod
    def from_config(cls, name, config): #name = "mixedbread-ai/mxbai-embed-large-v1"
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            print('The mixbread embeddings need sentence_transformers library installed.')

        model_loader = lambda: SentenceTransformer(name, truncate_dim=config.size)
        return cls(name='mixbread', mo_loader=model_loader, rep_type = 'single_vector', config=config)
    

    def _transform_query(query: str) -> str:
        """ For retrieval, add the prompt for query (not for documents).
        """
        return f'Represent this sentence for searching relevant passages: {query}'

        
    def encode(self, docs, size=1024, dtype='float32', is_query=False):
        from sentence_transformers.quantization import quantize_embeddings
        dtype2precision = { #TODO: check, fix this map
                    'float32': 'float32', 'float16': 'float16', 'bfloat16': 'bfloat16',
                    'binary': 'ubinary'
        }
        embeddings = self.get_model().encode(docs) #TODO: check size?
        dtype = self.config.dtype
        embeddings = quantize_embeddings(embeddings, precision=dtype2precision[dtype])
    
        return embeddings
    
    def get_similarity_fn(self):
        assert self.name == "mixedbread-ai/mxbai-embed-large-v1"
        from sentence_transformers.util import cos_sim
        return cos_sim
    