# System Design Primer

<p align="center">
  <img src="jj3A5N8.png" alt="System design" />
</p>

---

Motivation > Study guide > Contributing > Back-of-envelope calculations > System design topics > System design interview questions with solutions > Object-oriented design interview questions with solutions > System design exercises for practice, testing, and tutoring > Study resources

---

## Motivation

> Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards.

<p align="center">
  <img src="n41Azff.png" alt="System design questions" />
</p>

**Studying for a systems design interview can be daunting.** There is an endless number of topics and resources available to prepare for a system design interview, making it difficult to know where to start.

This repository **organizes** the resources needed to **learn** systems design, **prepares** you for the **interview**, and helps you **refresh** your knowledge of how systems scale.

In addition, this repo contains study materials for general coding interviews, interactive coding challenges, and object-oriented design interviews.

- [Study guide](#study-guide)
- [Back-of-envelope calculations](#back-of-the-envelope-calculations)
- [System design topics](#system-design-topics) — start here for an overview
- [System design interview questions with solutions](#system-design-interview-questions-with-solutions) — real questions with detailed walkthroughs
- [Object-oriented design interview questions with solutions](#object-oriented-design-interview-questions-with-solutions)
- [System design exercises for practice, testing, and tutoring](#system-design-exercises-for-practice-testing-and-tutoring)
- [Anki flashcard decks](#anki-flashcards)

## Contributing

Contributions are welcome!

- Fix an error
- Expand a section
- Add a new section or question
- Translate this document

Review the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute.

## Study guide

### Suggested study path

Depending on your timeline and which areas you'd like to work on, here is a suggested path:

* **You are short on time** — Review the [System design topics](#system-design-topics) summary, then work through a few [System design interview questions with solutions](#system-design-interview-questions-with-solutions).
* **You have more time** — Work through the [System design topics](#system-design-topics) in detail, then complete the [System design interview questions with solutions](#system-design-interview-questions-with-solutions), and go through [Object-oriented design interview questions with solutions](#object-oriented-design-interview-questions-with-solutions).
* **You want to refresh your knowledge** — Browse the [System design topics](#system-design-topics) summaries and focus on the areas you are less familiar with.
* **You want to improve your interactive coding skills** — Work through the [interactive coding challenges](#additional-system-design-interview-questions) in the `solutions` directory, including the hash map, LRU cache, call center, deck of cards, parking lot, and online chat exercises.

<p align="center">
  <img src="n16iOGk.png" alt="Study guide" />
</p>

### What you need to know

| Topic | Under review | First pass | Complete |
|---|---|---|---|
| [Steps to review a system design problem](#steps-to-review-a-system-design-problem) | | | |
| [System design topics: start here](#system-design-topics-start-here) | | | |
| [Non-functional: characteristics of a system](#non-functional-characteristics-of-a-system) | | | |
| [Back-of-envelope calculations](#back-of-the-envelope-calculations) | | | |
| [Consistency patterns](#consistency-patterns) | | | |
| [Availability patterns](#availability-patterns) | | | |
| [Domain name system](#domain-name-system) | | | |
| [Content delivery network (CDN)](#content-delivery-network-cdn) | | | |
| [Load balancer](#load-balancer) | | | |
| [Reverse proxy (web server)](#reverse-proxy-web-server) | | | |
| [Application layer](#application-layer) | | | |
| [Microservices](#microservices) | | | |
| [Service discovery](#service-discovery) | | | |
| [Relational database management system (RDBMS)](#relational-database-management-system-rdbms) | | | |
| [NoSQL](#nosql) | | | |
| [Cache](#cache) | | | |
| [Asynchronism](#asynchronism) | | | |
| [Communication](#communication) | | | |
| [Security](#security) | | | |

## Back-of-the-envelope calculations

Learn how to estimate numbers you might need during a system design interview. Practice with these estimates:

| Metric | Estimate |
|---|---|
| Power of two | 2¹ = 2, 2² = 4, ... 2⁶⁴ ≈ 1.8 × 10¹⁹ bytes |
| Numbers everyone should know | Latency numbers every programmer should know |
| Standard units | bit, byte, KB, MB, GB, TB, PB |

Useful latency numbers (approximate):

| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Mutex lock/unlock | 25 ns |
| Main memory reference | 100 ns |
| Compress 1K bytes with Zippy | 3 µs |
| Send 1K bytes over 1 Gbps network | 10 µs |
| Read 4K randomly from SSD | 150 µs |
| Read 1 MB sequentially from memory | 250 µs |
| Round trip within same datacenter | 500 µs |
| Read 1 MB sequentially from SSD | 1 ms |
| Disk seek | 10 ms |
| Read 1 MB sequentially from disk | 30 ms |
| Packet roundtrip California→Netherlands→California | 150 ms |

Conversion guide:

| Unit | Value |
|---|---|
| 1 KB | 10³ bytes |
| 1 MB | 10⁶ bytes |
| 1 GB | 10⁹ bytes |
| 1 TB | 10¹² bytes |
| 1 PB | 10¹⁵ bytes |

## System design topics: start here

New to system design?

First, you'll need a basic understanding of common principles:

### Steps to review a system design problem

The following is a general framework for approaching a system design problem:

1. **Scope the problem** — Don't make assumptions; ask clarifying questions to understand constraints, use cases, and expected traffic.
2. **Sketch up an initial design** — Draw a rough design based on the use cases and constraints. Identify bottlenecks.
3. **Identify bottlenecks** — Look for parts of the design that will break under heavy load or that violate constraints.
4. **Scale** — Address bottlenecks using scaling techniques: horizontal scaling, caching, load balancing, database partitioning, etc.

Be prepared to go back and forth throughout the interview as new information and constraints surface.

### Non-functional: characteristics of a system

<p align="center">
  <img src="b4YtAEN.png" alt="System characteristics" />
</p>

Key non-functional characteristics to consider:

- **Availability** — the percentage of time the system is operational (e.g. 99.99% uptime)
- **Latency** — the time it takes to transfer a request from its point of origin to its destination
- **Throughput** — the number of requests per second the system can handle
- **Redundancy** — the duplication of critical components to increase reliability
- **Scalability** — the ability to handle increased load by adding resources

### Scalability

#### Load balancing

<p align="center">
  <img src="fNcl65g.png" alt="Load balancer" />
</p>

A **load balancer** distributes incoming client requests among a cluster of servers, improving both availability and performance:

- Prevents requests from going to unhealthy servers
- Prevents overloading resources
- SSL termination
- Session persistence (sticky sessions) with cookies

**Load balancer selection criteria:**
- Round robin, weighted round robin, least connections, least loaded, or random
- Active or passive health checks
- Layer 4 (transport) vs Layer 7 (application) balancing

#### Horizontal scaling

Scale by adding more machines rather than upgrading a single machine:

- **Horizontal scaling** — add more nodes; favors fault tolerance and modularity; may require load balancing and consistency considerations
- **Vertical scaling** — add more power (CPU, RAM) to an existing node; simpler but has hardware limits and a single point of failure

#### Caching

Caching improves page load times and can reduce the load on servers and databases. See the [Cache](#cache) section for details.

#### Database scaling

- **Read replicas** — replicate data across multiple database nodes to spread read traffic
- **Sharding (horizontal partitioning)** — split data across multiple database servers, each holding a subset of the data
- **Denormalization** — trade redundant data for faster reads
- **SQL tuning** — indexes, query optimization, and connection pooling

## System design topics

### Consistency patterns

<p align="center">
  <img src="yB5SYwm.png" alt="Consistency patterns" />
</p>

With multiple copies of the same data, we must decide how to synchronize them so users have a consistent view of the data.

#### Weak consistency

After a write, reads may or may not see it. This approach is chosen when it is acceptable to write on any replica, and the data will eventually sync. Memcached uses weak consistency. Well suited for real-time use cases such as video conferencing.

#### Eventual consistency

After a write, reads will *eventually* see it (typically within milliseconds). Data is replicated asynchronously. DNS and email systems use this approach. Popular with systems such as Dynamo, Riak, and Cassandra.

#### Strong consistency

After a write, reads will see it. Data is replicated synchronously. Well suited for use cases requiring transactions. Systems such as HBase and file systems typically use strong consistency.

### Availability patterns

There are two main patterns to support high availability: **fail-over** and **replication**.

#### Fail-over

- **Active-passive** — active and passive heartbeats; when the active fails, the passive takes over; no downtime unless the failure goes undetected
- **Active-active** — both servers manage traffic, spreading the load

#### Replication

- **Master-slave** — masters serve writes, slaves serve reads; slaves replicate from masters
- **Master-master** — both masters serve reads and writes and coordinate with each other on writes

Disadvantage(s): availability — masters can go down, replication lag can cause data loss, and conflicts may require resolution.

### Domain name system

<p align="center">
  <img src="h9TAuGI.jpg" alt="DNS" />
</p>

A **Domain Name System (DNS)** translates domain names (such as `www.example.com`) to IP addresses. DNS is hierarchical, with slightly different top-level domains (TLDs) such as `.com`, `.net`, `.edu`, and country-level domains.

- **DNS registrars** — manage domain name reservations
- **DNS servers** — resolve domain names to IP addresses
- **DNS records** — A (address), CNAME (canonical name), MX (mail), TXT

DNS resolution flow: browser cache → OS cache → router cache → ISP DNS server → root/authoritative servers.

### Content delivery network (CDN)

<p align="center">
  <img src="4edXG0T.png" alt="CDN" />
</p>

A **content delivery network (CDN)** is a globally distributed network of proxy servers, serving content from locations closer to the user. CDNs cache static content (images, CSS, JavaScript) and can also serve dynamic content, improving latency and reducing load on your origin servers.

- **Push CDNs** — you upload content to the CDN; you control what is cached
- **Pull CDNs** — the CDN fetches content from your servers on first request and caches it; simpler but can result in slower first requests

Disadvantage(s): CDN costs can be significant, and content might be stale if not managed carefully.

### Load balancer

See [Load balancing](#load-balancing) above.

### Reverse proxy (web server)

<p align="center">
  <img src="IOyLj4i.jpg" alt="Reverse proxy" />
</p>

A **reverse proxy** is a server that sits in front of web servers and forwards client requests to those web servers. Benefits:

- Caching
- SSL termination
- Compression
- Load balancing and routing
- Centralized logging and auditing

Examples: Nginx, HAProxy, Varnish.

### Application layer

<p align="center">
  <img src="V5q57vU.png" alt="Application layer" />
</p>

The **application layer** (also known as the web tier) contains the core business logic. It can be scaled horizontally by adding more servers. Statelessness is a key principle: keep the application servers stateless so requests can go to any server. Session data should be stored in a centralized data store such as a database or a cache.

### Microservices

<p align="center">
  <img src="TcUo2fw.png" alt="Microservices" />
</p>

A suite of **microservices** consists of separately deployable services, each responsible for a distinct business capability. Benefits:

- Independently deployable and scalable
- Smaller teams can own individual services
- Technology diversity is possible

Disadvantages: distributed system complexity, operational overhead, and potential latency between services.

### Service discovery

<p align="center">
  <img src="OfVllex.png" alt="Service discovery" />
</p>

**Service discovery** systems help services find each other in dynamic environments where instances come and go. Tools such as Zookeeper, Consul, and etcd provide service registry and health checking.

### Relational database management system (RDBMS)

<p align="center">
  <img src="iF4Mkb5.png" alt="RDBMS" />
</p>

A relational database such as SQL represents data in tables, rows, and columns. Supports **ACID** transactions (Atomicity, Consistency, Isolation, Durability) and structured queries with SQL.

- **Indexing** — speeds up reads at the cost of slower writes and additional storage
- **Normalization** — reduces data redundancy; may require joins
- **Denormalization** — trades redundancy for read performance
- **Replication and sharding** — scale reads and distribute data

### NoSQL

<p align="center">
  <img src="Xkm5CXz.png" alt="NoSQL" />
</p>

NoSQL encompasses a variety of data stores that don't use the traditional relational model:

- **Key-value store** — simplest form; lookup by key (Redis, Memcached, DynamoDB)
- **Document store** — data stored as documents (JSON) (MongoDB, CouchDB)
- **Wide column store** — columns grouped into column families (Cassandra, HBase)
- **Graph database** — nodes and relationships (Neo4j)

Generally favors **BASE** (Basically Available, Soft state, Eventually consistent) over ACID. Choose NoSQL when your data doesn't fit a relational model well, when you need massive scale, or when availability trumps consistency.

### SQL vs NoSQL

| | SQL (RDBMS) | NoSQL |
|---|---|---|
| Data model | Tables with rows and columns | Key-value, documents, wide column, graph |
| Schema | Fixed schema | Flexible schema |
| Transactions | ACID | Typically BASE / eventual consistency |
| Scaling | Vertical (traditionally); sharding is more complex | Horizontal |
| Best for | Structured data, complex queries, transactions | Large volumes, flexible data, high availability |

### Cache

<p align="center">
  <img src="jrUBAF7.png" alt="Cache" />
</p>

Caching improves page load times and reduces load on servers and databases. Caches can exist at many layers: client, CDN, reverse proxy, application server (memory cache), and database.

**Cache patterns:**
- **Cache-aside** — the application is responsible for reading and writing to the cache and the database; the cache does not interact with the database directly
- **Read-through** — the cache sits in line with the database; on a miss, the cache loads from the database
- **Write-through** — data is written to the cache and the database at the same time
- **Write-behind (write-back)** — data is written to the cache and asynchronously written to the database
- **Write-around** — data is written to the database, bypassing the cache

**Cache eviction policies:**
- FIFO (first in first out)
- LIFO (last in first out)
- LRU (least recently used)
- LFU (least frequently used)
- Random replacement

**Distribution:**
- **Client-side caching** — caches on the client
- **CDN** — distributed caching for static content
- **Web server caching** — reverse proxy caching
- **Database caching** — query result caching (e.g. MySQL query cache)
- **Application caching** — in-memory caches such as Memcached and Redis

### Asynchronism

<p align="center">
  <img src="zdCAkB3.png" alt="Asynchronism" />
</p>

Slow workflows should be handled asynchronously, typically with:

- **Message queues** — messages are added to a queue and processed by workers; enables decoupling and buffering
- **Task queues** — describe asynchronous tasks and schedule their execution (e.g. Celery)

**Backpressure** — if queues grow faster than workers can process, backpressure builds; you can limit queue size, scale workers, or shed load.

### Communication

<p align="center">
  <img src="bgLMI2u.png" alt="Communication" />
</p>

#### Hypertext transfer protocol (HTTP)

HTTP is a request-response protocol. Common methods: GET, POST, PUT, DELETE. RESTful APIs leverage HTTP verbs and are stateless, supporting horizontal scaling. HTTP is a higher-level protocol built on TCP.

#### Transmission control protocol (TCP)

TCP provides reliable, ordered, error-checked delivery of a stream of bytes. Used for HTTP, SSH, email (SMTP), and more. A TCP connection is established via a three-way handshake.

#### User datagram protocol (UDP)

UDP is connectionless and provides no guarantees on delivery or ordering — but it has lower overhead and latency. Well suited for streaming, gaming, and VoIP.

#### Remote procedure call (RPC)

RPC allows a program to cause a procedure to execute in another address space as if it were local. Examples: gRPC, Thrift. Useful for internal service-to-service communication.

#### Representational state transfer (REST)

REST is an architectural style enforcing statelessness and a uniform interface using standard HTTP verbs and nouns (URIs). Caching is straightforward, and it is easy to consume from browsers and mobile clients.

### Security

All system design interviews should include considerations around security:

- **Encryption in transit** — TLS/SSL for all client-server communication
- **Encryption at rest** — encrypt sensitive data stored in databases and backups
- **Authentication and authorization** — verify identity and access rights (e.g. OAuth, JWT, session tokens)
- **Input validation and sanitization** — protect against SQL injection, XSS, and CSRF attacks
- **Rate limiting and throttling** — protect against abuse and denial-of-service attacks
- **Secrets management** — keep credentials out of source control; use secret stores

## System design interview questions with solutions

<p align="center">
  <img src="wU8x5Id.png" alt="Short URL architecture" />
</p>

Work through the following past system design interview questions, complete with solutions, diagrams, tradeoffs, and discussions.

| Question | Design documents |
|---|---|
| Design Pastebin.com (or Bit.ly) | [Pastebin](./pastebin/README.md) with [snippets](./pastebin/pastebin.py) and diagrams |
| Design the Twitter timeline (or Facebook feed) | [Twitter](./twitter/README.md) with diagrams |
| Design a web crawler | [Web crawler](./web_crawler/README.md) with MapReduce and snippets |
| Design Mint.com | [Mint](./mint/README.md) with MapReduce and snippets |
| Design the data structures for a social network | [Social graph](./social_graph/README.md) with snippets and diagrams |
| Design a key-value store for a scalable cloud | [Query cache](./query_cache/README.md) with snippets and diagrams |
| Design a function to return the sales rank for the past week | [Sales rank](./sales_rank/README.md) with MapReduce and diagrams |
| Scale a AWS-based application | [Scaling AWS](./scaling_aws/README.md) with diagrams |
| Design a system for the customer support chat / online chat | [Online chat](./online_chat/README.md) |

Each solution includes:

- **Scope the problem** — use cases and constraints with assumptions
- **Back-of-envelope calculations** — estimate traffic, storage, and capacity
- **Sketch a design** — high-level component diagram
- **Optimize the design** — identify bottlenecks and apply scaling techniques
- **Discuss tradeoffs** — consistency vs availability, caching strategies, sharding approaches

Diagrams are provided in PNG format with editable source files (`.graffle` for OmniGraffle).

## Object-oriented design interview questions with solutions

Common object-oriented design interview questions with solutions, discussions, and tradeoffs:

| Question | Solution |
|---|---|
| Design a hash map | [hash_map.py](./solutions/oop_design/hash_map/hash_map.py) with [notebook](./solutions/oop_design/hash_map/hash_map.ipynb) |
| Design a least recently used (LRU) cache | [lru_cache.py](./solutions/oop_design/lru_cache/lru_cache.py) with [notebook](./solutions/oop_design/lru_cache/lru_cache.ipynb) |
| Design a call center | [call_center.py](./solutions/oop_design/call_center/call_center.py) with [notebook](./solutions/oop_design/call_center/call_center.ipynb) |
| Design a deck of cards | [deck_of_cards.py](./solutions/oop_design/deck_of_cards/deck_of_cards.py) with [notebook](./solutions/oop_design/deck_of_cards/deck_of_cards.ipynb) |
| Design a parking lot | [parking_lot.py](./solutions/oop_design/parking_lot/parking_lot.py) with [notebook](./solutions/oop_design/parking_lot/parking_lot.ipynb) |
| Design an online chat (chat server) | [online_chat.py](./solutions/oop_design/online_chat/online_chat.py) with [notebook](./solutions/oop_design/online_chat/online_chat.ipynb) |

Each solution walks through:

1. Clarifying the question and use cases
2. Identifying core objects and their relationships
3. Designing class hierarchies and interfaces
4. Discussing design patterns, tradeoffs, and extensibility

## System design exercises for practice, testing, and tutoring

<p align="center">
  <img src="MzExP06.png" alt="Interactive exercises" />
</p>

In addition to the study materials, this repository contains **interactive coding challenges** you can run in your browser or locally via the included Jupyter notebooks (`.ipynb` files). These are useful for self-study, testing your knowledge, or tutoring others.

## Anki flashcards

The provided [Anki](https://apps.ankiweb.net/) flashcard decks use spaced repetition to help you retain key system design concepts:

- **System Design.apkg** — covers the system design topics in this repository
- **System Design Exercises.apkg** — flashcards for the system design interview questions with solutions
- **OO Design.apkg** — flashcards for the object-oriented design interview questions with solutions

To use the decks:

1. Download [Anki](https://apps.ankiweb.net/) for your platform
2. Import the `.apkg` files
3. Review the cards on a spaced repetition schedule

## Study resources

Additional resources to deepen your system design knowledge:

- [High Scalability](http://highscalability.com/)
- [Netflix Architecture](https://netflixtechblog.com/)
- [Google Research Publications](https://research.google/pubs/)
- [Facebook Engineering](https://engineering.fb.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [The Art of Scalability](https://www.amazon.com/Art-Scalability-Architecture-Enterprise-Organizations/dp/0134052807)
- [Designing Data-Intensive Applications](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321)
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)

## Translations

Thanks to the community, this guide is available in additional languages:

- [简体中文 (Chinese — Simplified)](./README-zh-Hans.md)

See [TRANSLATIONS.md](TRANSLATIONS.md) for details on how to contribute a new translation.

## License

This project is licensed under the terms of the [LICENSE.txt](LICENSE.txt) file — provided under a Creative Commons license for the text and an MIT-style license for the source code, depending on the component. See the license file for full details.

## Credits

This project draws inspiration and material from many publicly available articles, papers, engineering blogs, and open source projects. Review the full list of sources and credits in the repository documentation.

---

**Good luck with your studies and your interviews!** If you find this material useful, consider contributing improvements, additional solutions, or translations.
