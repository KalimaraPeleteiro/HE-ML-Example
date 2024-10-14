"""Modelo utilizado para a avaliação de ML."""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


class LinearModel:
    def __init__(self, dataset="data/insurance.csv", model=LinearRegression(), random_state=1208) -> None:
        self.dataset = pd.read_csv(dataset)
        self.model = model
        self.random_state = random_state
        self.metrics = {}


    def train(self, last_column):
        """
        Processo de Treinamento. São computadas as métricas:
        . Erro Médio Absoluto (MAE) ->            Diferença absoluta entre valores previstos e reais.
        . Erro Médio Quadrático (MSE) ->          Média dos quadrados das diferenças.
        . Raiz do Erro Médio Quadrático (RMSE) -> Versão do MSE mais sensível a Outliers.
        . Coeficiente R² ->                       Proporção da Variância da Variável Predita. Quanto mais próximo de 1, melhor ajuste.
        """

        y = self.dataset[last_column]
        x = self.dataset.drop(columns=[last_column])
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, 
                                                            random_state=self.random_state)

        self.model.fit(x_train, y_train)
        y_predictions = self.model.predict(x_test)

        self.metrics['MSE'] = mean_squared_error(y_test, y_predictions)
        self.metrics['RMSE'] = np.sqrt(self.metrics['MSE'])
        self.metrics['R²'] = r2_score(y_test, y_predictions)
        self.metrics['MAE'] = mean_absolute_error(y_test, y_predictions)


    def get_results(self):
        if self.metrics != {}:
            print("Métricas de Treinamento...\n")
            for metric, value in self.metrics.items():
                print(f"{metric}: {value:.4f}")
        else:
            print("Sem métricas computadas. Treine o modelo primeiro.")


if __name__ == "__main__":
    model = LinearModel()
    model.get_results()
