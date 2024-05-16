import unittest
from tkinter import *
from tkinter import messagebox
from unittest.mock import patch
import main.py  

class TestMorseGame(unittest.TestCase):
    def setUp(self):
        self.tk = morse_game.tk
        self.canvas = morse_game.canvas

    def test_game_start(self):
        # Überprüfung der Anzeige von Spielfeldern
        self.assertEqual(len(self.canvas.find_all()), 2)  # Два игровых поля
        # Überprüfung der Platzierung von Schiffen
        self.assertNotEqual(len(self.canvas.find_all()), 0)  # Корабли присутствуют на поле
        # Überprüfung der Spielfeldgröße
        self.assertEqual(self.canvas.winfo_width(), morse_game.size_canvas_x * 2 + morse_game.menu_x)
        self.assertEqual(self.canvas.winfo_height(), morse_game.size_canvas_y + morse_game.menu_y)

    @patch('morse_game.check_winner2', return_value=True)
    def test_game_end_player1(self, mock_check_winner2):
        # Überprüfen des Spielendes, wenn Spieler 1 gewinnt
        with patch.object(messagebox, 'askokcancel') as mock_askokcancel:
            mock_askokcancel.return_value = True
            morse_game.app_running = False
            morse_game.on_closing()
            self.assertFalse(morse_game.app_running)

    @patch('morse_game.check_winner2_igrok_2', return_value=True)
    def test_game_end_player2(self, mock_check_winner2_igrok_2):
        # Überprüfen des Spielendes, wenn Spieler 2 gewinnt
        with patch.object(messagebox, 'askokcancel') as mock_askokcancel:
            mock_askokcancel.return_value = True
            morse_game.app_running = False
            morse_game.on_closing()
            self.assertFalse(morse_game.app_running)

    def test_switch_game_mode(self):
        # Überprüfung des Wechsels des Spielmodus
        morse_game.computer_vs_human = False
        morse_game.change_rb()
        self.assertTrue(morse_game.computer_vs_human)
        # Überprüfen der Anzeige der Spielmodusinformationen
        self.assertIn("(Компьютер)", morse_game.add_to_label)
        self.assertIn("(прицеливается)", morse_game.add_to_label2)

    def test_restart_game(self):
        # Spielneustart prüfen
        morse_game.button_begin_again()
        # Überprüfen der Entfernung aller Objekte
        self.assertEqual(len(self.canvas.find_all()), 0)

    @patch('morse_game.hod_computer')
    def test_computer_hod_when_human_mode(self, mock_hod_computer):
        # Überprüfen des Fortschritts des Computers im Modus „Mensch gegen Mensch
        morse_game.computer_vs_human = False
        morse_game.add_to_all("<Button-1>")
        mock_hod_computer.assert_not_called()

    @patch('morse_game.hod_computer')
    def test_computer_hod_when_computer_mode(self, mock_hod_computer):
        # Überprüfen des Fortschritts des Computers im Modus „Mensch vs. Computer“
        morse_game.computer_vs_human = True
        morse_game.hod_igrovomu_polu_1 = True
        morse_game.add_to_all("<Button-1>")
        mock_hod_computer.assert_called_once()

    def test_human_hod_when_computer_mode(self):
        # Überprüfen des menschlichen Zuges im Modus Mensch gegen Computer
        morse_game.computer_vs_human = True
        morse_game.hod_igrovomu_polu_1 = False
        with patch.object(morse_game, 'mark_igrok') as mock_mark_igrok:
            morse_game.add_to_all("<Button-1>")
            mock_mark_igrok.assert_called_once_with(False)

    def test_human_hod_when_human_mode(self):
        # Überprüfung des menschlichen Zuges im Modus „Mensch gegen Mensch“
        morse_game.computer_vs_human = False
        morse_game.hod_igrovomu_polu_1 = True
        with patch.object(morse_game, 'mark_igrok') as mock_mark_igrok:
            morse_game.add_to_all("<Button-1>")
            mock_mark_igrok.assert_called_once_with(True)

if __name__ == '__main__':
    unittest.main()
