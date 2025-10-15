# FinAdvisor Chatbot

A domain-specific chatbot for financial advisory using fine-tuned transformer models. This chatbot specializes in answering questions about stocks, companies, and market data from the S&P 500.

## Project Structure

```
finadvisor/
├── data/
│   ├── securities.csv          # S&P 500 company information
│   ├── fundamentals.csv        # Financial fundamentals data
│   ├── prices.csv              # Historical stock prices
│   └── processed/
│       └── conversations.json  # Synthetic conversational dataset
├── notebooks/
│   └── finadvisor_chatbot.ipynb # Main implementation notebook
├── models/
│   └── finadvisor_gpt2/        # Fine-tuned GPT-2 model
├── src/
│   └── utils.py                # Utility functions
├── app/
│   └── chatbot.py              # Gradio chatbot interface
└── README.md
```

## Features

- **Domain-Specific**: Specialized in financial and stock market queries
- **Generative QA**: Uses GPT-2 fine-tuned for generating natural responses
- **Web Interface**: Interactive chatbot built with Gradio
- **Evaluation Metrics**: BLEU, ROUGE, and perplexity scores
- **Synthetic Dataset**: 10,000 conversation pairs generated from real company data

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd finadvisor
```

2. Install dependencies:
```bash
pip install transformers torch datasets pandas numpy scikit-learn nltk streamlit gradio
pip install accelerate -U
pip install evaluate rouge-score
```

## Usage

### Training the Model

1. Open the Jupyter notebook:
```bash
jupyter notebook notebooks/finadvisor_chatbot.ipynb
```

2. Run all cells to:
   - Generate synthetic dataset
   - Fine-tune GPT-2 model
   - Evaluate performance

### Running the Chatbot

```bash
python app/chatbot.py
```

This will launch a Gradio web interface where you can interact with the chatbot.

## Dataset

The chatbot is trained on a synthetic dataset created from S&P 500 securities data, including:
- Company names and tickers
- Sectors and industries
- Headquarters locations
- Business descriptions

## Model Architecture

- **Base Model**: GPT-2 (124M parameters)
- **Fine-tuning**: 3 epochs with learning rate scheduling
- **Task**: Generative question answering
- **Input Format**: "Question: {question}\nAnswer: {answer}"

## Evaluation Results

- **BLEU Score**: [To be updated after training]
- **ROUGE Scores**: [To be updated after training]
- **Perplexity**: [To be updated after training]

## Examples

**Input:** "What is Apple's sector?"  
**Output:** "Apple Inc. (AAPL) operates in the Information Technology sector, specifically in Computer Hardware. The company is based in Cupertino, California."

**Input:** "Tell me about Microsoft"  
**Output:** "Microsoft Corp. (MSFT) is in the Information Technology sector and Systems Software industry. It's headquartered in Redmond, Washington."

## Hyperparameter Tuning

The model was tuned with the following parameters:
- Learning rate: 5e-5
- Batch size: 4
- Epochs: 3
- Warmup steps: 500
- Weight decay: 0.01

## Deployment

The chatbot can be deployed as:
- Web application (Gradio/Streamlit)
- API endpoint (FastAPI)
- Command-line interface

## Future Improvements

- Add conversation memory
- Implement multi-turn dialogues
- Integrate real-time stock data
- Add sentiment analysis
- Expand to more financial metrics

## License

[Add license information]

## Contributing

[Add contribution guidelines]

## Demo Video

[Link to 5-10 minute demo video showcasing functionality]