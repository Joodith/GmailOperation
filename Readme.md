Steps for running the script:
1. pip install requirements.txt


2. python main.py -s num 

Here num is the number of gmail messages to be stored locally for testing.The argument is mandatory.This must be done for the database,tables and the rows to get created

3. python main.py -r rule_no

rule_no is specified in rules.json file and thus can be used for executing a particular rule.

If further rules are to be added,they can be done in rules.json file.
Each rule must have list of condition tuples,predicate and a list of actions to be performed

Note:  client_secret.json is needed for gmail authorisation and it is stored as enviroment variable