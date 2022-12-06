import sys
from refactorengine import RefactorEngine

def main():
    code = sys.argv[1]

    refactorEngine = RefactorEngine(code)
    refactorEngine.refactorCode()
    
    
if __name__ == "__main__":
    main()