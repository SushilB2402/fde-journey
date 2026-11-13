# Kaggle Learn: Data Cleaning — Chapter-by-Chapter Q&A notes

A personal, plain-English reference guide covering all five lessons of Kaggle Learn's **Data Cleaning** course—updated for **pandas 3.1+** and **NumPy 2.x**.

## Chapter 1: Handling Missing Values

### Q1: What is the very first thing I should do when I encounter missing data (`NaN` or `None`)?

**A:** Before jumping straight to code, pause and ask *why* the data is missing. Is the value missing because it wasn't recorded, or because it doesn't exist?

* **Example:** If a house doesn't have a garage, the "Garage Area" isn't just missing—it doesn't exist (so filling it with `0` makes sense). On the other hand, if someone skipped a question on a survey, it wasn't recorded, so guessing or imputing a value might make more sense.

### Q2: How do I quickly check how many missing values are in my dataset?

**A:** You can chain `.isnull().sum()` on your pandas DataFrame to get the exact count of missing entries per column. To get a sense of scale, divide the total missing cells by `df.size` (or `np.prod(df.shape)`) to see the overall percentage of missing data.

### Q3: When is it okay to just drop missing values using `dropna()`?

**A:** Dropping rows (`df.dropna()`) or columns (`df.dropna(axis=1)`) is usually only a good idea for quick prototypes or when a tiny fraction of your data is missing. If you drop every row with at least one `NaN`, you could accidentally wipe out your entire dataset!

### Q4: What are the best ways to fill in (impute) missing values automatically?

**A:** Instead of throwing away good data, you can use `.fillna()` or directional fill methods:

* **Constant value:** `df.fillna(0)` replaces all `NaN`s with `0` (great when missing means "none").

* **Backward/Forward fill:** `df.bfill().fillna(0)` (or `df.ffill()`) fills missing values using the value that comes right after (or before) it in the same column, and then replaces any remaining `NaN`s at the edges with `0`. This works especially well for data that has a logical order, like time-series logs.

## Chapter 2: Scaling and Normalization

### Q1: What is the difference between Scaling and Normalization? People use them interchangeably!

**A:** They sound similar, but they change your numbers in very different ways:

* **Scaling** changes the **range** of your data (e.g., squishing all values so they sit neatly between `0` and `1`). The shape of the data's distribution stays the exact same.

* **Normalization** changes the **shape** of your data's distribution so that it looks more like a normal distribution (a classic bell curve).

### Q2: Why and when should I scale my data?

**A:** You should scale your data whenever you are using algorithms that measure distances between data points—like **Support Vector Machines (SVM)** or **k-Nearest Neighbors (kNN)**. If one column is measured in millimeters and another in kilometers, the algorithm will mistakenly treat the larger numbers as more important. Scaling puts every feature on a level playing field (typically `[0, 1]`).

### Q3: Why and when should I normalize my data?

**A:** You should normalize your data if you plan to use machine learning or statistical techniques that assume your data follows a bell curve (a Gaussian distribution)—such as **Linear Discriminant Analysis (LDA)** or **Gaussian Naive Bayes**. Using a method like the **Box-Cox transformation** (`scipy.stats.boxcox`) helps tame heavily skewed data into a clean bell shape.

## Chapter 3: Parsing Dates

### Q1: Why does pandas sometimes treat a column of dates like plain text?

**A:** When you load a CSV file, pandas often reads date columns as string/object data types because dates can be written in dozens of ways (`03/11/2026`, `2026-11-03`, `Nov 3, 2026`). Until you explicitly parse them, Python doesn't know how to extract the month, day, or year, or how to sort them chronologically.

### Q2: How do I convert a text column into proper Python `datetime64` objects?

**A:** You use `pd.to_datetime()` along with an explicit `format` string that tells pandas how to read the pieces of the date using `strftime` directives:

* `%d` = Day of the month (e.g., `13`)

* `%m` = Month as a number (e.g., `11`)

* `%y` = 2-digit year (e.g., `26`) vs. `%Y` = 4-digit year (e.g., `2026`)

* *Example:* `pd.to_datetime(df['Date'], format="%d/%m/%Y")` (or `"%m/%d/%Y"` for US dates)

### Q3: What if a single column has mixed date formats and throws a `ValueError`?

**A:** Real-world datasets often have messy entries where someone typed a full year in one row and a 2-digit year in another. You can check the string lengths of your date entries (`df['Date'].str.len()`) to isolate the weird rows, parse each subset with its own explicit `format`, and combine them back together. *(Note: Avoid `format='mixed'` on non-US dates, as it defaults to month-first parsing and can silently flip day and month—e.g., reading `03/11/2026` as March 11 instead of 3 November!)*

### Q4: Once dates are parsed, how do I extract specific parts like the day of the month?

**A:** Use the `.dt` accessor! For example, `df['Date_parsed'].dt.day` pulls out just the day of the month for every row. Plotting a histogram of these days (`1` through `31`) is a classic sanity check—if you see a massive spike on the 1st of every month, it might mean missing days defaulted to `01`, or your month and day got swapped!

## Chapter 4: Character Encodings

### Q1: What is a character encoding, and why do I get `UnicodeDecodeError` when opening files?

**A:** Computers only understand binary (`0`s and `1`s). A **character encoding** is the rulebook that maps specific byte sequences to human-readable characters (like `"A"`, `"é"`, or `"🚀"`). A `UnicodeDecodeError` happens when you try to read a file using the wrong rulebook—for instance, trying to read a file saved in `Windows-1252` or `Shift_JIS` using Python's default `UTF-8` encoding.

### Q2: What is UTF-8, and how should I save my cleaned files?

**A:** **UTF-8** is the universal standard text encoding for Python and the web. It can represent almost every character in every human language (plus emojis) without breaking. Whenever you export your cleaned DataFrame to a CSV, save it in UTF-8 and remember to pass `index=False` so pandas doesn't write an extra unnamed index column:

```python
df.to_csv("cleaned_data.csv", index=False)
```

### Q3: How can I figure out the encoding of a mystery file that refuses to open?

**A:** Don't guess blindly! Read the first few thousand bytes of the file in raw binary mode (`'rb'`) and pass them to the `charset_normalizer` (or `chardet`) library. It will inspect the byte patterns and tell you the most likely encoding along with a confidence score. Then, pass that exact encoding into `pd.read_csv(..., encoding='...')`.

## Chapter 5: Inconsistent Data Entry

### Q1: What causes inconsistent text entries, and why are they a problem?

**A:** Whenever humans type data by hand, small variations creep in: `"USA"`, `"usa"`, `"United States"`, or `"USA "` (with a trailing space). To a human, those are identical. To Python, they are four completely different categories, which will ruin your grouping, counting, and model training.

### Q2: What are the first two quick wins for cleaning messy text columns?

**A:** Always start by standardizing case and stripping hidden whitespace:

1. Convert everything to lowercase: `df['Country'] = df['Country'].str.lower()`

2. Remove leading and trailing spaces: `df['Country'] = df['Country'].str.strip()`
   Doing just these two steps often eliminates half of your duplicate categories right away.

### Q3: How do I fix remaining typos and spelling variations without checking thousands of rows by hand?

**A:** Use **fuzzy matching** with a library like `thefuzz` (formerly `fuzzywuzzy`)! Fuzzy matching calculates a similarity score (from `0` to `100`) between two strings based on how many character edits it takes to turn one into the other.

* **Workflow:** Grab the unique values in your column, use `process.extract()` to find strings that closely match a target word (e.g., a similarity score `> 80`), and replace all those close matches with one clean, standardized string.