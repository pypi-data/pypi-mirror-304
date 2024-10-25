import os 
import time 

class ZStyle:

  RESET = '\033[0m'
  BLACK = '\033[30m'
  RED = '\033[31m'
  GREEN = '\033[32m'
  YELLOW = '\033[33m'
  BLUE = '\033[34m'

  @staticmethod
  def clear():
    os.system('cls' if os.name == 'nt' else "clear")

  @staticmethod
  def type(text:str, delay:float=0.15):
    for char in text:
      print(char, end="", flush=True)
      time.sleep(delay)

  @staticmethod
  def type_input(text:str, delay:float=0.15):
    for char in text:
      print(char, end="", flush=True)
      time.sleep(delay)
    return input()

  @staticmethod
  def pause(message:str = "Press Enter to continue.."):
    input(message)

  @staticmethod
  def color(text:str, color:str) -> str:
    return f"{color}{text}{ZStyle.RESET}"


    


    
    