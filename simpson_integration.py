import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class SimpsonIntegration:
    def __init__(self, root):
        self.root = root
        self.root.title("Численное интегрирование методом Симпсона")
        self.root.geometry("1200x900")

        # Создание фреймов
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.graph_frame = ttk.Frame(root, padding="10")
        self.graph_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.result_frame = ttk.Frame(root, padding="10")
        self.result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Параметры из варианта
        ttk.Label(self.control_frame, text="Функция: f(x) = sin²(x)", font=('Arial', 12, 'bold')).grid(row=0, column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=5)

        ttk.Label(self.control_frame, text="Нижний предел a:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.a_entry = ttk.Entry(self.control_frame, width=15)
        self.a_entry.insert(0, str(-0.5 * np.pi))
        self.a_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.control_frame, text="Верхний предел b:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.b_entry = ttk.Entry(self.control_frame, width=15)
        self.b_entry.insert(0, str(0.5 * np.pi))
        self.b_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.control_frame, text="Точность ε:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.eps_entry = ttk.Entry(self.control_frame, width=15)
        self.eps_entry.insert(0, "0.001")
        self.eps_entry.grid(row=3, column=1, pady=5)

        ttk.Label(self.control_frame, text="Начальное число разбиений n:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.n_entry = ttk.Entry(self.control_frame, width=15)
        self.n_entry.insert(0, "4")
        self.n_entry.grid(row=4, column=1, pady=5)

        # Кнопка вычисления
        self.calc_button = ttk.Button(self.control_frame, text="Вычислить", command=self.calculate)
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=15)

        # Поле для вывода результатов
        self.result_text = tk.Text(self.result_frame, height=10, width=100, font=('Courier', 10))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar для текстового поля
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Настройка весов для растягивания
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

    def f(self, x):
        """Функция для интегрирования: f(x) = sin²(x)"""
        return np.sin(x) ** 2

    def simpson_method(self, a, b, n):
        """Метод Симпсона для вычисления определенного интеграла"""
        if n % 2 != 0:
            n += 1  # n должно быть четным

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = self.f(x)

        # Формула Симпсона
        integral = y[0] + y[-1]
        integral += 4 * np.sum(y[1:-1:2])  # Нечетные индексы
        integral += 2 * np.sum(y[2:-1:2])  # Четные индексы
        integral *= h / 3

        return integral, x, y

    def runge_estimation(self, I_n, I_2n):
        """Оценка погрешности по методу Рунге"""
        # Для метода Симпсона порядок точности p = 4
        return abs(I_2n - I_n) / 15

    def calculate(self):
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            eps = float(self.eps_entry.get())
            n = int(self.n_entry.get())

            # Очистка результатов
            self.result_text.delete(1.0, tk.END)

            # Заголовок
            self.result_text.insert(tk.END, "=" * 90 + "\n")
            self.result_text.insert(tk.END, "ЧИСЛЕННОЕ ИНТЕГРИРОВАНИЕ МЕТОДОМ СИМПСОНА\n")
            self.result_text.insert(tk.END, "=" * 90 + "\n\n")

            self.result_text.insert(tk.END, f"Функция: f(x) = sin²(x)\n")
            self.result_text.insert(tk.END, f"Интервал: [{a:.4f}, {b:.4f}]\n")
            self.result_text.insert(tk.END, f"Требуемая точность: ε = {eps}\n\n")

            # Итерационный процесс
            self.result_text.insert(tk.END, "-" * 90 + "\n")
            self.result_text.insert(tk.END,
                                    f"{'Итерация':<10} {'n':<10} {'I(n)':<20} {'Оценка Рунге':<20} {'Достигнута?':<15}\n")
            self.result_text.insert(tk.END, "-" * 90 + "\n")

            I_n, x_n, y_n = self.simpson_method(a, b, n)
            iteration = 1

            self.result_text.insert(tk.END, f"{iteration:<10} {n:<10} {I_n:<20.10f} {'—':<20} {'—':<15}\n")

            while True:
                n_new = 2 * n
                I_2n, x_2n, y_2n = self.simpson_method(a, b, n_new)
                runge_error = self.runge_estimation(I_n, I_2n)

                iteration += 1
                achieved = "Да" if runge_error < eps else "Нет"

                self.result_text.insert(tk.END,
                                        f"{iteration:<10} {n_new:<10} {I_2n:<20.10f} {runge_error:<20.10f} {achieved:<15}\n")

                if runge_error < eps:
                    final_n = n_new
                    final_I = I_2n
                    final_x = x_2n
                    final_y = y_2n
                    final_error = runge_error
                    break

                I_n = I_2n
                n = n_new
                x_n = x_2n
                y_n = y_2n

                if n > 10000:  # Защита от бесконечного цикла
                    self.result_text.insert(tk.END, "\nПревышено максимальное число разбиений!\n")
                    return

            # Итоговые результаты
            self.result_text.insert(tk.END, "-" * 90 + "\n\n")
            self.result_text.insert(tk.END, "РЕЗУЛЬТАТЫ:\n")
            self.result_text.insert(tk.END, f"Значение интеграла I = {final_I:.10f}\n")
            self.result_text.insert(tk.END, f"Число разбиений n = {final_n}\n")
            self.result_text.insert(tk.END, f"Оценка погрешности (Рунге) = {final_error:.10e}\n")

            # Аналитическое значение для sin²(x)
            # ∫sin²(x)dx = x/2 - sin(2x)/4 + C
            analytical = (b / 2 - np.sin(2 * b) / 4) - (a / 2 - np.sin(2 * a) / 4)
            self.result_text.insert(tk.END, f"Аналитическое значение = {analytical:.10f}\n")
            self.result_text.insert(tk.END, f"Абсолютная погрешность = {abs(final_I - analytical):.10e}\n")

            # Построение графиков
            self.plot_results(a, b, final_x, final_y, final_I)

        except ValueError as e:
            self.result_text.insert(tk.END, f"Ошибка ввода данных: {e}\n")

    def plot_results(self, a, b, x_points, y_points, integral_value):
        """Построение графиков функции и сетки интегрирования"""
        # Удаляем старый график если есть
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(10, 5))

        # График функции
        ax1 = fig.add_subplot(121)
        x_smooth = np.linspace(a, b, 1000)
        y_smooth = self.f(x_smooth)

        ax1.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x) = sin²(x)')
        ax1.fill_between(x_smooth, 0, y_smooth, alpha=0.3)
        ax1.plot(x_points, y_points, 'ro', markersize=4, label=f'Узлы (n={len(x_points) - 1})')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.set_title('График функции и узлы интегрирования')
        ax1.legend()

        # График сетки интегрирования
        ax2 = fig.add_subplot(122)
        ax2.bar(x_points[:-1], y_points[:-1], width=(x_points[1] - x_points[0]),
                align='edge', alpha=0.5, edgecolor='black', label='Сетка Симпсона')
        ax2.plot(x_smooth, y_smooth, 'r-', linewidth=2, label='f(x)')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)')
        ax2.set_title(f'Сетка интегрирования\nI ≈ {integral_value:.6f}')
        ax2.legend()

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpsonIntegration(root)
    root.mainloop()