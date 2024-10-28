# SimpSave

## Introduction  
As the name suggests, SimpSave is an extremely lightweight Python library that provides a simple solution for variable persistence. It is particularly suitable for use in small scripts or student projects.

SimpSave offers the following features:  
- **Extremely Simple**: The project has less than 200 lines of code, making it easy to understand and use quickly.
- **Easy to Learn**: It requires only basic Python knowledge, with no need for complex tutorials. In most cases, users can learn to use the library within a minute.

> The project has been published on PyPi.

## Usage Guide  

### Installation  
- Install SimpSave via `pip`:  
  ```bash
  pip install simpsave
  ```

- Import SimpSave into your code (usually as `ss`):  
  ```python
  import simpsave as ss
  ```

### Basic Concepts  
SimpSave supports the persistent storage of basic Python data types, including `int`, `float`, `bool`, `str`, as well as `list`, `tuple`, and `dict`. It provides basic operations like create, read, update, and delete.  
> For non-basic types, if the object implements a `__str__()` method, you can set the `convert_unsupported` parameter to `True` to store it as a string.

SimpSave’s methods make it easy to achieve data persistence. First, you need to check if SimpSave is ready (i.e., if the `.ini` file exists). If not, you need to initialize it:  
- Use `ss.ready()` to check if SimpSave is ready (i.e., if the `.ini` file exists).
- If not initialized, use the `ss.init()` method to initialize it. You can pass in `names` and `values` lists to set initial key-value pairs. The two lists must correspond one-to-one and have the same length.

SimpSave provides the following core functionalities:  
- `write()` to write data into the `.ini` file.
- `read()` to read stored data.
- `remove()` to delete specific data.
- `has()` to check if a specific key exists.
- `clear_ss()` to clear SimpSave by deleting the `.ini` file.

By default, SimpSave uses `__ss__.ini` as the storage file name, but you can change the file name by modifying the global variable `SIMPSAVE_FILENAME`.

Here’s a simple code example:  
```python
import simpsave as ss  # Import SimpSave with the alias ss

# Prepare data
name = 'Hello World'
value = 'Hello World!'

# Initialize SimpSave and write data (auto convert to two list)
ss.init(name, value)

"""
The above code is equivalent to (if auto_init = True)
ss.write(name, value)
"""

# Read and print the stored value
print(ss.read(name))  # Output: Hello World!
```

The name of a SimpSave storage unit can be any string, but ensure uniqueness to avoid conflicts.

For more detailed function usage and explanations, check the library overview below. You can also visit the GitHub project page to download sample code and explore this simple, easy-to-use library further.

### Library Overview  

##### `ready(operation_file: str = None)`  
- **Description**: Checks if SimpSave is initialized by verifying the existence of the `.ini` file.  
- **Parameters**:  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.    
- **Returns**: `True` if the file exists, `False` otherwise.  
- **Exceptions**:  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  

```python
if ss.ready():
    print("SimpSave is ready.")
```

##### `init(names: Union[list[str], str] = [], values: Union[list[Any], Any] = [], init_check: bool = True, operation_file: str = None)`  
- **Description**: Initializes SimpSave and writes key-value pairs if provided. Handles both single key-value pairs and lists.  
- **Parameters**:  
  - `names`: A list of strings or a single string representing the key(s).  
  - `values`: A list of values or a single value corresponding to the key(s).  
  - `init_check`: If set to `True`, raises a `FileExistsError` if SimpSave already exists.  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: `True` if initialization succeeds.  
- **Exceptions**:  
  - `FileExistsError`: If the `.ini` file exists and `init_check` is `True`.  
  - `ValueError`: If `names` and `values` are not lists or their lengths don't match.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  

```python
ss.init(['key1'], ['value1']) # Equal: ss.init('key1','value1')

# both raise ValueError
ss.init('key', [[1,2,3], 123])
ss.init(['1'], ['0', 11])

ss.init('count', 0, init_check = True, opeartion_file = 'simpsave.ini') # Skip init check, operating simpsave.ini

ss.init('test') # Will be init with value '[]' (as default value of value)
ss.init(['123', '123'], ['111', 111]) # Only storage one '123' with value 111 (The first one is overwrited)  
```

##### `write(names: Union[str, list[str]], values: Union[Any, list[Any]], overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False, operation_file: str = None)`  
- **Description**: Writes key-value pairs to SimpSave, with options for overwriting, automatic initialization, and type checking.  
- **Parameters**:  
  - `names`: Key name(s) (string or list of strings).  
  - `values`: Corresponding value(s) (any supported type).  
  - `overwrite`: If set to `False`, raises a `KeyError` if the key already exists.  
  - `auto_init`: Initializes SimpSave if it does not already exist.  
  - `type_check`: Checks for type consistency with existing data.  
  - `convert_unsupported`: If `True`, converts unsupported types to strings.  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: `True` if the write succeeds.  
- **Exceptions**:  
  - `FileNotFoundError`: If SimpSave doesn't exist and `auto_init` is `False`.  
  - `KeyError`: If overwriting is disabled and the key exists.  
  - `TypeError`: If value types are unsupported or inconsistent.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  

```python
ss.write('my_key', 123)
ss.write(['a','b','c'], ['1',2,[3.14]])

# convert unsupported
import datetime
ss.write('now', datetime.datetime.now(), convert_unsupported = True)

# operating a different file, with auto_init off
ss.write('1', 111, auto_init = False, opeation_file = 'different.ini')
```

##### `read(names: Union[str, list[str]], operation_file: str = None)`  
- **Description**: Reads the value(s) associated with the specified key(s).  
- **Parameters**:  
  - `names`: The key(s) to read (string or list of strings).  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: The value(s) associated with the key(s).  
- **Exceptions**:  
  - `FileNotFoundError`: If SimpSave doesn't exist.  
  - `KeyError`: If a key doesn't exist.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  

```python
value = ss.read('my_key')
print(value)

# read multiple
values = ss.read(['key1', 'key2', 'key3'])
for value in values:
  print(value)
```  
##### remove(names: Union[str, list[str]], operation_file: str = None)  
- **Description**: Removes the specified key and its associated value from SimpSave.  
- **Parameters**:  
  - `names`: The key(s) to remove (string or list of strings).  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: True if the key is successfully removed.  
- **Exceptions**:  
  - `FileNotFoundError`: If the SimpSave `.ini` file does not exist.  
  - `KeyError`: If the specified key does not exist.  
  - `TypeError`: If the key name is not a string.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  
  

```python
ss.remove('my_key')

# remove multiple
ss.remove(['r1', 'r2'])
```

##### has(names: Union[str, list[str]], operation_file: str = None)  
- **Description**: Check if the specific key exists.  
- **Parameters**:  
  - `names`: The key(s) to check (string or list of strings).  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: True if the key is exist. (Get a list of booleans if names is a list)    
- **Exceptions**:  
  - `FileNotFoundError`: If the SimpSave `.ini` file does not exist.  
  - `TypeError`: If the key name is not a string.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  
  

```python
ss.has('key')
```


##### clear_ss(operation_file: str = None)  
- **Description**: Deletes the SimpSave `.ini` file from the current directory.  
- **Parameters**:  
  - `operation_file`: The file for operating simpsave. If None, using default SIMPSAVE_FILENAME.   
- **Returns**: True if the file was successfully deleted, False otherwise.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist.  
  - `NameError`: If `operation_file` is not an INI file.  
- **Example**:  
  

```python
ss.clear_ss()
```  

### File Name and Reserved Words  
By default, SimpSave uses `__ss__.ini` as its name. You can modify `operation_file` when calling the function to manipulate different files.   
The following keys are retained in SimpSave:  
-` _build_ `: Record the creation time of SimpSave instance  
-` _uupdate_ `: Record the latest update time of SimpSave instance  
-` _ path_ `: Record the working path of SimpSave instance  
You can use the ` read() ` function to read relevant information. These reserved words are protected and will be rejected when written using the ` write() ` function.   
