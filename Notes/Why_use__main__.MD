# Why use `if __name__ == "__main__":`

It's a Python convention that answers the question: **"was this file run directly, or imported by something else?"**

When Python runs a file, it sets a special variable called `__name__`. Its value depends on *how* the file was launched:

- If you run it directly (`python data_acquisition.py`), Python sets `__name__ = "__main__"`
- If another file imports it (`import data_acquisition`), Python sets `__name__ = "data_acquisition"` (the module name instead)

So the block:
```python
if __name__ == "__main__":
    # setup, start threads, etc.
```
only executes when you run the file directly. If someone imports your file to reuse `transform_data()` or `csv_write_loop()` in another script, the serial port won't open, threads won't start, and `input()` won't block — only the function definitions get loaded.

---

In your specific case it's not strictly necessary since you're unlikely to import this file elsewhere, but it's considered good practice because it:

- Makes your intent clear — "this is the entry point"
- Keeps setup code separated from reusable code
- Makes the file safer to import for testing individual functions without triggering the full program

Think of it as the Python equivalent of a "start here" sign.