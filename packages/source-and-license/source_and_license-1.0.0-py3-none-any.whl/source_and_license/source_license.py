# source_license.py
import os

##################
#  CONFIGURATION #
##################
# Setting up supported languages and methods to check if a language and an
#  extension are supported.

LANGUAGES = (
    ("python", ".py", "#"),
    ("lua", ".lua", "--")
)  # LANGUAGES


def supported_languages() -> tuple:
    supp_langs = []
    for lang_tup in LANGUAGES:
        supp_langs.append(lang_tup[0])
    return tuple(supp_langs)


print("Supported languages: %s" % str(supported_languages()))


def supported_extensions() -> tuple:
    supp_exts = []
    for lang_tup in LANGUAGES:
        supp_exts.append(lang_tup[1])
    return tuple(supp_exts)


print("Supported extensions: %s" % str(supported_extensions()))


def is_lang_supp(chosen_language: str) -> str | None:
    if chosen_language in supported_languages():
        return chosen_language
    return None


def is_ext_supp(chosen_ext: str) -> str | None:
    if chosen_ext in supported_extensions():
        return chosen_ext
    return None


def fetch_by_language(chosen_language: str) -> tuple[str, str, str] | None:
    for lang_tup in LANGUAGES:
        if chosen_language == lang_tup[0]:
            return lang_tup
    return None


def fetch_by_extension(chosen_extension: str) -> tuple[str, str, str] | None:
    for lang_tup in LANGUAGES:
        if chosen_extension == lang_tup[1]:
            return lang_tup
    return None


def fetch_language_by_extension(chosen_extension: str) -> str | None:
    return fetch_by_extension(chosen_extension)[0]


#############
# AUTHORING #
#############
# Methods for generating the license header


def generate_license_header_for_language(chosen_language: str) -> str:
    # Example authors: "Fred, George and Helena"
    authors = "PICK AN AUTHOR NAME"
    # Example license: "GNU General Public License 3"
    license_name = "PICK A LICENSE NAME"
    base_text = \
        "This source code is copyright of %s, and it is licensed under %s.\n"
    supported_language = fetch_by_language(chosen_language.lower())
    if supported_language is not None:
        lang_comment = supported_language[2]
        return ("%s%s%s %s" % (
            lang_comment,
            lang_comment,
            lang_comment,
            (base_text % (
                authors, license_name
            ))  # BASE_TEXT
        ))  # return
    # Else:
    error_msg = "\n"
    error_msg += " /!\ Invalid language: %s\n" % chosen_language
    error_msg += " /!\ Supported languages: %s\n" % str(supported_languages())
    return error_msg


example = "   COMCOMCOM %s" % (
        "BASE_TEXT authors: %s, license: %s."
        % ("AUTHORS", "LICENSE_NAME")
)  # example
print("Example: %s" % example)

py_example = generate_license_header_for_language("python")
lua_example = generate_license_header_for_language("lua")
err_example = generate_license_header_for_language("ENGLISH")
print("   Python example: %s" % py_example)
print("   Lua example: %s" % lua_example)
print("   Error example: %s" % err_example)


##################
# INPUT / OUTPUT #
##################
# Methods for gathering all input files to be processed and writing the license
#  header to the output.

print("-------------------")
print("BEGIN WRITING FILES")


IN_DIR = "./data/input/"
INPUT_FILES = []
for filename in os.listdir(IN_DIR):
    file_name, file_ext = os.path.splitext(filename)
    if file_ext in supported_extensions():
        INPUT_FILES.append(filename)
    else:
        print("Skipping '%s', extension not supported." % filename)

print("Input files: %s" % INPUT_FILES)


OUT_DIR = "./data/output/"
for input_filename in INPUT_FILES:
    output_filename = input_filename
    for supp_ext in supported_extensions():
        if input_filename.endswith(supp_ext):

            # Generate the license header.
            source_license = generate_license_header_for_language(
                fetch_language_by_extension(supp_ext)
            )
            source_input = ""

            # Read the original file.
            with open(IN_DIR + input_filename, "r") as input_file:
                for line in input_file:
                    source_input += line

            # Skip writing if the file already starts with the same license.
            if source_input.startswith(source_license):
                print(
                    "Skipping file '%s', it already has the same license..."
                    % input_filename
                )  # print

            # Write the new file with the generated license.
            else:
                with open(OUT_DIR + output_filename, "w") as output_file:
                    output_file.write(
                        source_license + source_input
                    )  # write
                print("Wrote file '%s'..." % output_filename)


print("END WRITING FILES")
print("-------------------")
