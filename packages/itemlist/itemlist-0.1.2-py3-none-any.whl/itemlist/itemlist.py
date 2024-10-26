import curses

class Item:
    """
    The Item class manages CLI menu items.
    """

    def __init__(self):
        """Initialize the Item class."""
        self.items = []
        self.cancel_option = ("Cancel", self._cancel, "Cancel and exit")

    def __call__(self, func):
        """
        Decorator to add functions to the item list.

        Args:
            func (function): The function to register.

        Returns:
            function: The original function.
        """
        # Add the function name, the function itself, and the description to the item list
        description = func.__defaults__[0] if func.__defaults__ else ""
        self.items.append((func.__name__, func, description))
        return func  # Return func to make it work as a decorator

    def select(self):
        """Display the CLI menu and return the selected item."""
        return self._cli_select()

    def _cli_select(self):
        """Internal method to display the CLI menu using curses."""
        def menu(stdscr):
            curses.curs_set(0)
            selected_index = 0
            search_query = ""
            all_items = self.items + [self.cancel_option]

            while True:
                stdscr.clear()
                height, width = stdscr.getmaxyx()

                # Display the search bar
                search_prompt = "Search: " + search_query
                stdscr.addstr(0, 0, search_prompt, curses.A_UNDERLINE)

                # Get the filtered items
                filtered_items = self._filter_items(search_query, all_items)

                # Adjust the items to be displayed (based on the maximum number of displayable rows)
                display_items = filtered_items[:height - 2]  # Consider the search bar and margin
                for idx, (name, _, description) in enumerate(display_items):
                    if idx == selected_index:
                        stdscr.addstr(idx + 1, 0, f"> {name}: {description}", curses.A_BOLD)
                    else:
                        stdscr.addstr(idx + 1, 0, f"  {name}: {description}")

                key = stdscr.getch()

                if key in (curses.KEY_UP, ord('k')):
                    selected_index = (selected_index - 1) % len(display_items) if display_items else 0
                elif key in (curses.KEY_DOWN, ord('j')):
                    selected_index = (selected_index + 1) % len(display_items) if display_items else 0
                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    search_query = search_query[:-1]
                    selected_index = 0
                elif key in [curses.KEY_ENTER, ord("\n")]:
                    if display_items:
                        return display_items[selected_index]
                elif key == 27:  # Cancel with ESC key
                    return self.cancel_option
                elif 32 <= key <= 126:  # Printable characters
                    search_query += chr(key)
                    selected_index = 0

                stdscr.refresh()

        return curses.wrapper(menu)

    def _filter_items(self, query, items):
        """Internal method to filter items based on a query."""
        if not query:
            return items
        query_lower = query.lower()
        return [item for item in items if query_lower in item[0].lower() or query_lower in item[2].lower()]

    def _cancel(self):
        """Handle cancellation."""
        # Processing when canceled (can be extended as needed)
        pass

    def endwin(self):
        """End the curses window."""
        curses.endwin()

item = Item()

def main():
    # Placeholder for console script entry point
    pass

if __name__ == '__main__':
    main()
