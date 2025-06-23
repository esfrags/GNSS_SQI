def validate_gpx_file(file_path):
    # Function to validate the GPX file format
    import os
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    if not file_path.endswith('.gpx'):
        raise ValueError("The file must be a GPX file.")
    
    return True

def log_message(message, log_file='app.log'):
    # Function to log messages to a specified log file
    with open(log_file, 'a') as f:
        f.write(message + '\n')