from transformers import GPT2LMHeadModel, GPT2Tokenizer

class GPT2ChatBot:
    def __init__(self, model_name="gpt2"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.load_model()

    def load_model(self):
        # Load pre-trained GPT-2 model and tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)

    def generate_text(self, input_text):
        # Encode input text, generate response, and decode the output
        inputs = self.tokenizer.encode(input_text, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=200, num_return_sequences=1)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
if __name__ == "__main__":
    bot = GPT2ChatBot()  # You can specify other models like "gpt2-medium"
    input_text = "Transformers are "
    generated_text = bot.generate_text(input_text)
    print("Generated text:")
    print(generated_text)
