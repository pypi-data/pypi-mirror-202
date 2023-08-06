import re
from typing import Any, List, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from collections import OrderedDict

PII_REGEX_PATTERNS = OrderedDict([
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

nlp_pipeline = None

def get_nlp_pipeline() -> Any:
    global nlp_pipeline
    if nlp_pipeline is None:
        tokenizer = AutoTokenizer.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
        model = AutoModelForTokenClassification.from_pretrained("ArunaSaraswathy/bert-finetuned-ner-pii")
        nlp_pipeline = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    return nlp_pipeline

def load_model():
    get_nlp_pipeline()

def redact_text(input_text: str, pii_info: Optional[List[str]] = []) -> str:
    for pattern_name, pattern in PII_REGEX_PATTERNS.items():
        input_text = re.sub(pattern, f'<{pattern_name.upper()}>', input_text, flags=re.IGNORECASE)
    return input_text

def anonymize(input_text: str, confidence_threshold: Optional[float] = None) -> str:
    nlp_pipeline = get_nlp_pipeline()
    detected_entities = nlp_pipeline(input_text)
        
    if confidence_threshold is not None:
        detected_entities = [entity for entity in detected_entities if entity['score'] >= confidence_threshold]

    for entity in detected_entities:
        input_text = input_text.replace(entity["word"], f"<{entity['entity_group']}>")

    return input_text
