from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

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


    def split_text(self, text, max_chars=500):
        """
        Splits the input text into smaller chunks before tokenizing.
        Ensures text is split at spaces to avoid breaking words.
        """
        words = text.split()  # Split text into words
        chunks = []
        current_chunk = []

        for word in words:
            if sum(len(w) for w in current_chunk) + len(word) < max_chars:  # Ensure chunk length is within limits
                current_chunk.append(word)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]

        if current_chunk:  # Add last chunk if not empty
            chunks.append(" ".join(current_chunk))
        print("number of chunks ", len(chunks))
        return chunks


    def generate_text(self, input_text, max_length=1024):
        """
        Processes text in smaller pre-tokenized chunks, avoiding token overflow.
        """
        text_chunks = self.split_text(input_text, max_chars=500)  # Split input text before tokenizing
        generated_texts = []

        for chunk in text_chunks:
            inputs = self.tokenizer.encode(chunk, return_tensors="pt")  # Tokenize each chunk
            attention_mask = torch.ones_like(inputs)

            # Generate response
            outputs = self.model.generate(
                inputs,
                max_length=min(len(inputs[0]) + 50, max_length),  # Prevent exceeding max length
                num_return_sequences=1,
                attention_mask=attention_mask,
                pad_token_id=self.tokenizer.eos_token_id
            )

            # Decode and store output
            generated_texts.append(self.tokenizer.decode(outputs[0], skip_special_tokens=True))
            return " ".join(generated_texts)

        return " ".join(generated_texts)


# Example usage
if __name__ == "__main__":
    bot = GPT2ChatBot()  # You can specify other models like "gpt2-medium"
    input_text = "Transformers are "
    generated_text = bot.generate_text(input_text)
    print("Generated text:")
    print(generated_text)
