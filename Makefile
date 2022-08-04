PYTHON_INPTERPETER=python
run:
	$(PYTHON_INPTERPETER) _agnes_3.0.py

setup: requirements.txt
	$(PYTHON_INPTERPETER) pip install -r requirements.txt

clean:
	rm -rf __pycache__

SEMGREP_IMAGE=returntocorp/semgrep
SEMGREP_OUTPUT=semgrep-audit.txt
semgrep-audit:
	docker pull $(SEMGREP_IMAGE)
	docker run --rm -v "$$(pwd):/src_folder" -u $$(id -u) $(SEMGREP_IMAGE) --metrics=off --config=p/r2c-ci \
				--output=/src_folder/$(SEMGREP_OUTPUT) /src_folder --verbose hmm