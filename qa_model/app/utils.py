import torch
from transformers import AutoTokenizer, AutoModel

class QAEmbedder:
  def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
    """
    Defines a QA embedding model. This is, given a set of questions,
    this class returns the corresponding embedding vectors.
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    self.model = None
    self.tokenizer = None
    self.model_name = model_name
    self.set_model(model_name)
  
  
  def get_model(self, model_name):
    """
    Loads a general tokenizer and model using pytorch
    'AutoTokenizer' and 'AutoModel'
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer
  
  
  def set_model(self, model_name):
    """
    Sets a general tokenizer and model using the 'self.get_model'
    method.
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    self.model, self.tokenizer = self.get_model(self.model_name)
  
  
  def _mean_pooling(self, model_output, attention_mask):
    """
    Internal method that takes a model output and an attention
    mask and outputs a mean pooling layer.
    
    Args:
      model_output (`torch.Tensor`): output from the QA model
      attention_mask (`torch.Tensor`): attention mask defined in the QA tokenizer
      
    Returns:
      The averaged tensor.
    """
    token_embeddings = model_output[0]
    
    input_mask_expanded = (
      attention_mask
      .unsqueeze(-1)
      .expand(token_embeddings.size())
      .float()
    )
    
    pool_emb = (
      torch.sum(token_embeddings * input_mask_expanded, 1) 
      / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    )
    
    return pool_emb
  
  
  def get_embeddings(self, questions, batch=32):
    """
    Gets the corresponding embeddings for a set of input 'questions'.
    
    Args:
      questions (`list` of `str`): List of strings defining the questions to be embedded
      batch (`int`): Performs the embedding job 'batch' questions at a time
      
    Returns:
      The embedding vectors.
    """
    question_embeddings = []
    for i in range(0, len(questions), batch):
    
        # Tokenize sentences
        encoded_input = self.tokenizer(questions[i:i+batch], padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Perform mean pooling
        batch_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        question_embeddings.append(batch_embeddings)
    
    question_embeddings = torch.cat(question_embeddings, dim=0)
    return question_embeddings



class QASearcher:
  def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
    """
    Defines a QA Search model. This is, given a new question it searches
    the most similar questions in a set 'context' and returns both the best
    question and associated answer.
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    self.answers = None
    self.questions = None
    self.question_embeddings = None
    self.embedder = QAEmbedder(model_name=model_name)
  
  
  def set_context_qa(self, questions, answers):
    """
    Sets the QA context to be used during search.
    
    Args:
      questions (`list` of `str`):  List of strings defining the questions to be embedded
      answers (`list` of `str`): Best answer for each question in 'questions'
    """
    self.answers = answers
    self.questions = questions
    self.question_embeddings = self.get_q_embeddings(questions)
  
  
  def get_q_embeddings(self, questions):
    """
    Gets the embeddings for the questions in 'context'.
    
    Args:
      questions (`list` of `str`):  List of strings defining the questions to be embedded
    
    Returns:
      The embedding vectors.
    """
    question_embeddings = self.embedder.get_embeddings(questions)
    question_embeddings  = torch.nn.functional.normalize(question_embeddings, p=2, dim=1)
    return question_embeddings.transpose(0,1)
  
  
  def cosine_similarity(self, questions, batch=32):
    """
    Gets the cosine similarity between the new questions and the 'context' questions.
    
    Args:
      questions (`list` of `str`):  List of strings defining the questions to be embedded
      batch (`int`): Performs the embedding job 'batch' questions at a time
    
    Returns:
      The cosine similarity
    """
    question_embeddings = self.embedder.get_embeddings(questions, batch=batch)
    question_embeddings = torch.nn.functional.normalize(question_embeddings, p=2, dim=1)
    
    cosine_sim = torch.mm(question_embeddings, self.question_embeddings)
    
    return cosine_sim
  
  
  def get_answers(self, questions, batch=32):
    """
    Gets the best answers in the stored 'context' for the given new 'questions'.
    
    Args:
      questions (`list` of `str`):  List of strings defining the questions to be embedded
      batch (`int`): Performs the embedding job 'batch' questions at a time
    
    Returns:
      A `list` of `dict`'s containing the original question ('orig_q'), the most similar
      question in the context ('best_q') and the associated answer ('best_a').
    """
    similarity = self.cosine_similarity(questions, batch=batch)
    
    response = []
    for i in range(similarity.shape[0]):
      best_ix = similarity[i].argmax()
      best_q = self.questions[best_ix]
      best_a = self.answers[best_ix]
      
      response.append(
        {
          'orig_q':questions[i],
          'best_q':best_q,
          'best_a':best_a,
        }
      )
    
    return response