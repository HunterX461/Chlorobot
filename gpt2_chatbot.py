from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model and tokenizer
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set padding token
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token  # Use eos_token as padding token

def generate_response(objects_detected: list, user_query: str):
    # Create a focused context for the model
    object_list = ', '.join(objects_detected)
    context = f"Objects detected: {object_list}. Question: {user_query}"

    # Tokenize input with attention mask
    inputs = gpt2_tokenizer(context, return_tensors='pt', padding=True, truncation=True, max_length=50, return_attention_mask=True)

    # Generate response with appropriate settings
    outputs = gpt2_model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],  # Include attention mask
        max_new_tokens=20,  # Limit the number of new tokens generated
        num_return_sequences=1,
        do_sample=False,  # Disable sampling for deterministic output
        temperature=0.7,  # Control randomness
        top_k=50,  # Only consider top k tokens
        top_p=0.95,  # Nucleus sampling
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    # Decode the response
    response = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Clean up the response to extract the relevant information
    answer_start = response.lower().find("answer:")
    if answer_start != -1:
        response = response[answer_start:].split("Answer:")[-1].strip()  # Get part after "Answer:"
        # Further clean the response by removing unnecessary phrases
        response = response.split(".")[0].strip()  # Take only the first sentence
    else:
        response = "Unable to determine the response."

    return response

# Example usage
detected_objects = ["cat"]
user_question = "What is this image?"
response = generate_response(detected_objects, user_question)
print(f"Response: {response}")  # Expected to get a clearer, more direct answer

