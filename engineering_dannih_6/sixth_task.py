import pandas as pd
import os
import json
import matplotlib.pyplot as plt

# Создаю директорию для сохранения графиков
output_dir = "./results" # путь к папке с графиками
os.makedirs(output_dir, exist_ok=True)

# 1. Загружаю данные
file_path = "./movies.csv" # путь до датасета
df = pd.read_csv(
    file_path,
    low_memory=False, # отключение оптимизации памятри при чтении файла для избежания ошибок с типами данных 
    converters={ #  преобразование значений
        'votes': lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.replace(',', '').isdigit() else None, # здесь убираю запятые для значений в этом столбце
        'gross_income': lambda x: float(x.replace('$', '').replace('M', '').replace(',', '').strip()) if isinstance(x, str) and x not in ['0', ''] else None # здесь убираю символы $ и M 
    }
)

# 2. Анализ данных
# a. Считаю размер файла на диске
file_size = os.path.getsize(file_path) / (1024 * 1024)  # считается в МБ

# b. Считаю размер данных в памяти
memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # считается в МБ

# c. Анализ колонок
columns_stats = []
for col in df.columns:
    col_mem = df[col].memory_usage(deep=True) / (1024 * 1024)  # считается в МБ (здесь вычисляется объем памяти, занимаемый столбцом)
    columns_stats.append({ # добавляю информацию о столбце
        "column": col,
        "memory_mb": col_mem,
        "memory_share_percent": (col_mem / memory_usage) * 100,
        "dtype": str(df[col].dtype)  # здесь преобразовываю dtype в строку
    })
columns_stats = sorted(columns_stats, key=lambda x: x["memory_mb"], reverse=True) # сортировка списка по объму пямати от большего к меньшему 

# Сохранение эту статистику до её оптимизации
with open("columns_stats_before_optimization.json", "w") as f:
    json.dump(columns_stats, f, indent=4)

# Блок с оптимизацией 
# 4. Преобразование object-колонок - выбрал все столбцы object
for col in df.select_dtypes(include='object').columns:
    if df[col].nunique() / len(df) < 0.5: # если уникальных значений в столбце меньше 50% от общего числа строк, преобразую его в category.
        df[col] = df[col].astype('category')

# 5. Оптимизация int-колонок - преобразование int в меньший тип 
for col in df.select_dtypes(include='int').columns:
    df[col] = pd.to_numeric(df[col], downcast='integer') 

# 6. Оптимизация float-колонок - преобразование float в меньший тип
for col in df.select_dtypes(include='float').columns:
    df[col] = pd.to_numeric(df[col], downcast='float')

# 7. Повторный анализ колонок уже после оптимизации
memory_usage_after = df.memory_usage(deep=True).sum() / (1024 * 1024)  # считается в МБ
columns_stats_after = []
for col in df.columns:
    col_mem = df[col].memory_usage(deep=True) / (1024 * 1024)  # считается в МБ (здесь вычисляется объем памяти, занимаемый столбцом)
    columns_stats_after.append({ # добавляю информацию о столбце
        "column": col,
        "memory_mb": col_mem,
        "memory_share_percent": (col_mem / memory_usage_after) * 100,
        "dtype": str(df[col].dtype)  # Преобразование dtype в строку
    })
columns_stats_after = sorted(columns_stats_after, key=lambda x: x["memory_mb"], reverse=True) # сортировка списка по объму пямати от большего к меньшему 

with open("columns_stats_after_optimization.json", "w") as f: 
    json.dump(columns_stats_after, f, indent=4)

# 8. Работа с поднабором данных
selected_columns = df.columns[:10]  # выбираю первые 10 колонок
chunk_size = 1000 # читаем файл по частям для экономии памяти
subset_file_path = "./subset_movies.csv"

if os.path.exists(subset_file_path):
    os.remove(subset_file_path)  # Удалить файл, если он существует

with pd.read_csv(file_path, usecols=selected_columns, chunksize=chunk_size) as reader:
    for chunk in reader:
        chunk.to_csv(subset_file_path, mode='a', header=not os.path.exists(subset_file_path), index=False)

# 9. Построение графиков
# Загрузка поднабора данных
df_subset = pd.read_csv(
    subset_file_path,
    low_memory=False,
    converters={
        'votes': lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.replace(',', '').isdigit() else None,
        'rating': lambda x: float(x) if isinstance(x, str) and x.replace('.', '').isdigit() else None
    },
    na_values=['n/a', 'na', '--', '']
)

# Преобразование столбцов в числовые типы
df_subset['rating'] = pd.to_numeric(df_subset['rating'], errors='coerce')
df_subset['votes'] = pd.to_numeric(df_subset['votes'], errors='coerce')

# Удаление строк с пропущенными значениями
df_subset = df_subset.dropna(subset=['rating', 'votes'])

# Линейный график - показывает количество фильмов по годам
plt.plot(df_subset['year'].value_counts().sort_index())
plt.title('Количество фильмов по годам')
plt.xlabel('Год')
plt.ylabel('Количество фильмов')
plt.savefig(f'{output_dir}/line_chart_years.png')
plt.close()

# Столбчатая диаграмма - топ-10 жанров по количеству фильмов
plt.bar(df_subset['genre'].value_counts().index[:10], df_subset['genre'].value_counts().values[:10])
plt.title('Топ 10 жанров')
plt.xlabel('Жанры')
plt.ylabel('Количество фильмов')
plt.xticks(rotation=45)
plt.savefig(f'{output_dir}/bar_chart_genres.png')
plt.close()

# Круговая диаграмма - распределение сертификатов
df_subset['certificate'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Сертификаты фильмов')
plt.ylabel('')
plt.savefig(f'{output_dir}/pie_chart_certificates.png')
plt.close()

# Корреляция - матрица коррелаций между числовыми столбцами
plt.matshow(df_subset.corr(numeric_only=True))
plt.title('Корреляция данных')
plt.colorbar()
plt.savefig(f'{output_dir}/correlation_matrix.png')
plt.close()

# Построение scatter plot - зависимость между рейтингом и кол-ом голосов
plt.scatter(df_subset['rating'], df_subset['votes'])
plt.title('Рейтинг vs Количество голосов')
plt.xlabel('Рейтинг')
plt.ylabel('Голоса')
plt.savefig(f'{output_dir}/scatter_plot_rating_votes.png')
plt.close()
