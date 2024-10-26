# ItemList
**ItemList** provides a tool for selecting and executing functions in a CLI environment. It offers an intuitive interface for managing and executing multiple workflows or tasks efficiently.

#### **1. Simple Decorator-Based Integration**
- Functions can be added to the menu simply by using the **@item decorator**. It requires minimal changes to existing functions to integrate them into the CLI menu.

  **Example Code**:
  ```python
  @item # only this!
  def func_1():
      print("func_1 is executing...")

  @item
  def func_2(description="Perform another important task"):
      print("func_2 is executing...")
  ```

![itemlist](https://github.com/user-attachments/assets/2a3ec397-ef90-4d44-a9df-c4a6b571cb6c)

#### **2. Intuitive CLI Interface**
- Utilizing the **curses** library, users can navigate through options smoothly with arrow keys or `j`/`k`. The currently selected item is displayed in bold for better visibility.

#### **3. Efficient Search Functionality**
- The menu includes a **search bar**, allowing users to filter options by function name or description. This makes it easy to quickly find the desired function, even among numerous options.

#### **4. Function Registration with Descriptions**
- Each function can be registered with an optional **description**. This allows users to easily understand the purpose or details of each task, reducing the chance of incorrect selections.

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
