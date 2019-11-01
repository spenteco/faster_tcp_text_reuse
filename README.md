# faster_tcp_text_reuse

A faster set of routines for find text reuse in the EEBO-TCP corpus, building upon an earlier repo [an earlier repo](https://github.com/spenteco/tcp_text_reuse), which was organized/optimized around finding quotations from the Bible.  This repo, on the other hand, is more generalized, and is intended as a basis for finding **all** text reuse in the corpus.

## Components

The important stuff:

* **01_all_data_prep_steps.ipynb** -- Takes morphadorned EEBO-TCP TEI XML (not the XML the TCP ships, but XML derived from the TCP's SGML), and creates two sets of data: 1) a pickled python data structure for each file (all 63,000 of them) which contains lists of tokens, ngram shingles, and the positions of the ngram shingles in the tokens; and 2) a single, very large sqlite database which contains every nrgam shingle in the corpus.

* **02_shingle_matching_from_sqlite3.ipynb** -- For any text (or, obviously, for any text in a lsit of texts), answers the question, "What sequences of tokens in this text occurs in other texts?"  Which is more or less the same as asking, "What texts does this text quote, and what texts quote this text?"  Run times for this process depends on a) the kind of device on which the sqlite database is mounted (I have my copy on an SSD); b) the state the file system cache (things run faster of the process finds pages from the database in the cache); and c) the number of texts which share sequences of tokens with the text being matched.  On my workstation, I'm seeing times like:

>   Herrick, *Hesperides*: 53 seconds

>   Spenser, *Faerie Queene*: 48 seconds

>   Browne, *Hydriotaphia*: 10 seconds

>   *Englands Parnassus*, 28 seconds

I don't have times for longer texts . . . 

* **matching_functions.py** -- Functions used by the notebooks.

* **all_to_all_html_outputs** -- Human readable results are written here.

## Next steps

1.  Get timings for some longer texts (Burton, the Book of Common Prayer, and the Geneva Bible).

2.  Migrate the function in 02_shingle_matching_from_sqlite3.ipynb to some parallelized process, and try running it on everything.




