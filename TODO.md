h2. TODO

* Alias: boredlater - maps to `borednow -a`
* Future: Add support for online/offline tasks
* Future: Allow importing a plain text file containing list of items

h3. DONE

* Main command: borednow
	* Reads/write entries in a JSON file
	* No options: pulls a random entry
	* Option `-a` or `--add`: Adds an entry to the file
	* Option `-d` or `--done`: Marks last displayed entry as done
	* Option `-s` or `--skip`: Skips the last displayed entry
		* If skip has been chosen too many times in a row, display a warning and refuse to accept any more skips until the current task has been marked as done
		* If not, display the next task
