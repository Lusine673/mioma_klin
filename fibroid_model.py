import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

class FibroidRecurrencePredictor:
    """
    Интегральная модель прогнозирования рецидива миомы матки.
    Объединяет клинические, морфологические и ИГХ факторы.
    """
    def __init__(self):
        # Коэффициенты на основе обученной модели (ваши веса)
        self.feature_names = [
            'Возраст_42_и_менее', 'Длительность_7лет', 'Отсутствие_родов',
            'НГЭ', 'НЖО', 'Быстрый_рост', 'Фибриноидный_некроз',
            'VEGF_высокий', 'TGF_beta_высокий'
        ]
        self.weights = np.array([1.25, 0.17, 0.85, 2.13, 2.47, 0.17, 1.48, 1.81, 0.99])
        self.intercept = -4.5  # Базовый порог модели
        
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_probability(self, features):
        """
        features: dict или list факторов (0 или 1)
        """
        z = np.dot(features, self.weights) + self.intercept
        return self.sigmoid(z)

    def get_risk_category(self, prob):
        threshold = 0.25 # Порог из диссертации
        if prob >= threshold:
            return "ВЫСОКИЙ РИСК (Рекомендована адъювантная терапия)"
        return "НИЗКИЙ РИСК"

# Пример использования
if __name__ == "__main__":
    predictor = FibroidRecurrencePredictor()
    
    # Данные новой пациентки: НГЭ(+), НЖО(+), VEGF(+) - типичный рецидив
    sample_patient = [1, 0, 1, 1, 1, 0, 0, 1, 0] 
    
    p = predictor.predict_probability(sample_patient)
    risk = predictor.get_risk_category(p)
    
    print(f"Прогноз для пациента:")
    print(f"Вероятность рецидива: {p:.2%}")
    print(f"Категория: {risk}")
