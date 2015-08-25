1. Chipotle data exploration
	* Columns
		1. The first column appears to be an order ID, which probably represents a single transaction made up of one or more items
		2. The second column appears to be the quantity of the item purchased for that order
		3. The third column appears to be the name of the item
		4. The fourth column appears to be an optional field that further describes the item
		5. The fifth column appears to be price for that quantity of items
	* Rows
		1. Each row appears to be an item of an order
	```head -n5 chipotle.tv```
2. There appear to be 1834 orders
	```
	tail -n1 chipotle.tsv
	cut -f1,1 chipotle.tsv | uniq | wc -l	
	```
3. There are 4623 lines
	```wc -l chipotle.tsv```
4. test