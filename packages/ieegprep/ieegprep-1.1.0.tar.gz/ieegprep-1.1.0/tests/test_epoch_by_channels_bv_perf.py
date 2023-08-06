"""
Unit tests to test the performance of epoching BrainVision data by iterating over and loading data per channel and
retrieving the trial-epochs




=====================================================
Copyright 2023, Max van den Boom (Multimodal Neuroimaging Lab, Mayo Clinic, Rochester MN)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import unittest
import os
import pickle
import numpy as np
from datetime import datetime
from ieegprep.bids.data_epoch import __load_data_epochs__by_channels
from ieegprep.utils.console import ConsoleColors
from ieegprep.utils.misc import clear_virtual_cache
from ieegprep.fileio.BrainVisionReader import BrainVisionReader

class TestFileIO(unittest.TestCase):
    """
    ...
    """

    #bv_data_path = 'D:\\BIDS_erdetect\\sub-BV\\ses-1\\ieeg\\sub-BV_ses-1_ieeg.vhdr'
    bv_data_path = os.path.expanduser('~/Documents/ERDetect_perf/sub-BV/ses-1/ieeg/sub-BV_ses-1_ieeg.vhdr')


    def test_epoch_by_channels_bv_perf(self):
        """
        ...
        """
        from ieegprep.utils.misc import time_func

        #__load_data_epochs__by_channels
        pass



if __name__ == '__main__':
    unittest.main()
