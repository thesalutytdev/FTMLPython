from ftml import FTMLParser
import ftml

class FTML:
    @staticmethod
    def main(args):
        objects = FTMLParser.parse_file("./example.ftml")
        for ftml_object in objects:
            print(str(ftml_object))

if __name__ == "__main__":
    FTML.main([])