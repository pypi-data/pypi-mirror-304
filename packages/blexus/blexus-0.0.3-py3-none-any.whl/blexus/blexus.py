import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

class TextGenerator:
    def __init__(self, model: GPT2LMHeadModel, use_gpu: bool):
        # Check if GPU is available and use it if specified
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        
        # Move the model to the appropriate device
        self.model = model.to(self.device)
        
        # Load the tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(model.config._name_or_path)  # Extracts the model path

        # Set model to evaluation mode
        self.model.eval()

    def quble_generate_text(self, prompt: str, system: str, max_length: int = 50, num_return_sequences: int = 1, temperature: float = 1.0) -> str:
        # Encode the prompt
        prompt = "SYSTEM: " + system + " <|endofsystem|> USER: " + prompt + "<|endofuser|>\nASSISTANT:"
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        # Generate continuation
        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=temperature  # Use temperature for sampling
            )

        # Decode the generated text
        generated_texts = [self.tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
        return generated_texts
    
    def FCP_generate_text(self, prompt: str, system: str, s1: str, s2: str, u1: str, u2: str, a1: str, max_length: int = 50, num_return_sequences: int = 1, temperature: float = 1.0) -> str:
        # Encode the prompt
        prompt = s1 + system + s2 + u1 + prompt + u2 + a1
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        # Generate continuation
        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=temperature  # Use temperature for sampling
            )

        # Decode the generated text
        generated_texts = [self.tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
        return generated_texts

    def eject_model(self):
        """Remove the model and clear resources."""
        self.model = None
        self.tokenizer = None
        torch.cuda.empty_cache()  # Clear the CUDA cache if using GPU
        print("Model ejected and resources cleared.")
