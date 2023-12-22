import nox


@nox.session
def tests(session):
    """Run the test suite."""
    tests = session.posargs or ["tests/"]
    env = {"VIRTUAL_ENV": session.virtualenv.location}
    session.run("pipenv", "install", "--dev", external=True, env=env)
    session.run("pytest", *tests, env=env)


@nox.session
def lint(session):
    session.run("flake8")
