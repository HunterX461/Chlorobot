from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model and tokenizer
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set padding token
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token

def generate_response(diseases_detected: list, user_query: str):
    """Generate a chatbot response based on detected diseases."""
    disease_list = ', '.join(diseases_detected)
    context = f"Diseases detected: {disease_list}. Question: {user_query}"

    # Tokenize input with attention mask
    inputs = gpt2_tokenizer(context, return_tensors='pt', padding=True, truncation=True, max_length=50)

    # Generate response
    outputs = gpt2_model.generate(
        inputs['input_ids'], attention_mask=inputs['attention_mask'],
        max_new_tokens=50, do_sample=False, temperature=0.7, top_k=50,
        top_p=0.95, no_repeat_ngram_size=2, early_stopping=True
    )

    response = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Extract and return the first meaningful sentence
    answer_start = response.lower().find("answer:")
    if answer_start != -1:
        response = response[answer_start:].split("Answer:")[-1].split(".")[0].strip()
    else:
        response = "Unable to determine the response."
    
    return response
