import numpy as np

def get_prev_days():
    """This function return the number of days of historical data that the 
    Model requires to make predictions. The user cannot request to simulate values
    from a date where there is not at least this many days of historical information.

    Ex. if this is 90, the user could simulate the future of a well begining at day
    90 or 91, but there would not be enough valid data for the user to begin the simulation 
    on days 88 or 89.

    Returns:
        int: days of historical inputs
    """
    return 90

def get_forward_days():
    """This function returns the number of days into the future that the model can predict.
    This would be the duration of the simulation.

    Returns:
        int: days into the future the simulation runs
    """
    return 100

def get_historical_params():
    """This function returns the historical parameters that the model expects to be sent in
    when simulating a wells operation. These parameters must be provided for the previous number of 
    days (given by the get_prev_days function) before the simulation begins.

    Returns:
        list[str]: all the historical parameters needed to simulate a well.
    """
    # @FIXME: Small change. Should not be needed once I get user selected csv headers working
    return ['oilProd', 'steamInj', 'waterProd', 'pressure']

def get_future_params():
    """This function returns the future parameters that the model expects to be sent in
    when simulating a wells operation. These parameters must be provided for the future number of 
    days (given by the get_forward_days function) after the simulation begins.

    This is usually just Steam as this should be a known quantity, in the future the interface will allow a user to 
    use constant steam values or things that are generated for this inference.

    Returns:
        list[str]: all the future parameters needed to simulate a well.
    """
    return ['Steam',]

def simulate(historical_data, future_data):
    # check the data types
    assert type(historical_data) == np.ndarray, f"historical data should be np.ndarray but is {type(historical_data)}"
    assert type(future_data) == np.ndarray, f"future data should be np.ndarray but is {type(future_data)}"
    # check the shapes (well_count, n_days, n_params)
    assert len(historical_data.shape) == 3, f"shape of historical_data is {historical_data.shape} but expected (well_count, n_prev, n_hist_params)"
    assert len(future_data.shape) == 3, f"shape of future_data is {future_data.shape} but expected (well_count, n_forward, n_future_params)"
    # ensure that the data is of the right shapes
    assert historical_data.shape[0] == future_data.shape[0], f"well counts do not match hist {historical_data.shape[0]} and fut {future_data.shape[0]}"
    assert historical_data.shape[1] == get_prev_days(), f"historical data n_days is not valid expected {get_prev_days()} but got {historical_data.shape[1]}"
    assert future_data.shape[1] == get_forward_days(), f"future data n_days is not valid expected {get_forward_days()} but got {future_data.shape[1]}"
    assert historical_data.shape[2] == len(get_historical_params()), f"historical data expected {len(get_historical_params())} paramaters but got {historical_data.shape[2]}"
    assert future_data.shape[2] == len(get_future_params()), f"future data expected {len(get_future_params())} paramaters but got {future_data.shape[2]}"

    # just return back the last oil value of each well
    last_oil_value = historical_data[:, -1, 0:1]
    simulated_oil = np.repeat(last_oil_value, get_forward_days(), axis=1)
    return simulated_oil


def test():
    N_WELLS = 10
    N_PAST = get_prev_days()
    N_FORWARD = get_forward_days()
    N_HIST_PARAMS = len(get_historical_params())
    N_FUT_PARAMS = len(get_future_params())
    hist_data = np.random.uniform(low=0, high=100, size=(N_WELLS, N_PAST, N_HIST_PARAMS))
    fut_data = np.random.uniform(low=0, high=100, size=(N_WELLS, N_FORWARD, N_FUT_PARAMS))
    data = simulate(hist_data, fut_data)
    print(hist_data[:, -1, 0])
    print(data.shape)
    print(data[:, -1])


if __name__ == '__main__':
    test()