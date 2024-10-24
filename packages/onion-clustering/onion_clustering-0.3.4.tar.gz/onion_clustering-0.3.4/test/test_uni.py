import os

import pytest
from onion_clustering import main as onion

### Set all the analysis parameters ###
FILE = "water_coex_100ps_1nm_LENS.npy"
PATH_TO_INPUT_DATA = "/Users/mattebecchi/00_signal_analysis/data/" + FILE
TAU_WINDOW = 10
T_DELAY = 1
NUM_TAU_W = 2
MAX_TAU_W = 10
MAX_T_SMOOTH = 2


# Define a fixture to set up the test environment
@pytest.fixture
def setup_test_environment(tmpdir):
    # tmpdir is a built-in pytest fixture providing a temporary directory
    original_dir = os.getcwd()  # Save the current working directory
    os.chdir(str(tmpdir))  # Change to the temporary directory
    yield tmpdir
    os.chdir(
        original_dir
    )  # Restore the original working directory after the test


# Define the actual test
def test_output_files(setup_test_environment):
    ### Create the 'data_directory.txt' file ###
    with open("data_directory.txt", "w+", encoding="utf-8") as file:
        print(PATH_TO_INPUT_DATA, file=file)

    ### Create the 'input_parameter.txt' file ###
    with open("input_parameters.txt", "w+", encoding="utf-8") as file:
        print(f"tau_window\t{TAU_WINDOW}", file=file)
        print(f"t_delay\t{T_DELAY}", file=file)
        print(f"num_tau_w\t{NUM_TAU_W}", file=file)
        print(f"max_tau_w\t{MAX_TAU_W}", file=file)
        print(f"max_t_smooth\t{MAX_T_SMOOTH}", file=file)

    # Call your code to generate the output files
    tmp = onion.main(False)

    # Test the output
    tmp.plot_tra_figure()
    tmp.plot_input_data("Fig0")
    tmp.plot_cumulative_figure()
    tmp.plot_one_trajectory()
    tmp.data.plot_medoids()
    tmp.plot_state_populations()
    tmp.sankey([0, 10, 20, 30, 40])
    tmp.print_labels()
    tmp.plot_pop_fractions()

    # Define the paths to the expected and actual output files
    original_dir = (
        "/Users/mattebecchi/00_signal_analysis/timeseries_analysis/test/"
    )
    expected_output_path_1 = original_dir + "output_uni/final_states.txt"
    expected_output_path_2 = original_dir + "output_uni/number_of_states.txt"
    expected_output_path_3 = original_dir + "output_uni/fraction_0.txt"
    actual_output_path_1 = "final_states.txt"
    actual_output_path_2 = "number_of_states.txt"
    actual_output_path_3 = "fraction_0.txt"

    # Use filecmp to compare the contents of the expected
    # and actual output directories
    with (
        open(expected_output_path_1, "r") as expected_file,
        open(actual_output_path_1, "r") as actual_file,
    ):
        assert expected_file.read() == actual_file.read()
    with (
        open(expected_output_path_2, "r") as expected_file,
        open(actual_output_path_2, "r") as actual_file,
    ):
        assert expected_file.read() == actual_file.read()
    with (
        open(expected_output_path_3, "r") as expected_file,
        open(actual_output_path_3, "r") as actual_file,
    ):
        assert expected_file.read() == actual_file.read()
