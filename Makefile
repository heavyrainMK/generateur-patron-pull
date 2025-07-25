.PHONY: test

test:
	@echo "=== Lancement des tests unitaires ==="
	PYTHONPATH=./backend python -m unittest discover -s backend -p 'test_*.py' -v -b