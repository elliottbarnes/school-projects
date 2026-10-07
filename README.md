# School Projects

A curated collection of original coursework code demonstrating algorithms, networking, concurrency, computer vision, data structures, and database design in C, Java, Python, JavaScript, and SQL.

**[Open the interactive Memory Lab](https://elliottbarnes.github.io/school-projects/)** — edit page references, compare FIFO/LRU/OPT, step through frame replacements, and translate a 32-bit virtual address.

## Run the completed example

Requires Node.js 24+, Python 3, and a C compiler (`cc`) for the native comparison tests. No package installation is needed.

```sh
node --test
node scripts/check-demo.mjs
python3 -m http.server 4177 --bind 127.0.0.1 --directory demo
```

Open **http://localhost:4177**. The browser lab accompanies C Assignments 7 and 8. Tests compile the C programs with warnings as errors and compare every trace row against the browser algorithms on 30 deterministic cases. Known fault totals and the FIFO anomaly provide independent examples. The updated C programs validate bounded inputs and correct the historical LRU victim-selection bug.

This is a complete runnable slice of an academic archive, not a claim that all historical exercises are finished products. The remaining areas below retain their own prerequisites and limitations. The Pages workflow publishes only `demo/`, excluding reports, datasets, and native source artifacts.

## Projects

| Project | Technologies | What is included |
|---|---|---|
| [AI in computer games](projects/ai-in-computer-games/) | C++ | Historical overview only; source is withheld because the supplied framework prohibits redistribution. |
| [Computer vision](projects/computer-vision/) | Python, Keras, OpenCV | Source for an emotion-classification experiment; datasets, trained models, papers, and imagery are omitted. |
| [Search algorithms](projects/search-algorithms/) | JavaScript | Historical overview only; grading files, instructor solutions, and course scaffolding are omitted. |
| [Decision tree](projects/decision-tree/) | Python, NumPy | Group-authored decision-tree growth, pruning, evaluation, and display code. |
| [Image processing](projects/image-processing/) | Java | Group-authored corner-response and derivative-of-Gaussian algorithm code. |
| [Databases](projects/databases/) | SQL | Normalization notes and queries written against the Chinook schema. |
| [Networking](projects/networking/) | Java | A simple line-oriented client/server exercise with credentials supplied through environment variables. |
| [C programming](projects/c-programming/) | C, POSIX threads | Small programs covering processes, threads, synchronization, memory, and page replacement. |

Each directory documents its scope, attribution, prerequisites, and limitations. These are archival learning projects: some depend on older libraries or omitted datasets, and the repository does not claim that every historical exercise is production-ready.

## Attribution

Individual project READMEs identify collaborators where the source came from group work. The curation adds documentation and removes private or restricted material; it does not claim exclusive authorship of group projects.

## Repository history

This is a clean public snapshot with new history. It includes reviewed original code and concise documentation while omitting course-provided or private academic material, generated artifacts, and dependencies that cannot be redistributed. Complete academic histories remain in private archival repositories.
