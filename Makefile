PYTHON = python
PYTEST = $(PYTHON) -m pytest

test_pil:
	env KIVY_TEXT=pil $(PYTEST) ./tests

test_sdl2:
	env KIVY_TEXT=sdl2 $(PYTEST) ./tests

test: test_pil test_sdl2
