# ExtendSenticNet

## Python dependencies:
- [NLTK](http://www.nltk.org/install.html)
- [Enchant](http://pythonhosted.org/pyenchant/tutorial.html)
	- $ pip install pyenchant

## Steps:
1. Run the script _extract_new_concepts.py_ using the command
	``$ python extract_new_concepts.py``
	This script extracts concepts from other lexicons.

2. Run this command after running the above command.
	``$ python add_concepts.py``

OR

1. Run the bash script.
	``$ sh run.sh``

## OUTPUT file:
- The final output file: `senticnet_new_data.py`
- The output is in the form of a senticnet python data file.

## More ways to extend SenticNet:
1. Add concepts from other lexicons.
2. Build module for crowdsourcing option.
	- Using Flask and HTML
3. Check for conflicts in SenticNet and other lexicons.
4. Build an API for SenticNet with response in both JSON and XML.