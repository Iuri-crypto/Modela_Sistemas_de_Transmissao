


from pathlib import Path 




class Subsystem__2():
    
    
    @classmethod
    def calculator(
        net,
        formato="json",
        dir_output: Path | str | None = None
    ):
      
        if dir_output is None:
            dir = Path(__file__).resolve().parent[3]
