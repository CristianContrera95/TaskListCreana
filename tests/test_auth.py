import pytest


@pytest.mark.asyncio
async def test_auth_token_fixture(auth_token):
    """Test only the auth_token fixture to ensure user creation and login works."""
    assert isinstance(auth_token, str)
    assert len(auth_token) > 10
