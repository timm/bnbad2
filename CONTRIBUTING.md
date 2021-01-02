# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have:

- a code of [conduct](#conduct), please follow it in all your interactions with the project.
- a set of local [idioms](#idioms), used when we write Python
- a set of [standards](#standards) that enable more experimentation with this systems.

## Idioms

- Keep lines under 70 characters.
  - Why? Readability.
- Keep defs short.
  - Why? See first point.
- Indent with 2 spaces.
  - Why? See first point.
- Use `i`, not `self` 
  - Why? See first point.
- All code in `/src`
- All test data in `/src/tests`
- Any shell tricks in `/etc/ish`
- Document code using `pycco`.
- No doc strings 
  - Why? Pycco does not treat them well.
- Most classes, defs, get a one line comment before each.
  - Why? Pycco treats these well
- Code using autopep8, disabling errors E261 and E302 
  - Why? these two errors add silly blank lines to pycco output.
- Most files start with `from it import *` (exceptions: `boot.py` and `it.py``)
- Test by adding the following code  to the end of the file:

```python
# ---
# main
if __name__ == "__main__":
  if "--test" in sys.argv:
    ok(csvok,splitok) #<==== names of test functions, containg asserts
```

## Standards

- Defaults are stored in it.py
- If an instance uses `it` then it creates its own copy of the relevant values in
  `i.it`.
- Instances pause after `__init__` so programmers (or hyperparameter
  optimizers) can adjust `i.it` before the real work starts.

## Conduct

<img src="https://github.com/timm/bnbad2/raw/main/etc/img/conduct.png"
     align=right width=400>

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [INSERT EMAIL ADDRESS]. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
