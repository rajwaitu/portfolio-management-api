env = 'prod'

if env == 'prod':
 GET_HOLDING_API = ''
 GET_INVESTMENT_API = ''
 CREATE_INVESTMENT_API = ''
 GET_WATCHLSIT_API = ''
 GET_USER_PORTFOLIO_API = ''

elif env == 'local':
 GET_HOLDING_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/holding'
 GET_INVESTMENT_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/investment'
 CREATE_INVESTMENT_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/investment'
 GET_WATCHLSIT_API = 'http://localhost:8001/v1/api/user/{}/watchlist'
 GET_USER_PORTFOLIO_API = 'http://localhost:8001/v1/api/user/{}/portfolio'
