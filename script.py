import pandas as pd
table1 = pd.read_excel('Курсач1.xlsx')
table2 = pd.read_excel('Курсач2.xlsx')
def find_durability(df, stress, ratio):
    mask = (df['Напряжение растяжения σ_p (МПа)'] == stress) & (df['Отношение D1/δ'] == ratio)
    result = df.loc[mask, 'Долговечность t_q0 (ч)']
    return result.values[0] if not result.empty else None
def find_Ci(df, opoq, u):
    mask = (df['σp/σq'] == opoq) & (df['u'] == u)
    result = df.loc[mask, 'CH']
    return result.values[0] if not result.empty else None
class durability_equation:
    def __init__(self):
        self.LP = 0
        self.RP = 0
        self.m = 6
        self.Ci = 0
        self.Cp = 0
        self.sigma_max = 0
        self.sigma_p = 0
        self.sigma_ce = 0
        self.tch = 0
        self.tch0 = 0
        self.sigma_N = 7.5
        self.Nc0 = 10**7

    def calculate_isequal(self):
        return abs(self.RP-self.LP)/self.RP < 0.15
    def calculate_LP(self):
        self.LP = self.sigma_max**self.m * 3600 * self.i * self.zsh * self.tch
    def calculate_sigma_max(self):
        self.sigma_max = self.sigma_p + self.sigma_i
    def calculate_sigma_p(self):
        self.sigma_p = self.sigma_0 + self.F/(2*self.b * self.delta) + self.sigma_ce
    def calculate_sigma_ce(self):
        self.sigma_ce = self.E_i * self.delta / self.D1
    def calculate_tch0(self):
        if self.case == 0:
            self.tch0 = 2.46 * 10**8 / (self.sigma_max**6)
        else:
            self.tch0 = find_durability(table1, round(self.sigma_p, 1), round(self.D1/self.delta, 0))
            if self.tch0 is None:
                print('Не удается найти значение tch0')
                self.tch0 = 2.46 * 10 ** 8 / (self.sigma_max ** 6)
            else:
                print('Значение tch0 в таблице найдено!', self.tch0)
    def calculate_tch(self):
        self.tch = (self.tch0 / self.i) * self.Ci * self.Cp
    def calculate_Ci(self):
        if self.case1 == 0:
            self.Ci = 2/(1+((self.sigma_p + self.sigma_i/self.u)/self.sigma_max)**6)
        else:
            self.Ci = find_Ci(table2, round(self.sigma_p/self.sigma_i, 1), self.u)
            if self.Ci is None:
                print('Не удается найти значение Ci')
                self.Ci = 2 / (1 + ((self.sigma_p + self.sigma_i / self.u) / self.sigma_max) ** 6)
            else:
                print('Значение Ci в таблице найдено!', self.Ci)
    def calculate_Cp(self):
        self.Cp = self.i1 / ((self.sigma_x/self.sigma_max)**6 * self.ix * self.divex)
    def calculate_RP(self):
        self.RP = self.sigma_N ** self.m * self.Nc0

    def calculate_all(self):
        self.calculate_sigma_ce()
        self.calculate_sigma_p()
        self.calculate_sigma_max()
        self.calculate_Ci()
        self.calculate_Cp()
        self.calculate_tch0()
        self.calculate_tch()
        self.calculate_LP()
        self.calculate_RP()

    def load_user_data(self):
        print("=" * 60)
        print("ВВОД ДАННЫХ ДЛЯ РАСЧЕТА ДОЛГОВЕЧНОСТИ РЕМНЯ")
        print("=" * 60)

        print("\n📏 ГЕОМЕТРИЧЕСКИЕ ПАРАМЕТРЫ:")
        self.delta = float(input("Толщина ремня, δ (мм): "))
        self.D1 = float(input("Диаметр малого шкива, D₁ (мм): "))
        self.b = float(input("Ширина ремня, b (мм): "))

        print("\n⚙️ МЕХАНИЧЕСКИЕ ПАРАМЕТРЫ:")
        self.E_i = float(input("Модуль упругости при изгибе, E_i (МПа): "))
        self.sigma_0 = float(input("Начальное напряжение растяжения, σ₀ (МПа): "))
        self.F = float(input("Сила тяги, F (Н): "))

        print("\n🔄 КИНЕМАТИЧЕСКИЕ ПАРАМЕТРЫ:")
        self.i = float(input("Число пробегов ремня в секунду, i (1/сек): "))
        self.zsh = int(input("Число шкивов в передаче, z_sh: "))
        self.u = float(input("Передаточное число, u: "))

        print("\n🎯 РЕЖИМЫ РАБОТЫ И КОЭФФИЦИЕНТЫ:")
        print("Способ определения долговечности:")
        print("  0 - по формуле, 1 - по таблице")
        self.case = int(input("case: "))

        print("Способ определения коэффициента Cи:")
        print("  0 - по формуле, 1 - по таблице")
        self.case1 = int(input("case1: "))

        print("\n📊 ПАРАМЕТРЫ ДЛЯ РАСЧЕТА КОЭФФИЦИЕНТОВ:")
        self.sigma_i = float(input("Напряжение изгиба, σ_i (МПа): "))
        self.i1 = float(input("Число пробегов при максимальном напряжении, i1 (1/сек): "))

        print("\n🔧 ПАРАМЕТРЫ ДЛЯ РАСЧЕТА Cp (переменный режим):")
        self.sigma_x = float(input("Напряжение дополнительного режима, σ_x (МПа): "))
        self.ix = float(input("Число пробегов при σ_x, i_x (1/сек): "))
        self.divex = float(input("Доля времени работы на режиме σ_x, 1/e_x: "))

        print("\n" + "=" * 60)
        print("ВВОД ДАННЫХ ЗАВЕРШЕН!")
        print("=" * 60)

    def print_detailed_calculation(self):

        print("\nДЕТАЛЬНЫЙ РАСЧЕТ:")
        print(f"σ_p = σ_0 + F/(2bδ) + σ_ce = {self.sigma_0} + {self.F}/(2×{self.b}×{self.delta}) + {self.sigma_ce} = {self.sigma_p:.2f} МПа")
        print(f"σ_max = σ_p + σ_i = {self.sigma_p:.2f} + {self.sigma_i:.2f} = {self.sigma_max:.2f} МПа")
        print(f"LP = σ_max^m × 3600 × i × z_sh = {self.sigma_max:.2f}^{self.m} × 3600 × {self.i} × {self.zsh} * {self.tch}")
        print(f"LP = {self.sigma_max ** self.m:.2e} × 3600 × {self.i} × {self.zsh} = {self.LP:.2e}")
        print(f"RP = σ_N^m × N_c0 = {self.sigma_N}^{self.m} × {self.Nc0} = {self.RP:.2e}")
        print(f"Отношение LP/RP = {self.LP / self.RP:.4f}")
    def load_test_data_1(self):
        """Тестовые данные 1: стандартный случай"""
        self.delta = 2
        self.D1 = 60
        self.sigma_0 = 0.4
        self.F = 18.
        self.b = 60
        self.E_i = 70

        self.i = 1
        self.i1 = 1
        self.zsh = 2
        self.u = 1.26

        self.case = 1
        self.case1 = 1

        self.sigma_i = 1.837
        self.sigma_x = 2.5
        self.ix = 3
        self.divex = 1

    def print_test_data_1(self):
        """Аккуратный вывод тестовых данных 1"""
        print("=" * 50)
        print("ТЕСТОВЫЕ ДАННЫЕ 1: СТАНДАРТНЫЙ СЛУЧАЙ")
        print("=" * 50)

        print("\nГЕОМЕТРИЧЕСКИЕ ПАРАМЕТРЫ:")
        print(f"   Толщина ремня (δ): {self.delta} мм")
        print(f"   Диаметр малого шкива (D₁): {self.D1} мм")
        print(f"   Ширина ремня (b): {self.b} мм")
        print(f"   Отношение D₁/δ: {self.D1 / self.delta}")

        print("\nМЕХАНИЧЕСКИЕ ПАРАМЕТРЫ:")
        print(f"   Модуль упругости (E_i): {self.E_i} МПа")
        print(f"   Начальное напряжение (σ₀): {self.sigma_0} МПа")
        print(f"   Сила тяги (F): {self.F} Н")

        print("\nКИНЕМАТИЧЕСКИЕ ПАРАМЕТРЫ:")
        print(f"   Число пробегов ремня (i): {self.i} пробегов/сек")
        print(f"   Число пробегов при σ_max (i1): {self.i1} пробегов/сек")
        print(f"   Число шкивов (z_sh): {self.zsh} шт.")
        print(f"   Передаточное число (u): {self.u}")

        print("\nРЕЖИМЫ РАБОТЫ:")
        print(f"   Способ определения долговечности (case): {self.case}")
        print(f"   Способ определения Cи (case1): {self.case1}")

        print("\nНАПРЯЖЕНИЯ И ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ:")
        print(f"   Напряжение изгиба (σ_i): {self.sigma_i} МПа")
        print(f"   Напряжение режима (σ_x): {self.sigma_x} МПа")
        print(f"   Число пробегов при σ_x (i_x): {self.ix} пробегов/сек")
        print(f"   Коэффициент времени работы (1/e_x): {self.divex}")

        print("\n" + "=" * 50)
de = durability_equation()
print('Выберите тип проверки (0 - из исходных данных, 1 - из своих)')
case = int(input())
if case == 0:
    de.load_test_data_1()
    de.print_test_data_1()
else:
    de.load_user_data()
de.calculate_all()
print('ВЫВОД:')
if de.calculate_isequal() == True:
    print('Правая и левая части равны в пределах допустимой погрешности, расчет достоверен.')
else:
    print('Правая и левая части не равны в пределах допустимой погрешности. Возможно, введенные данные некорректны в нашем случае.')
print('Вывести детали (0 - нет, 1 - да)')
case = int(input())
if case == 0:
    pass
else:
    de.print_detailed_calculation()