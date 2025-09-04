from app.models import User, ScriptGroup, Script


def test_user_password(session):
    user = User(username="alice", email="alice@example.com")
    user.set_password("secret")
    session.add(user)
    session.commit()

    db_user = User.query.filter_by(username="alice").first()
    # password should be hashed and check_password should work
    assert db_user is not None
    assert db_user.username == "alice"
    assert db_user.check_password("secret")
    assert not db_user.check_password("wrongpass")


def test_user_scriptgroup_relationship(session):
    user = User(username="bob", email="bob@example.com")
    user.set_password("hunter2")

    group = ScriptGroup(name="Test Group",
                        description="Example group", author=user)

    session.add(user)
    session.add(group)
    session.commit()

    db_group = ScriptGroup.query.filter_by(name="Test Group").first()

    assert db_group is not None
    assert db_group.author == user
    assert user.script_groups[0] == db_group


def test_scriptgroup_script_relationship(session):
    user = User(username="charlie", email="charlie@example.com")
    user.set_password("pass123")

    group = ScriptGroup(
        name="Utilities", description="Utility scripts", author=user)
    script = Script(title="Hello", content="print('hello world')",
                    author=user, group=group)

    session.add_all([user, group, script])
    session.commit()

    db_script = Script.query.filter_by(title="Hello").first()

    assert db_script is not None
    assert db_script.author == user
    assert db_script.group == group
    assert group.scripts[0] == db_script
    assert user.scripts[0] == db_script
