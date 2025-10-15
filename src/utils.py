"""
Utility functions for FinAdvisor Chatbot
"""

import pandas as pd
import json
import random
from typing import List, Dict, Any


def load_securities_data(filepath: str) -> pd.DataFrame:
    """Load securities dataset."""
    return pd.read_csv(filepath)


def create_synthetic_dataset(securities_df: pd.DataFrame, num_samples: int = 5000) -> List[Dict[str, str]]:
    """
    Create synthetic conversational dataset from securities data.

    Args:
        securities_df: DataFrame with securities information
        num_samples: Number of conversation pairs to generate

    Returns:
        List of conversation dictionaries with 'question' and 'answer' keys
    """
    conversations = []

    # Question templates
    question_templates = [
        "What is the sector of {company}?",
        "Tell me about {company} stock.",
        "What industry is {company} in?",
        "Where is {company} headquartered?",
        "What does {company} do?",
        "Give me information about {ticker}.",
        "What sector does {ticker} belong to?",
        "Is {company} in the {sector} sector?",
        "Tell me the headquarters location of {company}.",
        "What is {ticker}'s industry?"
    ]

    # Answer templates
    answer_templates = [
        "{company} is in the {sector} sector and {sub_industry} industry. It's headquartered in {location}.",
        "{company} ({ticker}) operates in the {sector} sector, specifically in {sub_industry}. The company is based in {location}.",
        "The company {company} is part of the {sector} sector and works in {sub_industry}. Headquarters: {location}.",
        "{ticker} belongs to {company}, which is in the {sector} sector and {sub_industry} industry, located in {location}.",
        "{company} is a {sector} company specializing in {sub_industry}, with headquarters in {location}."
    ]

    for _ in range(num_samples):
        company = securities_df.sample(1).iloc[0]

        # Select random question template
        question_template = random.choice(question_templates)

        # Fill in question
        if '{ticker}' in question_template:
            question = question_template.format(ticker=company['Ticker symbol'])
        elif '{sector}' in question_template:
            question = question_template.format(
                company=company['Security'],
                sector=company['GICS Sector']
            )
        else:
            question = question_template.format(company=company['Security'])

        # Select random answer template
        answer_template = random.choice(answer_templates)
        answer = answer_template.format(
            company=company['Security'],
            ticker=company['Ticker symbol'],
            sector=company['GICS Sector'],
            sub_industry=company['GICS Sub Industry'],
            location=company['Address of Headquarters']
        )

        conversations.append({
            'question': question,
            'answer': answer
        })

    return conversations


def save_conversations(conversations: List[Dict[str, str]], filepath: str) -> None:
    """Save conversations to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(conversations, f, indent=2)


def load_conversations(filepath: str) -> List[Dict[str, str]]:
    """Load conversations from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def calculate_dataset_stats(conversations: List[Dict[str, str]]) -> Dict[str, Any]:
    """Calculate basic statistics about the dataset."""
    questions = [conv['question'] for conv in conversations]
    answers = [conv['answer'] for conv in conversations]

    return {
        'total_conversations': len(conversations),
        'avg_question_length': sum(len(q.split()) for q in questions) / len(questions),
        'avg_answer_length': sum(len(a.split()) for a in answers) / len(answers),
        'unique_questions': len(set(questions)),
        'unique_answers': len(set(answers))
    }


def filter_financial_questions(conversations: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter conversations to keep only financial/stock related questions."""
    financial_keywords = [
        'sector', 'industry', 'stock', 'company', 'headquarters', 'headquartered',
        'ticker', 'market', 'finance', 'business'
    ]

    filtered = []
    for conv in conversations:
        question_lower = conv['question'].lower()
        if any(keyword in question_lower for keyword in financial_keywords):
            filtered.append(conv)

    return filtered


if __name__ == "__main__":
    # Example usage
    securities_df = load_securities_data("data/securities.csv")
    conversations = create_synthetic_dataset(securities_df, 100)
    save_conversations(conversations, "data/processed/sample_conversations.json")

    stats = calculate_dataset_stats(conversations)
    print("Dataset Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")