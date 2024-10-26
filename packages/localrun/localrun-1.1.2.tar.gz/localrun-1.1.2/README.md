# LocalRun

`localrun` is a Python package that provides an easy way to run a simple HTTP server locally, similar to the `php -S` command. It supports both silent and non-silent modes for logging HTTP requests.

## Installation

You can install `localrun` using pip:

```bash
pip install localrun
```

## Command-Line Usage

You can run the server directly from the command line using the following syntax:

### Start Server with Host and Port

```bash
localrun --host <HOST> --port <PORT>
```

### Start Server with Silent Mode

To run the server in silent mode, which suppresses log output:

```bash
localrun --host <HOST> --port <PORT> --silent
```

### Examples

1. **Start Server on Default Host and Port (127.0.0.1:8000)**

   ```bash
   localrun
   ```

2. **Start Server on Specified Host and Port**

   ```bash
   localrun --host 127.0.0.1 --port 8000
   ```

3. **Start Server with Silent Mode**

   ```bash
   localrun --host 127.0.0.1 --port 8000 --silent
   ```

## Programmatic Usage

You can also use `localrun` as a module in your Python scripts.

### Example Script

Here’s how to start the server programmatically:

```python
# example_script.py
import localrun

# Start the server in silent mode
running_address = localrun.run_server('127.0.0.1', 8000, silent=True)

# Print the running address
print(f"Running port is: {running_address}")
```

### Running Without Silent Mode

To start the server without silent mode:

```python
# example_script.py
import localrun

# Start the server
running_address = localrun.run_server('127.0.0.1', 8000)

# Print the running address
print(f"Running port is: {running_address}")
```

## Logging Format

In non-silent mode, the server logs HTTP requests in the following format :

```
localrun - - [25/Oct/2024 23:01:50] "GET /new/instance/ HTTP/1.1" 200 -
```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


