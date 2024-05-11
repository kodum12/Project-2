import math
import re

from gui import *
from PyQt6.QtWidgets import *


class Logic(QMainWindow, Ui_Calculator):
    def __init__(self) -> None:
        """Initialize the calculator."""
        super().__init__()
        self.setupUi(self)
        self.calc_output.setEnabled(False)
        self.degreeChecked: bool = False
        self.radianChecked: bool = False
        self.current_input: str = ''

        # Connect number buttons
        self.button0.clicked.connect(lambda: self.number_clicked('0'))
        self.button1.clicked.connect(lambda: self.number_clicked('1'))
        self.button2.clicked.connect(lambda: self.number_clicked('2'))
        self.button3.clicked.connect(lambda: self.number_clicked('3'))
        self.button4.clicked.connect(lambda: self.number_clicked('4'))
        self.button5.clicked.connect(lambda: self.number_clicked('5'))
        self.button6.clicked.connect(lambda: self.number_clicked('6'))
        self.button7.clicked.connect(lambda: self.number_clicked('7'))
        self.button8.clicked.connect(lambda: self.number_clicked('8'))
        self.button9.clicked.connect(lambda: self.number_clicked('9'))

        # Connect trigonometric function buttons
        self.sine_button.clicked.connect(lambda: self.add_trig_function('sin('))
        self.cosine_button.clicked.connect(lambda: self.add_trig_function('cos('))
        self.tangent_button.clicked.connect(lambda: self.add_trig_function('tan('))
        self.arcsine_button.clicked.connect(lambda: self.add_trig_function('SI-1('))
        self.arccos_button.clicked.connect(lambda: self.add_trig_function('CO-1('))
        self.arctan_button.clicked.connect(lambda: self.add_trig_function('TA-1('))

        # Connect other buttons
        self.addition_button.clicked.connect(lambda: self.operation_clicked('+'))
        self.subtract_button.clicked.connect(lambda: self.operation_clicked('-'))
        self.multiply_button.clicked.connect(lambda: self.operation_clicked('*'))
        self.divide_button.clicked.connect(lambda: self.operation_clicked('/'))
        self.equals_button.clicked.connect(self.evaluate)
        self.clear_button.clicked.connect(self.clear)
        self.delete_button.clicked.connect(self.delete)
        self.pi_button.clicked.connect(lambda: self.number_clicked(str(math.pi)))
        self.sqrt_button.clicked.connect(lambda: self.add_sqrt('√'))
        self.dot_button.clicked.connect(lambda: self.add_dot('.'))

        self.para1_button.clicked.connect(lambda: self.add_para('('))
        self.para2_button.clicked.connect(lambda: self.add_para(')'))

        # Mode buttons
        self.degree_button.clicked.connect(self.degree_mode)
        self.radian_button.clicked.connect(self.radian_mode)

    def add_trig_function(self, function: str) -> None:
        """Add a trigonometric function to the current input."""
        self.current_input += function
        self.calc_output.setText(self.current_input)

    def add_dot(self, dot: str) -> None:
        """Add a dot to the current input."""
        self.current_input += dot
        self.calc_output.setText(self.current_input)

    def add_sqrt(self, sqrt: str) -> None:
        """Add a square root function to the current input."""
        self.current_input += f"{sqrt}("
        self.calc_output.setText(self.current_input)

    def degree_mode(self) -> None:
        """Switch to degree mode."""
        self.degreeChecked = True
        self.radianChecked = False
        self.degree_button.setEnabled(False)
        self.radian_button.setEnabled(True)

    def radian_mode(self) -> None:
        """Switch to radian mode."""
        self.radianChecked = True
        self.degreeChecked = False
        self.radian_button.setEnabled(False)
        self.degree_button.setEnabled(True)

    def number_clicked(self, number: str) -> None:
        """Append a number to the current input."""
        self.current_input += number
        self.calc_output.setText(self.current_input)

    def operation_clicked(self, operation: str) -> None:
        """Append an operation to the current input."""
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/']:
            self.current_input += operation
            self.calc_output.setText(self.current_input)

    def add_para(self, parentheses: str) -> None:
        """Add parentheses to the current input."""
        self.current_input += parentheses
        self.calc_output.setText(self.current_input)

    def delete(self) -> None:
        """Delete the last character from the current input."""
        self.current_input = self.current_input[:-1]
        self.calc_output.setText(self.current_input)

    def clear(self) -> None:
        """Clear the calculator."""
        self.current_input = ""
        self.calc_output.setText("")
        self.degreeChecked = False
        self.degree_button.setEnabled(True)
        self.radian_button.setEnabled(True)
        self.radianChecked = False

    def evaluate(self) -> None:
        """Evaluate the current expression."""
        try:
            self.expression = self.current_input

            numeric_values = set(re.findall(r'\d*\.?\d+', self.expression))

            for user_answer in numeric_values:
                self.expression = self.expression.replace(f'√({user_answer})', f'math.sqrt({user_answer})')

                if self.degreeChecked:
                    # Replace inverse trig functions with degrees conversion in degree mode
                    if f"math.asin(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.asin({user_answer}))",
                                                f"math.degrees(math.asin({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'SI-1({user_answer})',
                                                                  f"math.asin(math.radians({user_answer}))")

                    if f"math.acos(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.acos({user_answer}))",
                                                f"math.degrees(math.acos({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'CO-1({user_answer})',
                                                                  f"math.acos(math.radians({user_answer}))")

                    if f"math.atan(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.atan({user_answer}))",
                                                f"math.degrees(math.atan({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'TA-1({user_answer})',
                                                                  f"math.atan(math.radians({user_answer}))")



                    if f"math.sin(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.sin({user_answer}))",
                                                f"math.degrees(math.sin({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'sin({user_answer})',
                                                                  f"math.sin(math.radians({user_answer}))")

                    if f"math.cos(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.cos({user_answer}))",
                                                f"math.degrees(math.cos({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'cos({user_answer})',
                                                                  f"math.cos(math.radians({user_answer}))")

                    if f"math.tan(math.radians({user_answer}))" in self.expression:
                        self.expression.replace(f"math.degrees(math.tan({user_answer}))",
                                                f"math.degrees(math.tan({user_answer}))")
                    else:
                        self.expression = self.expression.replace(f'tan({user_answer})',
                                                                  f"math.tan(math.radians({user_answer}))")
                else:
                    if f'math.asin({user_answer})' in self.expression:
                        self.expression.replace(f'math.asin({user_answer})', f'math.asin({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'SI-1({user_answer})', f'math.asin({user_answer})')

                    if f'math.acos({user_answer})' in self.expression:
                        self.expression.replace(f'math.acos({user_answer})', f'math.acos({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'CO-1({user_answer})', f'math.acos({user_answer})')

                    if f'math.atan({user_answer})' in self.expression:
                        self.expression.replace(f'math.atan({user_answer})', f'math.atan({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'TA-1({user_answer})', f'math.atan({user_answer})')

                    if f'math.sin({user_answer})' in self.expression:
                        self.expression.replace(f'math.sin({user_answer})', f'math.sin({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'sin({user_answer})', f'math.sin({user_answer})')

                    if f'math.cos({user_answer})' in self.expression:
                        self.expression.replace(f'math.cos({user_answer})', f'math.cos({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'cos({user_answer})', f'math.cos({user_answer})')

                    if f'math.tan({user_answer})' in self.expression:
                        self.expression.replace(f'math.tan({user_answer})', f'math.tan({user_answer})')
                    else:
                        self.expression = self.expression.replace(f'tan({user_answer})', f'math.tan({user_answer})')



            self.result = eval(self.expression)
            self.calc_output.setText(str(self.result))
            self.current_input = str(self.result)

        except Exception as e:
            self.calc_output.setText(
                'Error. Please check your input and try again.'
            )
            self.current_input = ''
            print(str(e))

