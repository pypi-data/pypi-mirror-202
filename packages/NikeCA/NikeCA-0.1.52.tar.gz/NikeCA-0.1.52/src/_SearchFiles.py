

class SearchFiles:

    def search_files(self, directory_path: str = None, search_string: str or list = None, save_path: str = None):
        """
        This function will go through a directory and all subdirectories and try to open each file no matter
        if it is another directory, a sql code, hql, or python file, or whatever. It will search for a substring
        or list of substrings within the file. It will then create a Polars dataframe with the following columns
        (Path, Filename, Start, Occurrences, Lines, Context). If the save_path is not None it will save the
        dataframe to the save_path.

        Parameters
        ----------
        directory_path : str
            The directory to recursively search through.
        search_string : str or list
            The substring or the list of substrings is the search criteria.
        save_path : str
            The location where to save the results.

        Returns
        -------
        Polars dataframe
            A Polars dataframe with the following columns (Path, Filename, Start, Occurrences, Lines, Context).
        """

        import os
        import re
        import pandas as pd
        import json

        # Check if directory_path is valid
        if not os.path.isdir(directory_path):
            raise ValueError('directory_path is not a valid directory.')

        # Check if search_string is valid
        if not isinstance(search_string, str) and not isinstance(search_string, list):
            raise ValueError('search_string must be a string or a list of strings.')

        if isinstance(search_string, str):
            search_string = [search_string]

        # Initialize the Polars dataframe
        df = {}

        for i in search_string:
            print(i)

            df[i] = {}

            # Recursively search through the directory
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    # Get the relative path for the file
                    path = os.path.relpath(os.path.join(root, file), directory_path)
                    filepath = path

                    with open(os.path.join(root, file), 'rb') as f:
                        byte_sequence = f.read()  # read the first 100 bytes
                        lines = byte_sequence.decode('iso-8859-1')

                        indexes = [index.start() for index in re.finditer(i.upper(), lines.upper())]

                        df[i][filepath] = {}
                        df[i][filepath]['Start'] = lines[:1000]
                        df[i][filepath]['char_index'] = {}

                        instance = 1
                        for index in indexes:
                            if index < 250:
                                index = 250
                            instance += 1

                            df[i][filepath]['char_index'][str(index)] = lines[index - 250: index + 250]

            print(i)

        reformed_dict = {}
        for k, v in df.items():
            for x, y in v.items():
                reformed_dict[(k, x)] = y

        df_pd = pd.DataFrame(reformed_dict).T

        df_pd.to_csv(save_path)

        return df_pd
