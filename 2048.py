import tkinter as tk
import colors as c
import random

""" Tworzenie planszy (macierzy kwadratowej) o danym rozmiarze
:param I_SIZE: wielkosc planszy
:type I_SIZE: int
"""
I_SIZE = 3
J_SIZE = I_SIZE


class Game(tk.Frame):
    def __init__(self):
        """Jest to gra stworzona na podstawie aplikacji mobilnej o nazwie '2048',
        Program ten polega na sumowaniu blokow o tej samej wartosci numerycznej,
        w wyniku tej operacji w miejscu jednego z blokow powstaje nowy blok o
        wartosci rownej sumie laczonych blokow.
        Gra przewiduje rozgrywke do 2048 punktow.
        Warunkiem przegranej jest brak mozliwych ruchow do wykonania
        Wszystkie dokonczone rozgrywki zostaja zapisane w pliku
        Aby przemieszczac bloki nalezy uzywac strzalek na klawiaturze
        """
        tk.Frame.__init__(self)

        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.nick_input_view()

        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

        self.mainloop()

    def nick_input_view(self):
        """Generowanie widoku odpowiedzialnego za wpisanie nicku uzytkownika
        """
        self.nick_input_label = tk.Label(self.main_grid,
                                         bg=c.GRID_COLOR,
                                         font=c.SCORE_LABEL_FONT,
                                         text="Wpisz swoj nick")
        self.nick_input_label.place(relx=0.5,
                                    y=20,
                                    anchor=tk.CENTER)
        self.nick_input_box = tk.Entry(self.main_grid,
                                       font=("Helvetica", 30, "bold"))
        self.nick_input_box.place(relx=0.5,
                                  y=70,
                                  anchor=tk.CENTER)
        self.nick_enter_button = tk.Button(self.main_grid,
                                           text="Zatwierdz nick",
                                           command=self.nick_button_reaction)
        self.nick_enter_button.place(relx=0.5,
                                     y=120,
                                     anchor=tk.CENTER)

    def nick_button_reaction(self):
        """Reakcja na przycisk zatwierdzajacy nazwe uzytkownika
        Zapisuje wpisana nazwe uzytkownika oraz zmienia wikod na
        plansze do gry
        """
        self.nick = self.nick_input_box.get()
        # usuwamy niepotrzebne juz czesci GUI
        self.nick_input_label.destroy()
        self.nick_input_box.destroy()
        self.nick_enter_button.destroy()
        if self.nick == "":
            self.nick_input_view()
        else:
            self.make_GUI()
            self.start_game()

    def make_GUI(self):
        """Tworzenie poczatkowego stanu GUI
        :param self.cells: komorki na planszy
        :param self.score_label: wyswietlany tekst o ilosci punktow
        :return:
        """
        # twprzenie komorek
        self.cells = []
        for i in range(I_SIZE):
            row = []
            for j in range(J_SIZE):
                cell_frame = tk.Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width=150, height=150)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {
                    "frame": cell_frame,
                    "number": cell_number
                }
                row.append(cell_data)
            self.cells.append(row)

        # tworzenie licznika punktow
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor=tk.CENTER)
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        """Generowanie poczatkowego stanu gry,
        Tworzenie pierwszych dwoch poczatkowych blokow do gry oraz ustawienie punktacji na 0
        :param self.matrix: macierz 2D ktora funkcjonuje jako plansza do gry
        :return:
        """
        # tworzenie planszy (macierzy) wypelnionej zerami
        self.matrix = [[0] * I_SIZE for _ in range(I_SIZE)]

        # wypelnienie dwoch losowych komorek blokami o poczatkowej wartosci 2
        row = random.randint(0, I_SIZE - 1)
        col = random.randint(0, J_SIZE - 1)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2],
                                                 font=c.CELL_NUMBER_FONTS[2], text="2")
        while self.matrix[row][col] != 0:
            row = random.randint(0, I_SIZE - 1)
            col = random.randint(0, J_SIZE - 1)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2],
                                                 font=c.CELL_NUMBER_FONTS[2], text="2")
        self.score = 0

    """Metody manipulacji macierza gry"""

    def move_blocks(self):
        """Przenoszenie blokow roznych od 0 na prawo tak blisko
        granicy jak to tylko mozliwe
        """
        new_matrix = [[0] * I_SIZE for _ in range(I_SIZE)]
        for i in range(I_SIZE):
            fill_position = 0
            for j in range(J_SIZE):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine_blocks(self):
        """Zlaczanie blokow bedacych obok siebie w linii poziomej"""
        for i in range(I_SIZE):
            for j in range(J_SIZE):
                if self.matrix[i][j] != 0 and j + 1 < J_SIZE \
                        and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse_matrix(self):
        """Odwrocenie macierzy"""
        new_matrix = []
        for i in range(I_SIZE):
            new_matrix.append([])
            for j in range(J_SIZE):
                new_matrix[i].append(self.matrix[i][J_SIZE - 1 - j])
        self.matrix = new_matrix

    def transpose_matrix(self):
        """Transpozycja macierzy"""
        new_matrix = [[0] * I_SIZE for _ in range(I_SIZE)]
        for i in range(I_SIZE):
            for j in range(J_SIZE):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_block(self):
        """Dodanie do losowych pustych komorek nowych
        blokow jezeli istnieje miejsce,
        """
        if self.exist_free_space_in_matrix():
            row = random.randint(0, I_SIZE - 1)
            col = random.randint(0, J_SIZE - 1)
            while self.matrix[row][col] != 0:
                row = random.randint(0, I_SIZE - 1)
                col = random.randint(0, J_SIZE - 1)
            self.matrix[row][col] = random.choice([2, 4])

    def update_GUI(self):
        """Uaktualnianie wyswietlanych informacji w GUI, nalezy wywolywac
        ta metode po kazdej wprowadzonej zmianie w interfejsie planszy gry
        Komorki sa uaktualniane na podstawie macierzy gry, jezeli wartosc
        komorki jest rowna 0 to oznacza brak bloku w danym miejscu
        Uaktualniana jest rowniez informacja o ilosci zdobytych punktow
        """
        for i in range(I_SIZE):
            for j in range(J_SIZE):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR,
                                                         text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value],
                                                         fg=c.CELL_NUMBER_COLORS[cell_value],
                                                         font=c.CELL_NUMBER_FONTS[cell_value],
                                                         text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    """Akcje wykonywane za pomoca klawiszy"""

    def move_left(self, e):
        """Ruch blokow w lewo"""
        self.move_blocks()
        self.combine_blocks()
        self.move_blocks()
        self.add_new_block()
        self.update_GUI()
        self.end_game()

    def move_right(self, e):
        """Ruch blokow w prawo"""
        self.reverse_matrix()
        self.move_blocks()
        self.combine_blocks()
        self.move_blocks()
        self.reverse_matrix()
        self.add_new_block()
        self.update_GUI()
        self.end_game()

    def move_up(self, e):
        """Ruch blokow w gore"""
        self.transpose_matrix()
        self.move_blocks()
        self.combine_blocks()
        self.move_blocks()
        self.transpose_matrix()
        self.add_new_block()
        self.update_GUI()
        self.end_game()

    def move_down(self, e):
        """Ruch blokow w dol"""
        self.transpose_matrix()
        self.reverse_matrix()
        self.move_blocks()
        self.combine_blocks()
        self.move_blocks()
        self.reverse_matrix()
        self.transpose_matrix()
        self.add_new_block()
        self.update_GUI()
        self.end_game()

    """Sprawdzanie czy istnieje mozliwosc ruchu"""

    def exist_free_space_in_matrix(self):
        """Metoda sprawdza czy na planszy istnieje miejsce o watosci 0
        :rtype bool
        """
        for i in range(I_SIZE):
            for j in range(J_SIZE):
                if self.matrix[i][j] == 0:
                    return True
        return False

    def horizontal_move_exist(self):
        """Metoda sprawdza czy na planszy jest mozliwosc aby wykonac ruch w poziomie
        :rtype bool"""
        for i in range(I_SIZE):
            for j in range(J_SIZE - 1):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exist(self):
        """Metoda sprawdza czy na planszy jest mozliwosc aby wykonac ruch w pionie
                :rtype bool"""
        for i in range(I_SIZE - 1):
            for j in range(J_SIZE):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    """Sprawdzanie warunkow ukonczenia gry"""

    def end_game(self):
        """Sprawdzanie warunkow zakonczenia gry
        Gra sie konczy jezeli na planszy brakuje miejsca na nowe bloki - Przegrana
        albo jezeli przynajmniej jeden z blokow osiagnie wartosc 2048 - Wygrana"""
        if any(2048 in row for row in self.matrix):
            self.show_score_label("Wygrales! :)")
        elif not any(0 in row for row in
                     self.matrix) and not self.horizontal_move_exist() and not self.vertical_move_exist():
            self.show_score_label("Przegrales! :c")

    def show_score_label(self, text):
        """Pokazanie koncowej tablicy wynikow wraz ze
        wszystkimi zapisanymi graczami i ich punktami
        """
        self.add_new_score()
        self.main_grid.destroy()
        self.end_frame = tk.Frame(self, width=100, bg=c.LOSER_BG)
        self.end_frame.grid()
        tk.Label(self.end_frame,
                 text=text,
                 bg=c.LOSER_BG,
                 fg=c.GAME_OVER_FONT_COLOR,
                 font=c.GAME_OVER_FONT).grid()
        self.new_game_button = tk.Button(self.end_frame,
                                         text="Nowa gra",
                                         command=self.new_game)
        self.new_game_button.grid()
        self.test = tk.Text(self.end_frame, width=30, height=30)
        self.test.grid()
        self.test.insert(tk.END, self.get_scores_in_order())

    def new_game(self):
        """Restart gry"""
        self.destroy()
        main()

    """Operacje wykonywane na pliku z wynikami gry"""

    def create_resoult_file(self):
        """Tworzenie pliku z wynikami graczy"""
        self.nick_line_in_file = 0
        open("scores.txt", "x")

    def is_that_player_exist(self):
        """Sprawdzanie czy gracz juz istnieje (jesli tak to jezeli zdobedzie lepszy wynik to zostanie on nadpisany)
        i zapisanie numeru lini w ktorej bedzie zapisany wynik uzytkownika
        :param self.nick_line_in_file: numer linii w pliku wynikowym w ktorej wynik uzytkownika zostanie zapisany
        :rtype bool
        """
        self.nick_line_in_file = 0
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    if self.nick in line:
                        return True
                self.nick_line_in_file += 1
            self.nick_line_in_file += 1
            return False

        except FileNotFoundError:
            self.create_resoult_file()
            return False

    def file_max_score(self):
        """Szukanie najwyzszego zdobytego wyniku z pliku
        :param self.max_score: Najwyzszy wynik ze wszystkich grajacych (domyslnie 0)
        :type self.max_score: int
        :return:
        """
        self.max_score = 0
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    if self.max_score < int(line[-1]):
                        self.max_score = int(line[-1])

        except FileNotFoundError:
            open("scores.txt", "x")

    def add_new_score(self):
        """Do pliku zostaje dodawany wynik gracza wraz
        z jego nazwa uzytkownika
        """
        text = self.nick + " " + str(self.score) + " \n"
        try:
            with open("scores.txt", "a") as f:
                f.writelines(text)

        except FileNotFoundError:
            with open("scores.txt", "x") as f:
                f.writelines(text)

    def override_player_score(self):
        """Nadpisywanie istniejacego juz wyniku wyniku gracza
        :return:
        """
        text = self.nick + " " + str(self.score) + " \n"
        try:
            with open("scores.txt", "r") as f:
                list_of_lines = f.readlines()
                list_of_lines[self.nick_line_in_file] = text

            with open("scores.txt", "w") as f:
                f.writelines(list_of_lines + 1)

        except FileNotFoundError:
            with open("scores.txt", "x") as f:
                f.writelines(text)

    def get_scores_in_order(self):
        """Zwraca posortowane wyniki w formie
        uporzadkowanego tekstu
        """
        with open("scores.txt", "r") as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            lines[i][-1] = int(lines[i][-1])

        lines.sort(key=lambda x: x[-1], reverse=True)

        place = 1
        res = ""
        for line in lines:
            res += str(place) + ".\t"
            for elem in line:
                res += str(elem) + " "
            if line == [self.nick, int(self.score)]:
                res += "\t<----- YOU"
            res += "\n"
            place += 1
        return res


def main():
    Game()


if __name__ == '__main__':
    main()
