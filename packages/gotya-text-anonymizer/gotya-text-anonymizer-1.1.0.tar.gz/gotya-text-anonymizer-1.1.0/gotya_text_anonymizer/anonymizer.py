import re
from typing import Any, List, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from collections import OrderedDict

def get_pii_regex_patterns() -> OrderedDict[str, str]:
    return OrderedDict([
        # Add more patterns here as needed
        ('ssn', r'\b\d{3}-\d{2}-\d{4}\b'),
        ('brp', r'\b[A-Z]{2}\d{7}\b'),
        ('uk_id', r'\b[A-Z]{3}\d{6}[A-Z]{1}\b'),
        ('email', r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        ('phone', r'\b(?:\+\d{1,2}\s?)?(?:(?:\d{2,4}[-.\s]?){2}\d{2,4}|\(\d{3}\)\s?\d{3}[-.]?\d{4})\b'),
        ('address', r'\b\d{1,5} [a-zA-Z0-9 ]+ [a-zA-Z]{2,} [0-9]{5}\b'),
        ('CREDIT_CARD', r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
        ('pin', r'\b\d{4}\b(?!\s(?:st|nd|rd|th))'),
        ('cvv', r'\b\d{3}\b(?!\s(?:st|nd|rd|th))')
    ])


class GotyaTextAnonymizer:
    def __init__(self, input_text: str, confidence_threshold: Optional[float] = None):
        self.input_text = input_text
        self.confidence_threshold = confidence_threshold
        self.nlp_pipeline = self.get_nlp_pipeline()

    @staticmethod
    def redact_text(input_text: str, pii_info: Optional[List[str]] = []) -> str:
        pii_regex_patterns = get_pii_regex_patterns()

        for pattern_name, pattern in pii_regex_patterns.items():
            input_text = re.sub(pattern, f'<{pattern_name.upper()}>', input_text, flags=re.IGNORECASE)
        return input_text

    @staticmethod
    def get_nlp_pipeline() -> Any:
        tokenizer = AutoTokenizer.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
        model = AutoModelForTokenClassification.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
        return pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    def anonymize_text_with_nlp_pipeline(self, input_text: str) -> str:
        detected_entities = self.nlp_pipeline(input_text)
        
        if self.confidence_threshold is not None:
            detected_entities = [entity for entity in detected_entities if entity['score'] >= self.confidence_threshold]

        for entity in detected_entities:
            input_text = input_text.replace(entity["word"], f"<{entity['entity_group']}>")

        return input_text

    def get_redacted_text(self) -> str:
        anonymized_text_nlp = self.anonymize_text_with_nlp_pipeline(self.input_text)
        pii_info = []
        redacted_text = self.redact_text(anonymized_text_nlp, pii_info)
        return redacted_text


def main(input_text: str, confidence_threshold: Optional[float] = None) -> str:
    anonymizer = GotyaTextAnonymizer(input_text, confidence_threshold)
    redacted_text = anonymizer.get_redacted_text()
    print('\nGotya Text Anonymizer (PER,LOC,ORG,DATE_TIME,NRP,brp,uk_id,email,phone,address,CREDIT_CARD,pin,cvv):\n')
    print(redacted_text, "\n\n")
    return redacted_text


if __name__ == "__main__":
    text = """My name is gotya tech and I live in Berlin, credit card 1234567890123456, 
    Phone Number: +441234567890, Address: 123 Main St, Anytown, UK, 
    Email: johndoe@example.com, PIN: 8888, CVV: 123"""
    threshold = 0.3
    redacted_text = main(text, threshold)

