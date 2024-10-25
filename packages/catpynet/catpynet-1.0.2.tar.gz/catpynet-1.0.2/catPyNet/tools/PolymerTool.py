import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from tqdm import tqdm
import catpynet.main.CatPyNet as cpn
import argparse
from catpynet.fileIO.IOManager import OUTPUT_FILE_FORMATS, TRUTH_STRINGS
import catpynet.Utilities as Ut



def main():

    parser = argparse.ArgumentParser(description="Constructs Polymer Models")
    parser.add_argument("-a", metavar="alphabet size",
                        help="alphabet size (list (x,y,z,...) or range (x-z or x-z/step) ok)",
                        default="2")
    parser.add_argument("-k", metavar="food max length",
                        help="food molecule max length  (list or range ok)", default="2")
    parser.add_argument("-n", metavar='polymer max length',
                        help="polymer max length  (list or range ok)", default="4")
    parser.add_argument("-m", metavar="mean catalyzed",
                        help="mean number of catalyzed reactions per molecule  (list or range ok)",
                        default="2.0")
    parser.add_argument("-r", metavar="replicate",
                        help="The replicate number/seed (list or range ok)", default="1")
    parser.add_argument("-o", metavar="output", help="Output directory (or stdout)",
                        default="stdout")
    parser.add_argument("-f", metavar="file name template",
                        help="file name template (use #a,#k,#n,#m,#r for parameters)",
                        default="polymer_model_a#a_k#k_n#n_m#m_r#r.crs")
    parser.add_argument("-z", metavar='output zipped',
                        help="Should the output be a zipped directory. (True or False)",
                        choices=TRUTH_STRINGS,
                        default="False")
    parser.add_argument("-of", metavar="output format",
                        help="file format to be written. e.g. '.crs'",
                        choices=OUTPUT_FILE_FORMATS,
                        default=None)
    parser.add_argument("-rn", metavar="reaction notation",
                        help="Output reaction notation", default="FULL")
    parser.add_argument("-an", metavar="arrow notation",
                        help="Output arrow notation", default="USES_EQUALS")
    parser.add_argument("-ow", metavar="overwrite ok", help="Sets if the program is allowed to " +
                        "write over files", choices=TRUTH_STRINGS, default="False")

    arguments = vars(parser.parse_args())

    alphabet_sizes = Ut.parse_integer_input(arguments["a"])
    food_max_lengths = Ut.parse_integer_input(arguments["k"])
    polymer_max_lengths = Ut.parse_integer_input(arguments["n"])
    means = Ut.parse_float_input(arguments["m"])
    number_of_replicates = Ut.parse_integer_input(arguments["r"])
    zipped = True if arguments['z'].casefold(
    ) in ['True'.casefold(), "1"] else False
    overwrite_ok = True if arguments['ow'].casefold(
    ) in ['True'.casefold(), "1"] else False

    cpn.generate_reaction_system_files(alphabet_sizes,
                                       food_max_lengths,
                                       polymer_max_lengths,
                                       means,
                                       number_of_replicates,
                                       arguments['o'],
                                       arguments['f'],
                                       zipped,
                                       arguments['of'],
                                       arguments['rn'],
                                       arguments['an'],
                                       overwrite_ok)


if __name__ == "__main__":
    main()
