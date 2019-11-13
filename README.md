# faster_tcp_text_reuse

A faster set of routines for find text reuse in the EEBO-TCP corpus, building upon an earlier repo [an earlier repo](https://github.com/spenteco/tcp_text_reuse), which was organized/optimized around finding quotations from the Bible.  This repo, on the other hand, is more generalized, and is intended as a basis for finding **all** text reuse in the corpus.

## Components

The important stuff:

* **01_all_data_prep_steps.ipynb** -- Takes morphadorned EEBO-TCP TEI XML (not the XML the TCP ships, but XML derived from the TCP's SGML), and creates two sets of data: 1) a pickled python data structure for each file (all 63,000 of them) which contains lists of tokens, ngram shingles, and the positions of the ngram shingles in the tokens; and 2) a single, very large sqlite database which contains every nrgam shingle in the corpus.

* **02_shingle_matching_from_sqlite3.ipynb** -- For any text (or, obviously, for any text in a lsit of texts), answers the question, "What sequences of tokens in this text occurs in other texts?"  Which is more or less the same as asking, "What texts does this text quote, and what texts quote this text?"  Run times for this process depends on a) the kind of device on which the sqlite database is mounted (I have my copy on an SSD); b) the state the file system cache (things run faster of the process finds pages from the database in the cache); and c) the number of texts which share sequences of tokens with the text being matched.  On my workstation, I'm seeing times like:

>   Herrick, *Hesperides*: 5 seconds

>   Spenser, *Faerie Queene*: 20 seconds

>   Browne, *Hydriotaphia*: 3 seconds

>   *Englands Parnassus*, 9 seconds

>   Burton, *Anatomy*, 334 seconds

>   *Book of Common Prayer* (1553), 3,346 seconds (i.e., 1 hour)

I've experimented with several different approaches, and I don't think I'm going to get times much better than these . . . 

* **matching_functions.py** -- Functions used by the notebooks.

* **all_to_all_html_outputs** -- Human readable results are written here.

* **match_worker.py** -- A version of the code in 02_shingle_matching_from_sqlite3.ipynb which runs as a stand-alone script.

* **match_controller.py** -- A script which manages running match_worker.py processes in parallel.  Starts new match_workers as old ones finish.  Checks to see if a text has been processed before starting a match_worker for it.  Kills long-running match_worker processes so we can finish as many short-running processes as possible.

## Next steps

1.  Desk check *Englands Parnassus*, which seems like a good test case.  Are the results correct?

2.  Enhance the output reports.

3.  Let it run over the week of Thanksgiving.  How many can we get done?

4.  Figure out what to do about the highly reused texts (e.g., Bibles) which won't run through these processes.




