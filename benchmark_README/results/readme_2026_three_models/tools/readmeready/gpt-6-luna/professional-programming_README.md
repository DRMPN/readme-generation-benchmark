# professional-programming<h2>Description</h2>

<p>This project includes examples illustrating two programming concepts:</p>

<ul>
<li>A Python example uses SQLAlchemy with an in-memory SQLite database to compare checking for a <code>Toaster</code> record by fetching it with <code>.first()</code> and checking existence with an <code>EXISTS</code> query.</li>
<li>An HTML page demonstrates JavaScript variable behavior, including hoisting and the difference between a function-scoped <code>var</code> declaration and an undeclared assignment.</li>
</ul>
<h2>Requirements</h2>

<ul>
<li>Python</li>
<li>SQLAlchemy, required by the database example. Install it with <code>pip install SQLAlchemy</code>.</li>
</ul>
<h2>Installation</h2>

<p>The SQLAlchemy example requires SQLAlchemy. Install it with:</p>

<p><code>bash
python -m pip install SQLAlchemy
</code></p>
<p>I’ll inspect the repository to identify its intended usage and any runnable examples.</p>

<h2>Usage</h2>

<p>The repository includes a standalone HTML example and a Python SQLAlchemy example.</p>

<ul>
<li>Open the HTML example in a browser to see the JavaScript output in the developer console and <code>Hello JavaScript!</code> on the page. It demonstrates that <code>typeof variable</code> returns <code>"undefined"</code>, that the assignment to <code>a</code> inside <code>hoist()</code> makes it accessible outside the function, and that the function-scoped <code>b</code> is not accessible there.</li>
<li>Run the Python example in an environment with SQLAlchemy installed. Its <code>main()</code> creates the tables in an in-memory SQLite database, then calls <code>toaster_exists_bad(1)</code> and <code>toaster_exists_good(2)</code>. The two functions show alternative ways to check whether a <code>Toaster</code> row exists.</li>
</ul>
<p>I’ll inspect the repository for contribution instructions and project-specific development workflows, then draft only what is supported by the files.</p>

<h2>Contributing</h2>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2017 Charles-Axel Dein</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>
