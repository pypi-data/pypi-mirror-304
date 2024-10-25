def ml1():
    return """
#1 Загрузка датасета и вывод описания

from sklearn.datasets import fetch_openml
import pandas as pd

# Загрузка датасета
data = fetch_openml(data_id=<data_id>, as_frame=True)  # Замените <data_id> на ID вашего датасета

# Вывод текстового описания
print(data.DESCR)

# Разделение данных на X и y
X = data.data
y = data.target


#2 Статистическое описание данных

# Количественное описание данных
print(f"Число строк (объектов): {X.shape[0]}")
print(f"Число столбцов (признаков): {X.shape[1]}")

# Основная статистика по признакам
print(X.describe())

#3 Типы данных

print(X.dtypes)

# Проверка, что все признаки числовые. Если нет, удаляем нечисловые колонки.
X = X.select_dtypes(include=[int, float])

# Проверка типа целевой переменной
print(type(y))

#X = X.drop(columns=['theta1']) - на случай, если в колонке theta1 не числовые данные

#4 Проверка на пропущенные значения

# Проверка на пропущенные значения
print(X.isnull().sum())
print(y.isnull().sum())

# Заполнение пропусков медианными значениями, если есть
X = X.fillna(X.median())
y = y.fillna(y.median())

#5 Построение гистограммы целевой переменной
import matplotlib.pyplot as plt

# Гистограмма распределения целевой переменной
plt.hist(y, bins=20)
plt.title('Распределение целевой переменной')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.show()

# Анализ распределения
# (в зависимости от полученной гистограммы можно делать выводы)

#6 Обучение собственной модели линейной регрессии
# Для реализации собственной модели линейной регрессии используем градиентный спуск

import numpy as np

class LinearRegressionCustom:
    def init(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations

    def fit(self, X, y):
        self.m, self.n = X.shape
        self.theta = np.zeros(self.n + 1)
        X_b = np.c_[np.ones((self.m, 1)), X]  # добавляем bias
        self.X_b = X_b

        for i in range(self.n_iterations):
            gradients = 2/self.m * X_b.T.dot(X_b.dot(self.theta) - y)
            self.theta -= self.learning_rate * gradients

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # добавляем bias
        return X_b.dot(self.theta)

# Обучение модели
model = LinearRegressionCustom()
model.fit(X.values, y.values)

# Прогнозирование
predictions = model.predict(X.values)

# Построение графика
plt.scatter(X.iloc[:, 0], y, color="blue", label="Данные")
plt.plot(X.iloc[:, 0], predictions, color="red", label="Модель")
plt.legend()
plt.show()

# Уравнение гиперплоскости
print(f"Уравнение гиперплоскости: y = {model.theta[0]} + {model.theta[1:]} * X")

#7 Обучение модели с использованием sklearn

from sklearn.linear_model import LinearRegression

# Обучение модели sklearn
sklearn_model = LinearRegression()
sklearn_model.fit(X, y)

# Вывод уравнения гиперплоскости
print(f"Уравнение гиперплоскости sklearn: y = {sklearn_model.intercept_} + {sklearn_model.coef_} * X")

#8 Оценка моделей
from sklearn.metrics import r2_score, mean_squared_error

# Оценка собственной модели
r2_custom = r2_score(y, predictions)
mse_custom = mean_squared_error(y, predictions)

# Оценка модели sklearn
y_pred_sklearn = sklearn_model.predict(X)
r2_sklearn = r2_score(y, y_pred_sklearn)
mse_sklearn = mean_squared_error(y, y_pred_sklearn)

# Вывод метрик
print(f"Коэффициент детерминации (своя модель): {r2_custom}")
print(f"Среднеквадратичная ошибка (своя модель): {mse_custom}")
print(f"Коэффициент детерминации (sklearn): {r2_sklearn}")
print(f"Среднеквадратичная ошибка (sklearn): {mse_sklearn}")
"""


def ml2():
    return """ 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

x = pd.read_csv("0_x.csv", header=None)
y = pd.read_csv("0_y.csv", header=None)

y
x

print(x.shape)
print(y.shape)

# Задача 2
#Реализуем метод градиентного спуска в модели множественной регрессии
class MultipleRegression(object):
    def __init__(self):
        self.b = None
    def predict(self, x):
        return x @ self.b
    def MSE(self, x, y):
        return (((y - self.predict(x)).T @ (y - self.predict(x))) / (2 * x.shape[0])).values
    def MAE(self, x, y):
        return (abs(y - self.predict(x)).mean()).values
    def MAPE(self, x, y):
        return (abs((y - self.predict(x))/y).mean()).values
    def coefs(self):
        return self.b
    def fit(self, x, y, alpha = 0.1, accuracy = 0.1, max_steps = 10000, intercept = True):
        y = np.array(y).reshape(-1, 1)
        if intercept:
            x['intercept'] = 1
        self.b = np.zeros((x.shape[1], 1))
        steps, errors = [], []
        step = 0
        for _ in range(max_steps):
            dJ_b = x.T @ (self.predict(x) - y) / x.shape[0]
            self.b -= alpha * dJ_b
            new_error = self.MSE(x, y)
            step += 1
            steps.append(step)
            errors.append(new_error)
        return steps, errors
        
regr = MultipleRegression()
x_ = x.copy()
steps, errors = regr.fit(x, y, alpha = 0.01, accuracy = 0.01, max_steps = 1000, intercept = True)

yy = regr.predict(x)
plt.scatter(yy, y)
plt.plot(yy, yy, c='r')

print(regr.MAE(x, y))

print(regr.MSE(x, y))

regr.MAPE(x, y)

#Задачи 3, 5 и 6

#полиномиальная регрессия для всех признаков

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

poly_features = PolynomialFeatures(degree=10).fit_transform(x)

poly_reg_model = LinearRegression()
start_time = time.time()
poly_reg_model.fit(poly_features, y)
print('Время обучения: ', time.time() - start_time, 'сек.')
start_time

yy = poly_reg_model.predict(poly_features)
plt.scatter(yy, y)
plt.plot(yy, yy, c='r')

poly_reg_model.score(poly_features, y)

poly_reg_model.score(poly_features, y)

poly_reg_model.score(poly_features, y)

#полиномиальная регрессия для каждого признака


degrees = [2, 3, 10]
for column in x.columns:
  x_i = x[[column]]
  for degree in degrees:
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x_i)

    model = LinearRegression()
    model.fit(x_poly, y)
    y_pred = model.predict(x_poly)

    print(f'Pol regression {degree} for column: {column}')

    plt.scatter(x_i, y)
    plt.xlabel(f'column: {column}')
    plt.ylabel('Target Variable')

    sorted_indices = np.argsort(x_i.values[:, 0])
    x_sorted = x_i.values[sorted_indices]
    y_sorted_pred = y_pred[sorted_indices]

    plt.plot(x_sorted, y_sorted_pred, c= 'r',label=f'degree{degree}')
    plt.legend()
    plt.show()


from sklearn.metrics import r2_score, mean_squared_error

results = []
for i in range(11):
  start = time.time()

  poly = PolynomialFeatures(degree = i)
  X_poly = poly.fit_transform(x)
  model = LinearRegression()
  model.fit(X_poly, y)
  y_pred = model.predict(X_poly)

  duration = time.time() - start
  score = model.score(X_poly, y)
  mse = mean_squared_error(y_pred, y)

  results.append([i, duration, score, mse])

  plt.scatter(y_pred, y)
  plt.plot(y, y, c = 'r')
  plt.title(f"Degree {i}")
  plt.show()


df = pd.DataFrame(results, columns = ["Degree", "Duration", "Model_Score", "MSE"])
print(df)
"""


def ml3():
    return """

from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt

#№ 1
df = fetch_openml(name="")
df
df.DESCR #текстовое описание загруженного датасета
y = df.target
y #целевая переменная
X = df.data
X #остальные данные

#№ 2 и 3

X.describe()
X.info()
#### В датасете 8192 строк, 8 признаков (столбцов).
#### НИЧЕГО УДАЛЯТЬ НЕ НУЖНО, у всех признаков и целевой переменной числовой тип (float64)

#X = X.drop(columns=['theta1']) - на случай, если в колонке theta1 не числовые данные
y.describe()

#№ 4
X.isna().sum()
y.isna().sum()
пропущенных значений нет, нет необходимости заменять на медиану
#X['theta1'] = X['theta1'].fillna(X['theta1'].median()) - если в theta1 есть пропуски

#№ 5

import seaborn as sns
sns.histplot(y)

#наиболее часто целевая переменная принимает значения от 0,6 до 0,8. Она принадлежит к нормальному распределению

№ 6
import numpy as np

class Model(object):
    """
    Модель
    парной
    линейной
    регрессии
    """
    def __init__(self):
        self.b0 = 0
        self.b = []

    def predict(self, x):
        x=np.array(x)
        if x.ndim == 1:
            x = x.reshape(-1, 1)
        predictions = self.b0 + np.dot(x, self.b)
        return predictions

    def error(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        return np.sum((self.predict(X) - Y)**2) / (2 * len(X))

    def fit(self, X, Y, alpha=0.01, accuracy=0.01, max_steps=2000):
        self.steps, self.errors = [], []
        X = np.array(X)
        Y = np.array(Y).reshape(-1)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        self.b = np.zeros(X.shape[1])  
        step = 0
        self.steps = [0]
        self.errors = [self.error(X, Y)]
        for _ in range(max_steps):
            predictions = self.predict(X)
            dJ0 = np.sum(predictions - Y) / len(X)
            dJ = np.sum((predictions - Y)[:, None] * X, axis=0) / len(X)
            self.b0 -= alpha * dJ0
            self.b -= alpha * dJ
            new_err = self.error(X, Y)
            old_err = self.errors[-1]
            step += 1            
            if new_err < accuracy:
                break
            if new_err>old_err:
                alpha = alpha/2
                self.__init__()
            self.steps.append(step)
            self.errors.append(self.error(X,Y))
        return self.steps, self.errors
    
newmodel=Model()
steps, errors = newmodel.fit(X, y)
print("Коэффициенты:", newmodel.b0,newmodel.b)
    
xpred=newmodel.predict(X)
plt.plot(xpred,xpred,'r')
plt.scatter(xpred,y)
    
plt.plot(steps, errors, 'g')
    
выведем уравнение гиперплоскости:
y=0,717-0,041x1
-0,0252x2
-0,154x3
-0,0254x4
+0,0714x5
-0,0408x6
-0,0405x7
+0,0207x8
    
#№7
from sklearn.linear_model import LinearRegression
regr_sk = LinearRegression()
regr_sk.fit(X, y)
regr_sk.coef_
regr_sk.intercept_

выведем уравнение гиперплоскости:
y=0,717-0,041x1
-0,0252x2
-0,154x3
-0,0254x4
+0,0714x5
-0,0408x6
-0,0405x7
+0,0207x8
    
    
уравнения схожи
from sklearn.metrics import r2_score, mean_squared_error
для модели sk_learn
r2_score(y, regr_sk.predict(X)) 
mean_squared_error(y, regr_sk.predict(X))
для нашей модели
r2_score(y, newmodel.predict(X))
mean_squared_error(y, newmodel.predict(X))
"""
def ml4():
    return """
    
#1
from sklearn.datasets import fetch_openml
import pandas as pd

# Загрузка данных
data = fetch_openml(name='LEV', as_frame=True)

# Отображение описания данных (если нужно)
print(data.DESCR)

# Обозначаем X и y
X = data.data
y = data.target

# Выводим первые 5 строк признаков (X) и целевой переменной (y)
print("Первые строки данных X:")
print(X.head())

print("Первые строки целевой переменной y:")
print(y.head())

#2
# Количество строк и столбцов
print("Количество строк и столбцов:")
print(X.shape)

# Основная статистика по признакам
print("\nСтатистика по признакам:")
print(X.describe())

# Статистика по целевой переменной
print("\nСтатистика по целевой переменной:")
print(y.describe())

#3
# Проверяем типы данных признаков
print("Типы данных признаков:")
print(X.dtypes)

# Проверяем тип данных целевой переменной
print("\nТип данных целевой переменной:")
print(y.dtypes)

#4

# Проверяем на пропущенные значения в признаках
print("Пропущенные значения в признаках:")
print(X.isnull().sum())

# Проверяем на пропущенные значения в целевой переменной
print("\nПропущенные значения в целевой переменной:")
print(y.isnull().sum())

#5
import matplotlib.pyplot as plt

# Построение гистограммы для целевой переменной
plt.figure(figsize=(10, 6))
plt.hist(y, bins=10, edgecolor='black', alpha=0.7)
plt.title('Гистограмма распределения целевой переменной (Итоговая оценка)')
plt.xlabel('Итоговая оценка')
plt.ylabel('Частота')
plt.grid(axis='y', alpha=0.75)
plt.show()

import seaborn as sns

sns.histplot(y)

#6
import numpy as np

# Добавляем столбец единиц к X для свободного члена
X_b = np.c_[np.ones((X.shape[0], 1)), X]  # добавляем x0 = 1

# Вычисляем коэффициенты линейной регрессии
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

# Выводим уравнение полученной гиперплоскости
print("Коэффициенты линейной регрессии:")
print(theta_best)

# Предсказания модели
y_pred = X_b.dot(theta_best)

# График предсказанных значений против фактических значений
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')  # линия y=x
plt.title('Сравнение фактических и предсказанных значений')
plt.xlabel('Фактические значения')
plt.ylabel('Предсказанные значения')
plt.grid()
plt.show()

from sklearn.linear_model import LinearRegression

# Создаем экземпляр модели
model = LinearRegression()

# Обучаем модель
model.fit(X, y)

# Получаем коэффициенты
intercept = model.intercept_  # свободный член
coefficients = model.coef_     # коэффициенты признаков

# Выводим уравнение гиперплоскости
print("Уравнение полученной гиперплоскости:")
print("y =", intercept, "+", " + ".join(f"{coef} * X{i+1}" for i, coef in enumerate(coefficients)))

# Выводим уравнение полученной гиперплоскости
print("Коэффициенты линейной регрессии:")
print(theta_best)

#8

from sklearn.metrics import mean_squared_error, r2_score

# Оценка для самописной модели
y_pred_custom = X_b.dot(theta_best)
r2_custom = r2_score(y, y_pred_custom)
mse_custom = mean_squared_error(y, y_pred_custom)

print("Оценка самописной модели:")
print(f"Коэффициент детерминации (R^2): {r2_custom:.4f}")
print(f"Средняя квадратическая ошибка (MSE): {mse_custom:.4f}")

# Оценка для модели из sklearn
y_pred_sklearn = model.predict(X)
r2_sklearn = r2_score(y, y_pred_sklearn)
mse_sklearn = mean_squared_error(y, y_pred_sklearn)

print("\nОценка модели sklearn:")
print(f"Коэффициент детерминации (R^2): {r2_sklearn:.4f}")
print(f"Средняя квадратическая ошибка (MSE): {mse_sklearn:.4f}")
"""

def ml5():
    return """

from sklearn.datasets import fetch_openml
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#Открываем файл
data = fetch_openml(name='stock')
data

#информация о датасете
print(data.DESCR)

#присваивание данных
X = data.data
X

#присваивание целевой переменной
y = data.target
y

#2
f'Число объектов - {X.shape[0]}'

f"Число столбцов (признаков): {X.shape[1]}"

#статистика по Х
X.describe()

#статистика по у
y.describe()

#3

#вывод типов данных
print(X.dtypes)

#проверка, что все признаки числовые
X = X.select_dtypes(include=[int, float])

#проверка типа целевой переменной
print(type(y))

#4

#проверка на пропущенные значения
print(X.isnull().sum())
print(y.isnull().sum())

#заполнение пропусков медианными значениями, если есть
X = X.fillna(X.median())
y = y.fillna(y.median())

#5
#построение гистограммы с помощью библиотеки seaborn
sns.histplot(y)

#построение гистограммы при помощи matplotlib
plt.hist(y)
plt.show()

#6

#модель множественной линейной регрессии
class MultipleRegression(object):
    def __init__(self):
        self.b = None
        self.steps, self.errors = [], []

    def predict(self, x):
        return x @ self.b

    def MSE(self, x, y):
        return (((y - self.predict(x)).T @ (y - self.predict(x))) / (2 * x.shape[0])).values

    def MAE(self, x, y):
        return (abs(y - self.predict(x)).mean()).values

    def MAPE(self, x, y):
        return (abs((y - self.predict(x))/y).mean()).values

    def coefs(self):
        return self.b

    def fit(self, x, y, alpha = 0.1, accuracy = 0.001, max_steps = 10000, intercept = True):
        y = np.array(y).reshape(-1, 1)

        if intercept:
            x['intercept'] = 1

        self.b = np.zeros((x.shape[1], 1))
        step = 0

        for _ in range(max_steps):
            dJ_b = x.T @ (self.predict(x) - y) / x.shape[0]
            self.b -= alpha * dJ_b
            new_error = self.MSE(x, y)
            step += 1
            self.steps.append(step)
            self.errors.append(new_error)

        return self.steps, self.errors


#нормализуем таблицу с помощью MinMaxScaler
scaler = MinMaxScaler()
X_ = scaler.fit_transform(X)
X_

X_df = pd.DataFrame(X_, columns=X.columns)
X_df

#обучение модели
model = MultipleRegression()
model.fit(X_df, y)

model.b

#построим график регрессии
yy = model.predict(X_df)
plt.scatter(yy, y)
plt.plot(yy, yy, c='r')

#7
#обучение модели с помощью sklearn
sklearn_model = LinearRegression()
sklearn_model.fit(X.values, y.values)

coefs = sklearn_model.coef_
print(f'уравнение имеет вид = {coefs[0]} + {coefs[1]} * x1 + {coefs[2]} * x2 + {coefs[3]} * x3 + {coefs[4]} * x4 + {coefs[5]} * x5 + {coefs[6]} * x6 + {coefs[7]} * x7 + {coefs[8]} * x8')

#8
# Оценка модели sklearn
y_pred_sklearn = sklearn_model.predict(X.values)
r2_sklearn = r2_score(y, y_pred_sklearn)
mse_sklearn = mean_squared_error(y, y_pred_sklearn)
r2_sklearn, mse_sklearn

f"Коэффициент детерминации (sklearn): {r2_sklearn}"
f"Среднеквадратичная ошибка (sklearn): {mse_sklearn}"
predictions = model.predict(X_df)

# Оценка собственной модели
r2_custom = r2_score(y, predictions)
mse_custom = mean_squared_error(y, predictions)
r2_custom, mse_custom
f"Коэффициент детерминации (своя модель): {r2_custom}"
f"Среднеквадратичная ошибка (своя модель): {mse_custom}"
"""