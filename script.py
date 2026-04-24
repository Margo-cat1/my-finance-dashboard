import plotly.graph_objects as go

# Данные твоего дашборда
labels = ['ROI', 'Sol2', 'Sol3', 'Liquidity']
values = [0.25, 5.0, 2.1, 1.8]  # Твои показатели в долях (25%, 500% и т.д.)

# Создаем красивую столбчатую диаграмму
fig = go.Figure(data=[go.Bar(
    x=labels,
    y=values,
    marker_color=['#2ecc71', '#3498db', '#9b59b6', '#e67e22'] # Цвета для стиля
)])

# Настраиваем внешний вид
fig.update_layout(
    title='Финансовые показатели: Визуализация 2.0',
    xaxis_title='Показатель',
    yaxis_title='Значение',
    template='plotly_dark' # Темная тема, как в PyCharm
)

# Запуск в браузере
fig.show()