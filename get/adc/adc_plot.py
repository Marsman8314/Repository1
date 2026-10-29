import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.title("Зависимость напряжения на выходе ЦАП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, time[-1] if time else 1)
    plt.ylim(0, max_voltage)
    plt.grid(True)
    plt.show()


def plot_sampling_period_hist(time):
    # Список промежутков времени, потраченного на каждое измерение
    sampling_periods = []

    # Разницы между соседними моментами времени
    for i in range(1, len(time)):
        sampling_periods.append(time[i] - time[i - 1])

    # Окно для отображения графика
    plt.figure(figsize=(10, 6))

    # Гистограмма периодов измерений
    plt.hist(sampling_periods)
    # Название графика и осей
    plt.title("Распределение количества измерений по их продолжительности")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    # Границы по оси X
    plt.xlim(0, 0.06)

    # Сетка
    plt.grid(True)

    # Отображение гистограммы
    plt.show()