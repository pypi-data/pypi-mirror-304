from g4f.client import Client

def r(req, model_id):
    model_dict ={
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt - 4o",
        5: "llama-3.1-70b",

    }

    model = model_dict.get(model_id, "gpt-4")
    client = Client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": req}],
    )
    print(response.choices[0].message.content)


def info():
    print("""
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt-4o",
        5: "llama-3.1-70b"
    """)


def f():
    text = """
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Данные выборки
data = [
    -143.531, -159.217, -141.105, np.nan, -164.107, -135.826, -155.828, np.nan, np.nan,
    -167.145, -218.919, -118.772, -88.716, -152.445, -183.226, -145.505, np.nan,
    -128.052, -159.136, np.nan, -127.464, -190.052, -201.962, -130.642, -95.26,
    -166.79, np.nan, np.nan, -156.917, np.nan, -189.694, -156.208, -161.634,
    -176.773, -159.338, -174.144, -148.573, -194.651, -145.698, -138.323,
    -183.823, -196.663, -132.26, -187.931, -131.537, -144.515, -144.973,
    -142.058, -139.963, -158.874, -184.942, -140.566, -135.685, -179.946,
    -139.99, -164.118, -152.163, -144.884, -126.065, np.nan, -161.675,
    -136.173, np.nan, -173.79, -112.299, -171.716, -169.328, np.nan,
    -156.466, -149.264, -154.392, -155.071, np.nan, -180.257, -137.577,
    -206.943, np.nan, -190.356, -143.85, -202.789, -130.981, -101.133,
    np.nan, -138.014, -140.387, -131.435, -122.716, np.nan, -155.816,
    -153.009, -151.528, -181.329, -180.411, -163.659, np.nan, -121.294,
    -165.012, -263.161625, -200.233, -138.825, -144.498, -177.739,
    -169.965, -173.423, -137.268, np.nan, -126.703, -167.115, -109.577,
    -175.169, -135.576, -172.54, -176.418, -155.838, -164.948, -193.231,
    -151.285, -126.651, -190.63, -170.938, -152.317, -164.072, -179.517,
    -161.974, -141.848, np.nan, -126.301, -154.503, -136.43, -145.411,
    -197.76, np.nan, -190.654, -126.403, -130.615, -164.15, -100.499,
    -178.188, -188.409, -199.688, -146.578, -121.394, -141.97, -151.104,
    np.nan, np.nan, -159.405, -169.622, -117.83, -117.443, -118.33,
    -125.984, 31.548375, -138.904, -152.499, -178.32, -176.598, -176.17,
    -110.085, -154.55, -169.436, -120.843, -185.529, np.nan, np.nan,
    -138.545, -136.804, -123.425, -177.84, -147.431, -133.27, -300.000375,
    -128.37, -153.994, -157.987, -217.636, -131.263, -160.715, -153.059,
    -167.264, -149.294, -143.658, -119.075, -115.729, -127.164, -142.578,
    -151.037, -144.635, -156.024, -164.215, -187.842, -147.622, -170.702,
    -173.255, -171.107, -119.772, -176.164, np.nan, -108.646, -121.072,
    -38.618, -115.681, np.nan, -164.143, -161.775, -108.76, -177.767,
    -206.968, -134.229, -138.894, -135.354, -154.621, -137.594, -154.652,
    -131.12, -120.825, -117.748, -151.096, -104.158, -224.645, np.nan,
    -133.238, -154.896, -135.61, np.nan, -126.297, -22.979, -158.358,
    -200.103, np.nan, -110.636, -165.234, np.nan, -176.802, -202.474,
    -135.66, -185.149, -99.819, -119.587, np.nan, -183.672, np.nan,
    np.nan, -170.601, -161.892, -135.019, np.nan, -188.308, np.nan,
    -95.595, -127.755, np.nan, -129.2, -175.151, -159.291, -110.203,
    -128.467, -162.085, -168.209, -183.638, np.nan, -150.976, -155.411,
    -185.619, -154.036, -120.735, np.nan, -169.178, -146.557, -168.638,
    -107.389, np.nan, -216.8, -168.799, -179.01, -88.76, np.nan,
    -177.859, np.nan, -134.225, -180.628, -169.829, -142.247, -139.941,
    -151.737, -156.984, -154.668, -189.575, -184.939, -144.368
]

# Преобразование в DataFrame
df = pd.DataFrame(data, columns=['A'])

# 1. Количество пропущенных значений
missing_values_count = df['A'].isna().sum()
print(f"Количество пропущенных значений: {missing_values_count}")

# 2. Очищенная выборка
cleaned_data = df['A'].dropna()

# 3. Объем очищенной выборки
cleaned_size = cleaned_data.size
print(f"Объем очищенной выборки: {cleaned_size}")

# 4. Среднее значение
mean_value = cleaned_data.mean()
print(f"Среднее значение: {mean_value}")

# 5. Стандартное отклонение (исправленное)
std_dev = cleaned_data.std(ddof=1)
print(f"Стандартное отклонение: {std_dev}")

# 6. Несмещенная дисперсия
variance = cleaned_data.var(ddof=1)
print(f"Несмещенная дисперсия: {variance}")


# 7. Первая квартиль
first_quartile = cleaned_data.quantile(0.25)
print(f"Первая квартиль: {first_quartile}")

# 8. Третья квартиль
third_quartile = cleaned_data.quantile(0.75)
print(f"Третья квартиль: {third_quartile}")

# 9. Медиана
median_value = cleaned_data.median()
print(f"Медиана: {median_value}")

# 10. Максимальное значение
max_value = cleaned_data.max()
print(f"Максимальное значение: {max_value}")

# 11. Минимальное значение
min_value = cleaned_data.min()
print(f"Минимальное значение: {min_value}")

# 12. Размах выборки
range_value = max_value - min_value
print(f"Размах выборки: {range_value}")

# 13. Эксцесс
kurtosis = stats.kurtosis(cleaned_data)
print(f"Эксцесс: {kurtosis}")

# 14. Коэффициент асимметрии
skewness = stats.skew(cleaned_data)
print(f"Коэффициент асимметрии: {skewness}")

# 15. Ошибка выборки
standard_error = std_dev / np.sqrt(cleaned_size)
print(f"Ошибка выборки: {standard_error}")

# 16. Доверительный интервал для E(X)
confidence_level = 0.95
z_score = stats.norm.ppf((1 + confidence_level) / 2)
margin_of_error = z_score * standard_error
confidence_interval_mean = (mean_value - margin_of_error, mean_value + margin_of_error)
print(f"0.95-доверительный интервал для E(X): {confidence_interval_mean}")

# 17. Доверительный интервал для Var(X)
chi2_lower = stats.chi2.ppf((1 - confidence_level) / 2, cleaned_size - 1)
chi2_upper = stats.chi2.ppf((1 + confidence_level) / 2, cleaned_size - 1)
confidence_interval_variance = ((cleaned_size - 1) * variance / chi2_upper,
                                  (cleaned_size - 1) * variance / chi2_lower)
print(f"0.95-доверительный интервал для Var(X): {confidence_interval_variance}")

# 18. Количество выбросов ниже нормы
lower_bound = first_quartile - 1.5 * (third_quartile - first_quartile)
outliers_below = cleaned_data[cleaned_data < lower_bound].count()
print(f"Количество выбросов ниже нормы: {outliers_below}")

# 19. Количество выбросов выше нормы
upper_bound = third_quartile + 1.5 * (third_quartile - first_quartile)
outliers_above = cleaned_data[cleaned_data > upper_bound].count()
print(f"Количество выбросов выше нормы: {outliers_above}")

# 20. Построение гистограммы и диаграммы "ящик с усиками"
plt.figure(figsize=(12, 6))

# Гистограмма
plt.subplot(1, 2, 1)
sns.histplot(cleaned_data, bins=30, kde=True)
plt.title('Гистограмма')
plt.xlabel('Значения')
plt.ylabel('Частота')

# Диаграмма "ящик с усиками"
plt.subplot(1, 2, 2)
sns.boxplot(x=cleaned_data)
plt.title('Диаграмма "ящик с усиками"')

plt.tight_layout()
plt.show()
    """
    print(text)