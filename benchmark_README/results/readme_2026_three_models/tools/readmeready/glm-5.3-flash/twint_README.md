# twint<h2>Description</h2>

<p>Twint is an advanced Twitter scraping tool written in Python that allows for scraping Tweets from Twitter profiles without requiring the use of Twitter's API.</p>

<p>Twint utilizes Twitter's search operators to make a complete query shown like this: <code>from:jack</code> or <code>since:2015-04-01</code>. Using these search operators as arguments in the command line allows the user to grab a lot of very specific Tweets as well as other Twitter information.</p>

<p>Twint can also be used to fetch almost all information about a Twitter account (follower/following lists, user info, tweets, retweets) except for private information like what you would see on a logged in account (for example, DMs).</p>

<p>One of the advantages of Twint is that it doesn't require an account to use it. Instead, the program scrapes directly from Twitter's search interface, forming the same kind of requests that are used by the website itself. It also works well with Python 3.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.6 - 3.8.</li>
</ul>

<p><strong>Modules mentioned in <a href="https://github.com/twintproject/twint/blob/master/requirements.txt">requirements.txt</a>:</strong></p>

<ul>
<li>aiohttp</li>
<li>aiodns</li>
<li>aiohttp_socks</li>
<li>beautifulsoup4</li>
<li>cchardet</li>
<li>dataclasses</li>
<li>elasticsearch</li>
<li>fake-useragent</li>
<li>geoip2</li>
<li>googletrans</li>
<li>pandas</li>
<li>pysocks</li>
<li>schedule</li>
</ul>

<p>Note that <code>googletrans</code> is installed from a custom fork (<a href="https://github.com/x0rzkov/py-googletrans">py-googletrans</a>) rather than from PyPI, as specified in the package's dependency links. When you install twint with <code>pip3 install . -r requirements.txt</code>, all of these dependencies are pulled in automatically.</p>
<h2>Installation</h2>

<h3>Pip</h3>

<p><code>
pip3 install twint
</code></p>

<p>or grab the latest version directly from GitHub:</p>

<p><code>
pip3 install --upgrade git+https://github.com/twintproject/twint.git@master
</code></p>

<p>Installing via <code>pip</code> registers a <code>twint</code> console command that you can run from your terminal.</p>

<h3>Git</h3>

<p><code>
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt
</code></p>

<h3>Docker</h3>

<p>A <code>Dockerfile</code> is included with the project. Build the image and run it interactively:</p>

<p><code>
docker build -t twint .
docker run -it twint
</code></p>

<blockquote>
  <p><strong>Note:</strong> <code>twint</code> requires Python 3.6 or higher (3.6, 3.7, and 3.8 are supported).</p>
</blockquote>
<h2>Usage</h2>

<p>twint can be used in two ways: as a command-line tool, or as a Python module that you import into your own scripts. In both cases, you configure <em>what</em> to scrape (users, search terms, date ranges, filters) and <em>where</em> to store the results (terminal output, CSV, JSON, SQLite, Elasticsearch, or pandas).</p>

<h3>Command-line tool</h3>

<p>Once installed, the <code>twint</code> command is available in your terminal. Some common examples:</p>

<ul>
<li><code>twint -u username</code> — Scrape all the Tweets of a user.</li>
<li><code>twint -u username -s pineapple</code> — Scrape all the Tweets of a user containing the word <code>pineapple</code>.</li>
<li><code>twint -s pineapple</code> — Collect every Tweet containing <code>pineapple</code> from everyone's Tweets.</li>
<li><code>twint -u username --year 2014</code> — Collect Tweets that were tweeted in 2014.</li>
<li><code>twint -u username --since 2015-12-20 --until 2016-01-05</code> — Collect Tweets that were tweeted between two dates.</li>
<li><code>twint -u username --database tweets.db</code> — Collect Tweets and save them to a SQLite database.</li>
<li><code>twint -u username --csv --output tweets.csv</code> — Collect Tweets and save them to a CSV file.</li>
<li><code>twint -u username --json --output tweets.json</code> — Collect Tweets and save them to a JSON file.</li>
<li><code>twint -u username --followers</code> — Scrape a user's followers.</li>
<li><code>twint -u username --following</code> — Scrape who a user follows.</li>
<li><code>twint -u username --favorites</code> — Collect all the Tweets a user has favorited.</li>
<li><code>twint -g "48.880048,2.385939,1km" -o tweets.csv --csv</code> — Collect Tweets tweeted by users located within 1 km of a given geographical spot.</li>
</ul>

<p>Run <code>twint --help</code> to see the full list of supported flags and options.</p>

<h3>Python module</h3>

<p>twint can also be used programmatically. All scraping behavior is controlled through a <code>twint.Config()</code> object, which is then passed to one of the runner functions in <code>twint.run</code>:</p>

<p>```python
import twint</p>

<h1>Configure</h1>

<p>c = twint.Config()
c.Username = "username"
c.Limit = 10</p>

<h1>Run</h1>

<p>twint.run.Search(c)
```</p>

<p>Depending on what you want to scrape, call one of the following runners with your <code>Config</code> object:</p>

<p><code>python
twint.run.Search(c)      # Tweets matching the configuration
twint.run.Followers(c)   # A user's followers
twint.run.Following(c)   # Who a user follows
twint.run.Favorites(c)   # Tweets a user has favorited
twint.run.Profile(c)     # A user's profile information
</code></p>

<h3>Configuration options</h3>

<p>The <code>twint.Config()</code> object accepts a wide range of options. Some of the most commonly used ones:</p>

<p>```python
c = twint.Config()</p>

<h1>What to scrape</h1>

<p>c.Username = "username"      # User whose Tweets / followers to scrape
c.Search = "search terms"    # Search terms to filter Tweets by
c.Query = "query"            # Raw query used for the scrape
c.Since = "2015-12-20"       # Only Tweets sent since this date
c.Until = "2016-01-05"       # Only Tweets sent until this date
c.Limit = 100                # Maximum number of Tweets to scrape</p>

<h1>Filters</h1>

<p>c.Popular<em>tweets = False     # Only popular Tweets
c.Retweets = False           # Include retweets
c.Native</em>retweets = False    # Only native retweets
c.Filter<em>retweets = False    # Exclude retweets
c.Min</em>likes = 0              # Minimum number of likes
c.Min<em>retweets = 0           # Minimum number of retweets
c.Min</em>replies = 0            # Minimum number of replies
c.Links = "include"          # include / exclude / only Tweets containing links</p>

<h1>Output and behavior</h1>

<p>c.Store<em>csv = True           # Store Tweets in CSV format
c.Store</em>json = True          # Store Tweets in JSON format
c.Database = "tweets.db"     # Store Tweets in a SQLite database
c.Hide_output = False        # Suppress terminal output</p>

<h1>Advanced options</h1>

<p>c.Custom<em>query = ""          # Use a custom query string
c.Translate = False          # Translate Tweets
c.TranslateSrc = "en"        # Source language for translation
c.TranslateDest = "en"       # Destination language for translation
c.Min</em>wait_time = 0          # Minimum wait time between requests
```</p>

<p>Options like <code>Bearer_token</code> and <code>Guest_token</code> are handled automatically by twint during a scrape, so in most cases you do not need to set them yourself.</p>
<h2>Contributing</h2>

<p>Contributions to twint are welcome and greatly appreciated!</p>

<p>If you'd like to contribute, please follow these steps:</p>

<ol>
<li>Fork the repository at <a href="https://github.com/twintproject/twint">https://github.com/twintproject/twint</a>.</li>
<li><p>Create a new branch for your feature or bug fix:</p>

<p><code>bash
git checkout -b feature/my-feature
</code></p></li>
<li><p>Make your changes and commit them:</p>

<p><code>bash
git commit -m "Add some feature"
</code></p></li>
<li><p>Push your branch to your fork:</p>

<p><code>bash
git push origin feature/my-feature
</code></p></li>
<li><p>Open a Pull Request against the upstream repository.</p></li>
</ol>

<p>For larger changes, it is a good idea to open an issue first to discuss what you would like to change before submitting your Pull Request.</p>
<h2>License</h2>

<p>twint is licensed under the <strong>MIT License</strong>.</p>

<p>Copyright (c) 2018 Cody Zacharias</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>

<p>The full license text is available in the <code>LICENSE</code> file at the root of the repository.</p>
<h2>Description</h2>

<p>Twint is an advanced Twitter scraping tool written in Python that allows for scraping Tweets from Twitter profiles <strong>without</strong> requiring the use of Twitter's official API.</p>

<p>Twint utilizes Twitter's search operators to scrape Tweets from specific users, scrape Tweets relating to certain topics, filter out sensitive information, etc. Twint is able to scrape almost everything from Twitter (except the photos/videos) that is accessible through Twitter's Search. This means it can fetch information like:</p>

<ul>
<li>date &amp; time of Tweet</li>
<li>Tweet</li>
<li>Tweet ID</li>
<li>User ID</li>
<li>Username</li>
<li>Tweet Retweets, Likes, ...</li>
</ul>

<p>That being said, a few things can be done with Twint:</p>

<ul>
<li>Scrape a user's Tweets</li>
<li>Scrape a user's followers/following</li>
<li>Scrape Tweets relating to certain topics</li>
<li>Scrape user information</li>
</ul>

<p>Twint can output the scraped data to a file in various formats:</p>

<ul>
<li>CSV</li>
<li>JSON</li>
<li>SQLite</li>
<li>Elasticsearch</li>
</ul>

<p>In addition, Twint can format the scraped data in a Pandas DataFrame format.</p>

<p>It is distributed as a Python package (<code>twint</code> and <code>twint.storage</code>) with a command-line interface entry point (<code>twint</code>) that can be run directly from the console after installation.</p>
<h2>Requirements</h2>

<p>Twint requires <strong>Python 3.6 or later</strong> (CPython 3.6, 3.7 and 3.8 are supported).</p>

<p>All of its Python dependencies are installed automatically together with the package. The main ones are:</p>

<ul>
<li><code>aiohttp</code> – asynchronous HTTP client</li>
<li><code>aiodns</code> – asynchronous DNS resolver</li>
<li><code>pysocks</code> / <code>aiohttp_socks</code> – SOCKS proxy support</li>
<li><code>pandas</code> – data analysis library (used for the Pandas/DataFrame output)</li>
<li><code>beautifulsoup4</code> – HTML parsing</li>
<li><code>readability-lxml</code> – HTML text extraction</li>
<li><code>fake-useragent</code> – user-agent generation</li>
<li><code>elasticsearch</code> – Elasticsearch client (used by the Elasticsearch output module)</li>
<li><code>googletrans</code> – translation support (installed from the git repository <code>git+https://github.com/x0rzkov/py-googletrans#egg=googletrans</code>)</li>
<li><code>dataclasses</code> – backport of the standard-library <code>dataclasses</code> module, needed on Python 3.6</li>
</ul>

<p>To install twint together with all of its requirements:</p>

<p><code>
pip3 install . -r requirements.txt
</code></p>
<h2>Installation</h2>

<h3>Pip</h3>

<p><code>
pip install twint
</code></p>

<p>or, to install the latest version directly from the GitHub repository:</p>

<p><code>
pip install --upgrade git+https://github.com/twintproject/twint.git
</code></p>

<h3>Git</h3>

<p><code>
git clone https://github.com/twintproject/twint.git
cd twint
pip install . -r requirements.txt
</code></p>

<h3>Docker</h3>

<p>The repository also ships with a <code>Dockerfile</code> that is based on <code>python:3.6-buster</code>, clones the project from GitHub and installs it together with its requirements:</p>

<p>```dockerfile
FROM python:3.6-buster</p>

<p>WORKDIR /root</p>

<p>RUN git clone --depth=1 https://github.com/twintproject/twint.git &amp;&amp; \
    cd /root/twint &amp;&amp; \
    pip3 install . -r requirements.txt</p>

<p>CMD /bin/bash
```</p>

<p>Once installed, the <code>twint</code> command-line tool is available in your environment (it is registered as a console script via the package's entry points, mapping to <code>twint.cli:run_as_command</code>).</p>
<h2>Usage</h2>

<p>You can find a complete list of example queries <a href="https://github.com/twintproject/twint/wiki/Examples">here</a>.</p>

<p><strong>As a command line tool</strong>:</p>

<ul>
<li><code>twint -u username</code> - Scrape all the Tweets of a <em>user</em> (doesn't include <strong>retweets</strong> but includes <strong>replies</strong>).</li>
<li><code>twint -u username -s pineapple</code> - Scrape all Tweets from the <em>user</em>'s timeline containing <em>pineapple</em>.</li>
<li><code>twint -s pineapple</code> - Collect every Tweet containing <em>pineapple</em> from everyone's Tweets (hidden replies not included).</li>
<li><code>twint -u username --since 2015-12-20 --until 2015-12-21</code> - Collect Tweets that were tweeted between 2015-12-20 00:00:00 and 2015-12-21 00:00:00.</li>
<li><code>twint -u username --since 2015-12-20 --until 2015-12-21 --popular-tweets</code> - Collect Tweets that were tweeted between 2015-12-20 00:00:00 and 2015-12-21 00:00:00 <strong>and</strong> order them by the Most Popular.</li>
<li><code>twint -u username --database tweets.db</code> - Collect Tweets from the <em>user</em>'s timeline and save them to a <strong>SQLite database</strong> called <em>tweets.db</em>.</li>
<li><code>twint -u username --csv</code> - Write all scraped Tweets to a <em>csv</em> file.</li>
<li><code>twint -u username --json</code> - Write all scraped Tweets to a <em>json</em> file.</li>
<li><code>twint -u username -o file.csv --csv</code> - Write all scraped Tweets to a file named <em>file.csv</em>.</li>
<li><code>twint -u username --email</code> - Scrape Tweets from a <em>user</em> that contain <strong>gmail/yahoo/hotmail</strong> addresses.</li>
<li><code>twint -u username --phone</code> - Scrape Tweets from a <em>user</em> that contain <strong>phone numbers</strong>.</li>
<li><code>twint -u username --verified</code> - Scrape Tweets from a <em>user</em> that are <strong>verified</strong>.</li>
<li><code>twint -u username --year 2014</code> - Collect Tweets that were tweeted in <strong>2014</strong>.</li>
<li><code>twint -u username --since "2015-12-20 19:30:15" --until "2015-12-31 05:33:22"</code> - Collect Tweets that were tweeted between the two given timestamps.</li>
<li><code>twint -u username --geo 37.783699,-122.409185,1km</code> - Collect Tweets that were tweeted from a <strong>geo location</strong> (GPS coordinates).</li>
<li><code>twint -u username --near "San Francisco, CA"</code> - Collect Tweets that were tweeted near "San Francisco, CA".</li>
<li><code>twint -u username --lang fr</code> - Collect Tweets that were tweeted in <strong>French</strong>.</li>
<li><code>twint -u username --limit 20</code> - Collect only the <strong>first 20 Tweets</strong>.</li>
<li><code>twint -u username --min-likes 100</code> - Collect only Tweets with at least <strong>100 likes</strong>.</li>
<li><code>twint -u username --min-retweets 100</code> - Collect only Tweets with at least <strong>100 retweets</strong>.</li>
<li><code>twint -u username --min-replies 10</code> - Collect only Tweets with at least <strong>10 replies</strong>.</li>
<li><code>twint -u username --followers</code> - Collect a <em>user</em>'s followers.</li>
<li><code>twint -u username --following</code> - Collect the accounts a <em>user</em> follows.</li>
<li><code>twint -u username --favorites</code> - Collect the Tweets a <em>user</em> has favorited.</li>
<li><code>twint -u username --user-full</code> - Collect all the information about a <em>user</em>.</li>
<li><code>twint -u username --profile-full</code> - Slowly collect Tweets from a <em>user</em>'s account and profile.</li>
<li><code>twint -u username --translate</code> - Translate the scraped Tweets (<code>--translate-src</code> and <code>--translate-dest</code> set the source and destination languages).</li>
<li><code>twint -u username --custom-query "..."</code> - Run a custom, raw Twitter search query.</li>
<li><code>twint -u username --format "Tweet ID: {id} | Tweet: {tweet}"</code> - Customize the console output with a format string.</li>
<li><code>twint -u username -es localhost:9200</code> - Save all scraped Tweets to an <strong>Elasticsearch</strong> instance.</li>
</ul>

<p>Run <code>twint --help</code> to see the full list of available command line options.</p>

<p><strong>As a python module</strong>:</p>

<p>```python
import twint</p>

<p>c = twint.Config()
c.Username = "residentevil7"</p>

<h1>Other config parameters</h1>

<p>c.Limit = 100</p>

<p>twint.run.Search(c)
```</p>

<p>Run methods:</p>

<ul>
<li><code>twint.run.Search(twint.Config())</code> - Search for Tweets.</li>
<li><code>twint.run.Profile(twint.Config())</code> - Get user timeline. E.g. Get all Tweets of a user.</li>
<li><code>twint.run.Followers(twint.Config())</code> - Get user's followers.</li>
<li><code>twint.run.Following(twint.Config())</code> - Get user's following.</li>
<li><code>twint.run.Favorites(twint.Config())</code> - Get all Tweets favorited by a user.</li>
<li><code>twint.run.User(twint.Config())</code> - Get user's info.</li>
<li><code>twint.run.Lookup(twint.Config())</code> - Get users' info from user id/username.</li>
</ul>

<p><strong>Storing data as a pandas DataFrame</strong>:</p>

<p>```python
import twint</p>

<p>c = twint.Config()
c.Username = "residentevil7"
c.Pandas = True</p>

<p>twint.run.Search(c)</p>

<p>twint.storage.panda.Tweets_df
```</p>
<h2>Contributing</h2>

<p>Contributions are always welcome! If you have questions, find a bug, or would like to suggest a new feature, feel free to open an issue on the <a href="https://github.com/twintproject/twint">twint GitHub repository</a>. Pull requests are welcome as well.</p>

<p>To work on twint locally:</p>

<ol>
<li><p>Clone the repository:</p>

<p><code>
$ git clone https://github.com/twintproject/twint.git
$ cd twint
</code></p></li>
<li><p>Install twint along with its dependencies:</p>

<p><code>
$ pip3 install . -r requirements.txt
</code></p></li>
</ol>

<p>twint is written in Python (the provided Docker image is based on Python 3.6). By submitting code to the project, you agree that your contributions will be licensed under the MIT License that covers the rest of the project.</p>
<h2>License</h2>

<p>twint is released under the MIT License.</p>

<p>Copyright (c) 2018 Cody Zacharias</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>

<p>The full license text is also available in the <a href="LICENSE">LICENSE</a> file at the root of the repository.</p>
