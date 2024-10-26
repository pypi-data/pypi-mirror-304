# ItemList
ItemList is a Python library that allows you to select and search items from the command line. It offers flexible UI options, search functionality, and a cancel option.

![itemlist](https://github.com/user-attachments/assets/2a3ec397-ef90-4d44-a9df-c4a6b571cb6c)


## Installation

```bash
pip install itemlist
```

## Usage

More details can be found in the [examples](https://github.com/Luftalian/itemlist/tree/main/examples) directory.

```python
from itemlist import item

@item
def flow_runner(description="Run the first flow"):
    run_locally(flow)

@item
def flow2_runner(description="Run the second flow"):
    run_locally(flow2)

@item
def flow3_runner(description="Run the third flow"):
    run_locally(flow3)

if __name__ == '__main__':
    selected = item.select()
    item.endwin()

    selected_name, selected_func, selected_func_description = selected

    if selected_func == item._cancel:
        print("Cancel selected. Exiting the program.")
    else:
        print(f"Running: {selected_name}\n")
        print(f"Description: {selected_func_description}\n")
        selected_func()
```

## License

[MIT License](https://github.com/Luftalian/itemlist/blob/main/LICENSE)
