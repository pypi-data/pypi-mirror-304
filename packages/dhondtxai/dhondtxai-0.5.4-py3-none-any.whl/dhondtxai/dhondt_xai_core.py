
import numpy as np
import matplotlib.pyplot as plt

class DhondtXAI:
    def __init__(self, model):
        self.model = model
        self.features = None
        self.feature_importances = None
        self.correlation_info = None
    
    def fit(self, X_train, y_train):  # Accept y_train to fit the model
        # Train the provided model and extract feature importances
        self.model.fit(X_train, y_train)
        self.features = list(X_train.columns)
        self.feature_importances = self.model.feature_importances_
        
        # Calculate correlation between features and the main target variable
        correlations = X_train.corrwith(y_train).to_dict()
        self.correlation_info = {feature: correlations.get(feature, 0) for feature in self.features}
    
    def select_features(self, feature_names):
        print("Available features:")
        for idx, feature in enumerate(feature_names):
            print(f"{idx + 1}. {feature}")

        # Allow user to specify features to exclude from the evaluation
        exclude_input = input("Enter the variables you want to exclude from the evaluation (e.g., '2, 4' or 'HL, CVD') or 'none': ")
        exclude_features = []
        if exclude_input.lower() != 'none':
            exclude_parts = exclude_input.split(',')
            for part in exclude_parts:
                var = part.strip()
                if var.isdigit():
                    feature_index = int(var) - 1
                    if 0 <= feature_index < len(feature_names):
                        exclude_features.append(feature_names[feature_index])
                else:
                    exclude_features.append(var)

        # Allow user to enter alliances using feature names or index numbers
        alliances_input = input("Enter any alliances between the variables (e.g., '2,3 and 4' or 'HL,HLmed and CVD') or 'none': ")
        alliances = []
        if alliances_input.lower() != 'none':
            alliance_parts = alliances_input.split('and')
            for part in alliance_parts:
                allies = part.strip().split(',')
                cleaned_allies = [ally.strip() for ally in allies]
                alliances.append(cleaned_allies)

        return alliances, exclude_features

    def apply_dhondt(self, num_votes, num_mps, threshold, alliances, exclude_features):
        # Example placeholder logic, will depend on actual algorithm you plan to use
        return self.features, [num_votes // len(self.features) for _ in self.features]

    def dhondt_method(self, votes, num_mps):
        # Example placeholder logic for seat allocation
        seats = [v // 1000 for v in votes]  # Simple example to distribute seats
        return seats

    def plot_results(self, features, seats):
        plt.bar(features, seats)
        plt.xlabel('Features')
        plt.ylabel('Seats')
        plt.title("D'Hondt Method Seat Allocation")
        plt.xticks(rotation=45)
        plt.show()
