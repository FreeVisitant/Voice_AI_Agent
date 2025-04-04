from transformers import pipeline

class NLPProcessor:
    def __init__(self):
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )
        self.intent_classifier = pipeline(
            "text-classification",
            model="Falconsai/intent_classification"
        )

    def extract_entities(self, text: str):
        """
        Extrae entidades clave del texto utilizando el pipeline de NER.

        Args:
            text (str): Texto a procesar.

        Returns:
            List[dict]: Lista de entidades con su etiqueta, puntuación y posiciones.
        """
        entities = self.ner_pipeline(text)
        return entities

    def classify_intent(self, text: str):
        """
        Detecta la intención del usuario a partir del texto utilizando el pipeline de clasificación.

        Args:
            text (str): Texto a procesar.

        Returns:
            List[dict]: Resultado de la clasificación de intenciones (etiqueta y puntuación).
        """
        intent = self.intent_classifier(text)
        return intent

if __name__ == "__main__":
    processor = NLPProcessor()

    # Extracción de entidades
    sample_text = "Mi nombre es Juan Pérez, trabajo en Empresa XYZ y necesito un presupuesto de 10000."
    print("Entidades extraídas:")
    for entity in processor.extract_entities(sample_text):
        print(entity)

    # Clasificación de intención
    sample_intent_text = "Estoy interesado en contratar servicios de consultoría y desarrollar software a medida."
    print("\nIntención detectada:")
    for item in processor.classify_intent(sample_intent_text):
        print(item)
