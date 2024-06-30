import os

import sys

def convert_srt_to_vtt(file_path, file_name):

    prefix_file_name = file_name[:-4]

    with open(os.path.join(file_path, file_name), encoding="utf-8") as inputFile:

        with open(os.path.join(file_path, prefix_file_name + ".vtt"), mode="w", encoding="utf-8") as outputFile:

            line_content = "WEBVTT\r\n\r\n\r\n"

            outputFile.write(line_content)

            for line in inputFile:

                if "-->" in line:

                    line_content = line.replace(",", ".")

                else:

                    line_content = line

                outputFile.write(line_content)

if __name__ == '__main__':

    args = sys.argv

    try:

        if os.path.isdir(args[1]):

            for file_name in os.listdir(args[1]):

                if file_name.endswith(".srt"):

                    print(file_name + " is converting...")

                    convert_srt_to_vtt(args[1], file_name)

                    print("convert completely!")

        elif os.path.isfile(args[1]):

            (file_path, file_name) = os.path.split(args[1])

            if file_name.endswith(".srt"):

                print(file_name + " is converting...")

                convert_srt_to_vtt(file_path, file_name)

                print("convert completely!")

            else:

                print("only srt file can converted.")

        else:
            print(111)
            # raise

    except:

        print("arg[1] should be file name or dir.")