# rs-template

This is a template repo demonstrating best practices. You can make your own repo from this template, which should save you a lot of work! Just be sure to find-and-replace for "rs-template", "rs_template", and "dennisbrookner" and update everything.

This file is a guide to the core elements that your project should have. In some cases, you may opt for a reasonable alternative, but all of this core functionality should be present.
  
## General organization

The following files in this repo should be adapated for your repo:

### [`pyproject.toml`](/pyproject.toml) configuration file
This is the configuration file for the package. The example in this repo is a good starting point. Some things to note:
 - I recommend copying the `[build-system]` and `[tool.hatch.version]` blocks exactly, and including `dynamic = ["version"]` in the `[project]` block. This allows you to version your package through numbered "releases" on GitHub. There are other ways to do this, but I think this is the best one.
 - There are three different types of dependencies in this file. First, the core `dependencies = ` in the `[project]` block are python packages which are required for your package to function. The `[project.optional-dependencies]` block adds two more types of dependencies:
     - `test`: Any packages necessary to run the test suite.
     - `docs`: Any packages necessary to build the package documentation locally. More on this below.

### [`setup.py`](/setup.py) legacy file
Using `setup.py` to define package configuration and installation is deprecated. However, for legacy reasons, the `setup.py` file must exist. You can adapt the example in this repo.

### [`LICENSE`](/LICENSE)
Pick an open-source license to use, or copy the one here (MIT license).

### [`tox.ini`](/tox.ini)
Copy and adapt this file. This file defines configurations for GitHub actions that will be run.

### [`.gitignore`](/.gitignore)
Cookie-cutter python gitignore file.

## Code
The actual code for your package lives in the `/src/{package-name}` directory. This folder **must** contain an `__init__.py` file, even it is empty. Ideally, use the `__init__.py` file to define what can be imported from your package.

### Code for command-line utilities
Command-line utilities should be structured such that the utility can be called by calling some function, likely the `main` function. Then, you can add the following to your `pyproject.toml` to give this utility a name and make it available from the command line:

```toml
[project.scripts]
"rs.template" = "rs_template._command_line:main"
```

## Docs
The `/docs` folder contains the necessary files to build package documentation. The files `make.bat` and `Makefile` are entirely cookie-cutter and can be copied exactly.

### `conf.py` configuration file for docs
There are lots of fun options here, but I recommend the sensible defaults in the example file. 
  
Note that if your documentation is to include a python API reference, you must include `"sphinx.ext.autodoc"` in `extensions = `. If your documentation is to include a command-line API reference, you must include `"sphinxcontrib.autoprogram"`.
  
If you want your documentation to include rendered jupyter notebooks, you can find code for this in various commented-out options in this file.

Note that the [`"myst_parser"`](https://myst-parser.readthedocs.io/en/latest/) extension allows pages to be written in a blend of markdown and reStructuredText. There are examples of this throughout the documentation.

### `index.md`: Your homepage
All websites need a homepage! This file can be written in markdown, and will be rendered into HTML based on the theme that you've picked. The only essential non-markdown element is the table of contents; see the `/docs/index.md` file in this repo for an example of the syntax.

### Building docs locally
Building docs locally is easy!

 1. Install your package, including the `[docs]` dependencies. Do this by navigating into the package directory and calling `pip install -e ".[docs]"`
 2. Navigate into the `/docs` directory and call `make html`. This will build the package documentation and place it in the `/docs/_build` directory.
    - Note that when repeatedly building documentation, you should call `make clean` each time, followed by `make html`.
 3. Open the file `/docs/_build/html/index.html` in your browser. This is your site! Links to other pages in the site should all work, so you can explore the documentation here.

## Tests

This template repo just has a placeholder test function. Check out [reciprocalspaceship](https://github.com/rs-station/reciprocalspaceship/tree/main/tests) for a good example of what more fleshed-out tests should look like.

## Workflows
You package should contain (at least) these four workflows, which live in the [`.github/workflows`](/.github/workflows/) folder.

### [`ci.yml`](/.github/workflows/ci.yml)

CI stands for "continuous integration". This is the workflow that actually builds your python package. Any time there is either a push or a pull to the main branch of your repo, this workflow will run and build your package.

Additionally, when you create a new version of your package (by making a new release) this workflow is responsible for deploying your latest version to PyPI.

### [`build_docs.yml`](/.github/workflows/build_docs.yml)

This workflow will build your package's documentation and deploy it online. This will be run any time that there is a push to the main branch of your repo. Note that this means that the online documentation may be "ahead" of the package version found on PyPI.

### [`test_docs.yml`](/.github/workflows/test_docs.yml)

This workflow is run on *pull requests* to the main branch. It builds your documentation, but does not deploy it online. This ensures that any changes made in your PR do not break the documentation.

### [`cron.yml`](/.github/workflows/cron.yml)

This workflow ensures that your package has not been broken by any unexpected changes to dependencies. You can configure it to run on a schedule.

## Essential Git / GitHub tasks

Some final chores that you'll need to do to get your package up and running. Some of these are things that you'll need to do online, even after creating this repo as described above. They can be a little tricky, but I'll describe them here as best I can!

### Creating an "orphan" `gh-pages` branch

The architechture described here allows GitHub to build your documentation and then deploy it to the `gh-pages` branch. For this to work, you want to make a branch for your repo called `gh-pages` which is an "orphan", e.g., it just lives in its own world and does not track changes with any other branches.

The easiest way to do this is from the command line. Just be careful! Make sure that you have successfully switched to your `gh-pages` branch before you `git rm` everything.

```bash
# make the orphan branch
git checkout --orphan gh-pages

# preview files to be deleted
git rm -rf --dry-run .
# actually delete the files
git rm -rf .

# make an empty index.html
touch index.html
git add index.html
git commit -m "initial commit to gh-pages branch"

# push the gh-pages branch online
git push origin gh-pages

# get back to the main branch
git checkout main
```

You then have to tell GitHub about this change. In settings, you want to choose "deploy from a branch" as your source, and deploy from gh-pages, root directory. It should look like this:

![Screenshot of github settings](/docs/images/ghpages_settings.png)

Now GitHub will look at the `gh-pages` branch and send whatever is there to rs-station.github.io/{your-repo}. You should be able to run your `build_docs` workflow, and your content will end up on the internet!

#### Don't forget the `.nojekyll` file

In a silly turn of events, all of the style information for the website lives in a folder with a leading underscore, and by default, GitHub *ignores* directories with leading underscores. You override this behavior by creating an empty file on the `gh-pages` branch called `.nojekyll`. (It's possible you could have done this above when you were creating things from the command-line, but I'm not sure.)

### PyPI

At this point, your package should be `pip`-installable via the `git+` syntax, e.g.:
```bash
pip install git+https://github.com/rs-station/rs-template.git
```
but your goal is probably to put your package on [PyPI](https://pypi.org/), such that it can be `pip`-installed directly.

The process of sending a package to PyPI is described [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/). I recommend following this tutorial, including sending your package to TestPyPI as a test.

Once you've sent 