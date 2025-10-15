"""
FinAdvisor Chatbot - Gradio Interface
A financial advisor chatbot using fine-tuned GPT-2 model
"""

import gradio as gr
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import os

# Model configuration
MODEL_PATH = "models/finadvisor_gpt2"

class FinAdvisorChatbot:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        """Load the fine-tuned GPT-2 model and tokenizer."""
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
            self.model.eval()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using base GPT-2 model for demonstration...")
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = GPT2LMHeadModel.from_pretrained('gpt2')
            self.model.eval()

    def generate_answer(self, question, max_length=150, temperature=0.7, top_p=0.9):
        """
        Generate an answer for the given question.

        Args:
            question: User's question
            max_length: Maximum length of generated response
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter

        Returns:
            Generated answer string
        """
        if self.model is None or self.tokenizer is None:
            return "Sorry, the model is not loaded properly."

        input_text = f"Question: {question}\nAnswer:"
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                early_stopping=True,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        # Extract answer part
        if "Answer:" in generated_text:
            answer = generated_text.split('Answer:')[-1].strip()
        else:
            answer = generated_text.strip()

        return answer

# Initialize chatbot
chatbot = FinAdvisorChatbot()

def chatbot_response(message, history):
    """
    Process user message and return chatbot response.

    Args:
        message: User's message
        history: Chat history

    Returns:
        Chatbot response
    """
    response = chatbot.generate_answer(message)
    return response

# Create Gradio interface
def create_interface():
    """Create and configure the Gradio chat interface."""

    iface = gr.ChatInterface(
        fn=chatbot_response,
        title="🤖 FinAdvisor Chatbot",
        description="""
        **Welcome to FinAdvisor!** 💰

        I'm your financial advisor chatbot specializing in stock market information.
        Ask me questions about companies, sectors, industries, and headquarters!

        **Examples:**
        - What is Apple's sector?
        - Tell me about Microsoft stock
        - Where is Google headquartered?
        - What industry is Amazon in?
        """,
        examples=[
            "What is Apple's sector?",
            "Tell me about Microsoft",
            "Where is Google headquartered?",
            "What industry is Amazon in?",
            "Is Tesla in the automotive sector?",
            "Give me information about JPM"
        ],
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .message.user {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .message.bot {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
        """
    )

    return iface

if __name__ == "__main__":
    # Create and launch interface
    iface = create_interface()

    # Launch with custom settings
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True for public sharing
        show_error=True
    )