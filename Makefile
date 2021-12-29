.PHONY: clean develop format publish
develop:
	poetry install

clean:
	rm -rf build dist *egg-info

publish: clean
	poetry build
	poetry publish

format:
	poetry run black check_git_repos
