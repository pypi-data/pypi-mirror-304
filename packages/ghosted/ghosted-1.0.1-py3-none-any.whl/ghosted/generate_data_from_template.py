import pandas as pd
import numpy as np

class GenerateDataFromTemplate:
    def __init__(self, random_seed=None):
        np.random.seed(random_seed)

    @staticmethod
    def list_templates():
        """
        Lists all available templates with descriptions and parameters.
        """
        templates_info = {
            "e_commerce_recommendation": {
                "description": "Simulates customer purchase behaviors for e-commerce recommendation systems.",
                "parameters": {
                    "num_customers": "Number of unique customers (int, default=1000)",
                    "num_products": "Number of unique products (int, default=50)"
                }
            },
            "healthcare_disease_prediction": {
                "description": "Generates patient data for disease prediction in a healthcare setting.",
                "parameters": {
                    "num_patients": "Number of unique patients (int, default=1000)"
                }
            },
            "finance_fraud_detection": {
                "description": "Simulates transaction data with labels for fraud detection analysis.",
                "parameters": {
                    "num_transactions": "Number of transactions (int, default=1000)"
                }
            }
        }

        print("Available templates:")
        for template_name, info in templates_info.items():
            print(f"- {template_name}: {info['description']}")
            print("  Parameters:")
            for param, desc in info['parameters'].items():
                print(f"    - {param}: {desc}")
            print()

    def e_commerce_recommendation(self, num_customers=1000, num_products=50):
        age = np.random.randint(18, 65, num_customers)
        income = np.random.normal(50000, 15000, num_customers)
        purchase_counts = np.random.poisson(2, (num_customers, num_products))

        product_ids = [f"P{i}" for i in range(num_products)]
        product_prices = np.round(np.random.uniform(10, 500, num_products), 2)
        categories = np.random.choice(['Electronics', 'Apparel', 'Books'], num_products)

        return pd.DataFrame({
            'customer_age': age,
            'customer_income': income,
            'product_ids': np.repeat(product_ids, num_customers // num_products),
            'purchase_counts': purchase_counts.flatten()
        })

    def healthcare_disease_prediction(self, num_patients=1000):
        age = np.random.randint(0, 100, num_patients)
        bmi = np.random.normal(25, 4, num_patients)
        family_history = np.random.choice(['Yes', 'No'], num_patients)
        pre_existing_conditions = np.random.choice(['Diabetes', 'Hypertension', 'None'], num_patients)

        diagnosis = np.random.choice(['Healthy', 'Diseased'], num_patients, p=[0.7, 0.3])

        return pd.DataFrame({
            'age': age,
            'bmi': bmi,
            'family_history': family_history,
            'pre_existing_conditions': pre_existing_conditions,
            'diagnosis': diagnosis
        })

    def finance_fraud_detection(self, num_transactions=1000):
        amounts = np.round(np.random.exponential(scale=100, size=num_transactions), 2)
        location = np.random.choice(['Online', 'In-store'], num_transactions)
        time_of_day = np.random.choice(['Morning', 'Afternoon', 'Evening'], num_transactions)
        device_type = np.random.choice(['Mobile', 'Desktop', 'Tablet'], num_transactions)
        
        fraud_label = np.random.choice([0, 1], num_transactions, p=[0.97, 0.03])

        return pd.DataFrame({
            'transaction_amount': amounts,
            'location': location,
            'time_of_day': time_of_day,
            'device_type': device_type,
            'fraudulent': fraud_label
        })
