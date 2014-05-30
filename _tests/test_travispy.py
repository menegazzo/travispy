from travispy import TravisPy



#===================================================================================================
# Test
#===================================================================================================
class Test:

    def test_accounts(self):
        travis = TravisPy.github_auth('9f6cce04ce8fee42519c256fe903836afc262833')

        accounts = travis.accounts(all=True)
        assert len(accounts) == 2

        assert accounts[0].id == 72481
        account = travis.account(72481)
        assert account.name == 'Fabio Menegazzo'
        assert account.login == 'menegazzo'
        assert account.type == 'user'
        assert account.repos_count == 6
        assert not hasattr(account, 'subscribed') # Only for Pro and Enterprise

        assert accounts[1].id == 17781
        account = travis.account(17781)
        assert account.name == 'ESSS'
        assert account.login == 'ESSS'
        assert account.type == 'organization'
        assert account.repos_count == 84
        assert not hasattr(account, 'subscribed') # Only for Pro and Enterprise

        account = travis.account(123)
        assert account is None
