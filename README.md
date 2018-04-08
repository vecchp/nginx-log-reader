# Notes
* There is no need for your program to parse the timestamps within the log.
* Your program should not be designed to read and process an entire log at once.
* We are effectively tailing the log file and should consider log rotation
* Each line in the output file should be terminated by a single newline (‘\n’).
* Note that the metrics do not need to appear in any particular order,
* as long as all four required metrics exist (and the optional error routes counts also appear if they are present in the original log).
* There is no need to separate/delimit consecutive five-second intervals.
* The sum of all error route counts should equal the “50x” count.