import glob
import numpy
from scipy.misc import imread, imresize, imshow
from PIL import Image

class DataHandler:
    """
    Handles the neural network data
    """

    def __init__(self, files=glob.glob('data/**/*.jpg'), initialize_files=True, debug_enabled=False):
        """
        Constructor

        :param files: Files to load in
        :param debug_enabled: If debug output is enabled
        """

        # Initialize class variables
        self.data = []
        self.target = []
        self.debug_enabled = debug_enabled
        if initialize_files:
            self.handle_files(files)

    def handle_files(self, files):
        """
        Load in files

        :param files: List of files to load
        """


        # Loop through each file
        num_forwards = 0
        for file in files:

            # Normalize data so forwards are not overrepresented
            if 'forward' in file:
                num_forwards += 1
                if num_forwards > 620:
                    continue

            # Read image
            image = imread(file, flatten=True)

            # Determine type
            im_type = self.determine_type(file)

            # Add to lists
            self.data.append(image)
            self.target.append(im_type)

            # Debug logging
            if self.debug_enabled:
                im_type_index = self.determine_index(im_type)
                print(self.index_to_description(im_type_index) + ": " + file)

    def determine_type(self, file):
        """
        Determine file type from file location

        :param file: File location
        :returns: Number representing file type
        """

        # Left - 2
        if file.find('left') != -1:
            return [0, 0, 1]
        # Right - 1
        elif file.find('right') != -1:
            return [0, 1, 0]
        # Forward - 0
        elif file.find('forward') != -1:
            return [1, 0, 0]
        else:
            print("Unknown image type: ", file)
            return [0, 0, 0]

    def determine_index(self, type_arr):
        """
        Gets index from type array

        :param type_arr: The type array as defined in self.determine_type
        :returns: The index
        """
        return numpy.argmax(type_arr)

    def index_to_description(self, index):
        """
        Convert type to description

        :param index: The index
        :returns: Description of the numeric representation of the type
        """

        descriptions = {
            0: 'forward',
            1: 'right',
            2: 'left'
        }

        # Return description from dictionary or 'Unknown'
        try:
            description = descriptions[index]
        except KeyError:
            description = 'Unknown'

        return description

    def get_data(self):
        """
        Get the data (images)
        
        :returns: Array of image arrays
        """
        return self.data

    def get_target(self):
        """
        Get the target (outputs)

        :returns: Array of outputs for the data
        """
        return self.target