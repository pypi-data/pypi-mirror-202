from ENPROG.enprog import EnProg
import sys
def dispatch(case):
    return {
        'run': 1,
        'import': 2,
        'check': 3,
        'translate': 4,
    }.get(case, 'Invalid case')

def main():
    args = sys.argv
    if len(sys.argv) < 2:
        print("Usage: enprog [run|import|check|translate]")
        sys.exit(1)
    if dispatch(args[1]) == 1:
        EnProg.run_program(args[2])
    elif dispatch(args[1]) == 2:
        EnProg.importPackage(args[2], args[3])
    elif dispatch(args[1]) == 3:
        EnProg.check_syntax(args[2])
    elif dispatch(args[1]) == 4:
        EnProg.translate_program(args[1])
    filename = sys.argv[1]
    EnProg.run_program(filename)

if __name__ == "__main__":
    main()
