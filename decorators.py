import subprocess

class PrintProgress:
    def __init__(self, total: int) -> None:
        self._total = total
        self._count = 0
    
    def __call__(self, parse_funct) -> any:
        def wrapper(*args: any, **kwds: any):
            self._count += 1
            percentage = (self._count / self._total) * 100
            
            subprocess.run("clear")
            
            print("Total: % {:.2f} ({} of {})".format(percentage, self._count, self._total))

            return parse_funct(*args, **kwds)
        return wrapper



    
    