import subprocess

class ProcessInTerminal:
    def __init__(self, total: int, title: str) -> None:
        self._init = 1
        self._total = total
        self._title = title
    
    def print(self) -> None:
        percentage = (self._init / self._total) * 100
        subprocess.run("clear")
        
        print("Novel: {}\nTotal: % {:.2f} ({} of {})".format(
                    self._title, 
                    percentage, 
                    self._init, 
                    self._total
                )
        )
        
        self._init = self._init + 1
        return None