import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class ChatBot:
  def __init__(self, model_name='microsoft/DialoGPT-large'):
    self.model, self.tokenizer = self.load_model(model_name)
    self.chat_history = []
    self.chat_history_ids = None
    
  def load_model(self, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

  def get_reply(self, user_message):
    # save message from the user
    self.chat_history.append({
      'text':user_message, 
      'time':str(datetime.datetime.now().time().replace(microsecond=0))
    })
    
    # encode the new user message to be used by our model
    message_ids = self.tokenizer.encode(user_message + self.tokenizer.eos_token, return_tensors='pt')

    # append the encoded message to the past history so the model is aware of past context
    if self.chat_history_ids is not None:
      message_ids = torch.cat([self.chat_history_ids, message_ids], dim=-1)

    # generated a response by the bot 
    self.chat_history_ids = self.model.generate(
      message_ids,
      pad_token_id=self.tokenizer.eos_token_id, 
      do_sample=True, 
      max_length=1000, 
      top_k=100, 
      top_p=0.95,
      temperature=0.8,
    )
    
    decoded_message = self.tokenizer.decode(
      self.chat_history_ids[:, message_ids.shape[-1]:][0], 
      skip_special_tokens=True
    )
    
    # save reply from the bot
    self.chat_history.append({
      'text':decoded_message, 
      'time':str(datetime.datetime.now().time().replace(microsecond=0))
    })
    
    return decoded_message