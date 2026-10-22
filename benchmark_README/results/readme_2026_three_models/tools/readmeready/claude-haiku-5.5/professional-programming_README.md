# professional-programming<h2>Description</h2>

<p>This repository is a collection of small code examples related to professional programming. The examples are short, self-contained snippets that can be read on their own.</p>

<p>Two examples are currently included:</p>

<ul>
<li><p><strong>Python with SQLAlchemy (<code>toaster_exists_bad</code> vs. <code>toaster_exists_good</code>):</strong> A SQLite in-memory database holds a <code>Toaster</code> table. The two functions check whether a toaster with a given ID exists. The "bad" version loads the full row with <code>.first()</code> to test for existence. The "good" version builds an <code>EXISTS</code> query and returns only a boolean, which avoids fetching unneeded data.</p></li>
<li><p><strong>JavaScript hoisting (HTML page):</strong> A small web page shows how JavaScript variables and functions behave when they are hoisted. It covers how an undeclared assignment inside a function creates a global variable, and how a <code>var</code> declared inside a function stays local to that function.</p></li>
</ul>

<p>The code is released under the MIT License, Copyright (c) 2017 Charles-Axel Dein.</p>
<h2>Requirements</h2>

<ul>
<li><strong>SQLAlchemy</strong>: The database example (<code>create_engine</code>, <code>sessionmaker</code>, <code>declarative_base</code>) imports from this package. No version is pinned in the provided context.</li>
</ul>

<p>The other example uses only the Python standard library (<code>collections.namedtuple</code>).</p>
<h2>Installation</h2>
<h2>Usage</h2>

<p>This project is a collection of standalone code examples. Each example is self-contained and can be run or opened on its own.</p>

<ul>
<li><strong>Python (SQLAlchemy) example:</strong> Running the script executes <code>main()</code>, which creates the <code>toasters</code> table in an in-memory SQLite database. It then calls <code>toaster_exists_bad(1)</code> and <code>toaster_exists_good(2)</code>. The engine is created with <code>echo=True</code>, so SQL statements are printed to the console. The script needs the <code>sqlalchemy</code> package installed.</li>
<li><strong>JavaScript hoisting example:</strong> This is an HTML page with an inline script. Open it in a web browser and check the browser's developer console to see the logged output. The comments in the script describe the expected results.</li>
</ul>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2017 Charles-Axel Dein.</p>

<p>The software is provided "as is", without warranty of any kind.</p>
