.PHONY: test test-visual test-visual-baseline test-integration lint

test:
	python -Wd manage.py test

test-visual:
	VISUAL=1 DISPLAY=:99.0 python -Wd manage.py test tests.visual

test-visual-baseline:
	VISUAL=1 DISPLAY=:99.0 NEEDLE_SAVE_BASELINE=1 python -Wd manage.py test tests.visual

test-integration:
	python -Wd manage.py test tests.integration

lint:
	flake8 material/
