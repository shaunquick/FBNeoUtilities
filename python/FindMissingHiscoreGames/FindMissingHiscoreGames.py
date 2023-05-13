# This script will neeed to
# extract all game names from hiscore.dat

# extract all games that currently do not have hiscore support from all d_*.cpp files
# input value will provide the starting folder which will need to recursively find all *.cpp files.

# populate both in lists
# once done 

#for each hiscore game 
#    check if exists in the *.cpp name
    # if yes then check if in *.cpp game name - check if already supported by hiecore -
#        if yes then do nothing otherwside
 #       raise that we need to add hiscore support.
        
# python3 FindMissingHiscoreGames.py 
# "G:\Source\Repos\FBNeo-ShaunFork\projectfiles\visualstudio-2022\x64\Release\support\hiscores\hiscore.dat" 
# "G:\Source\Repos\FBNeo-ShaunFork\src\burn\drv"




# System modules
import os
from fnmatch import fnmatch
import sys
import getopt

#Local modules



def usage(exit_status, debug=False):
    FUNC_NAME="usage(): "
    if debug: print(FUNC_NAME)
    """Show command line usage."""
    msg = ('Usage: FindMissingHiscoreGames.py [OPTIONS] hiscore.dat-file fbneo-programs-folder \n'
           'Find missing hiscores\n\nOptions:\n'
           '-o, --output=filename               If not provided, will output to STDOUT\n'
           '-h --help                           Display usage information and exit.\n'
           '-d --debug                          Run in debug mode (display extra info).\n'
    )
    print(msg)
    print ('python3 FindMissingHiscoreGames.py -d -o="G:\...\Find Missing Hiscore Games\missinghiscores.log"  G:\...\support\hiscores\hiscore.dat G:\...\src\burn\drv')

    sys.exit(exit_status)


    
def writeResults(filename, data_list, debug=False):
    FUNC_NAME="writeResults(): "
    if debug: print(FUNC_NAME)
    
    # Write the  data to output file
    if len(filename) > 0:
        with open(filename, "w") as file:
            file.write("List of games that require HiScore support to be added")
            for item in data_list:
                file.writelines(["\n",item])
    else:
        print("List of games that require HiScore support to be added")
        for item in data_list:
            print(item)

    return(0)

def find_nth(search_string, search_value, n):
    start = search_string.find(search_value)
    while start >= 0 and n > 1:
        start = search_string.find(search_value, start+len(search_value))
        n -= 1
    return start

def getGamesWithoutHiscoreSupport(hiscore_games,unsupported_cpp_games):
    missing_hiscore_support_list = []
    for game in hiscore_games:
        if game in unsupported_cpp_games:
            missing_hiscore_support_list.append(game)
    return (missing_hiscore_support_list)

def getUnsupportedHiscoreGames(cpp_filename):

    try:
        with open(cpp_filename, "rt") as file:        
            file_lines_list=file.readlines()    
    except:
        with open(cpp_filename, "rt", encoding="utf8") as file:        
            file_lines_list=file.readlines()    

    unsupported_hiscore_games_list=[]
    is_BurnDriver=False
    for line in file_lines_list:
        if line.find("struct BurnDriver") >= 0:
            is_BurnDriver=True
            burn_driver_line=line
        elif is_BurnDriver:
            burn_driver_line = burn_driver_line + line
            if line.find(";") >= 0:
                if burn_driver_line.find("BDF_HISCORE_SUPPORTED") == -1 and burn_driver_line.find("BDF_GAME_WORKING") >= 0:
                    # add the game name to the list as it is not hiscore supported
                    unsupported_hiscore_games_list.append(burn_driver_line[find_nth(burn_driver_line,'"',1)+1:find_nth(burn_driver_line,'"',2)])
                is_BurnDriver=False


    return (unsupported_hiscore_games_list)

def getCppFilenames(source_directory,debug=False):
    FUNC_NAME="get_cpp_filenames(): "
    if debug: print(FUNC_NAME)

    pattern = "d_*.cpp"
    files_list = []
    try:
        for path, subdirs, files in os.walk(source_directory):
            for name in files:
                if fnmatch(name, pattern):
                    if debug: print(os.path.join(path, name))
                    files_list.append( os.path.join(path, name))

    except Exception as err:
        raise Exception("{0}".format(err))
    else:
        return (files_list)
         
def getHiscoreGames(hiscore_filename="./hiscore.dat", debug=False):
    # return a list of hiscore game names in json fomat
    # ["pacman","pacman2"]

    FUNC_NAME="get_hiscore_games(): "
    if debug: print(FUNC_NAME)

    try:
        with open(hiscore_filename, "rt") as file:
            file_lines_list=file.readlines()    

        list_of_hiscore_games=[]
        for line in file_lines_list:
            if len(line) >0:
                if line[0] != ';' and line[0] != '@' and line != "\n":
                    list_of_hiscore_games.append(line[0:line.find(":")])
                    if debug: print(line[0:line.find(":")])
    # 
    except Exception as err:
        raise Exception("{0}".format(err))
    else:
        return (list_of_hiscore_games)

            
def main():
    FUNC_NAME="main(): "
    try:
        arg_names = ["help", "debug", "output ="]
        opts, args = getopt.getopt(sys.argv[1:], "hdo:", arg_names)
    except getopt.GetoptError:
        usage(2)


    try:
        debug = False
        outputfile=""
        for option, arg in opts:
            if option in ("-h", "--help"):
                usage(0, debug=debug)
 

            if option in ("-d", "--debug"):
                debug = True
                if debug: print(FUNC_NAME+"Debug Turned On!!")

            if option in ("-o", "--output"):
                outputfile = arg[1:]
                if debug: 
                    print(FUNC_NAME)
                    print("Output file is :- " + outputfile)

        if not args:
            usage(2, debug=debug)

        if len(args) < 2:
            usage(2, debug=debug)

        hiscore_filename=args[0]
        source_directory=args[1]

        if hiscore_filename.find("/") >= 0:
            print("found a / will be a full filename")
        elif hiscore_filename.find("\\") >= 0:
            print("found a \\ will be a full filename")
        else:
            print("found nothing need to add default folder name")
            hiscore_filename = "./" + hiscore_filename

        hiscore_games_list = getHiscoreGames(hiscore_filename, debug)

        cpp_files_list = getCppFilenames(source_directory,debug)
        unsupported_cpp_games_list=[]
        for cpp_filename in cpp_files_list:
            unsupported_cpp_games_list = unsupported_cpp_games_list + getUnsupportedHiscoreGames(cpp_filename)
  
    # We now have a list of games that support hiscores from hiscore.dat and also a list of all the games
    # from the drivers .cpp files that have not had hiscore support added
    # now for each hiscroe suported game check if it is in the cpp list - if so it's a miss !!!        


        missing_hiscore_support_list = getGamesWithoutHiscoreSupport(hiscore_games_list,unsupported_cpp_games_list)
        writeResults(outputfile, missing_hiscore_support_list, debug)
    except Exception as err:
        raise Exception("{0}".format(err))
    else:
        return(True)

    
    
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    print("App is started..")
    try:
        main()
    except Exception as err:
        print("Exception found: {0}".format(err))
    else:
        print("App has ended....")
    
            
