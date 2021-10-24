import config.app_env as env

if env.data_lake_runtime == 'vm':
    pass
 

elif env.data_lake_runtime == 'local':
 GET_HOLDING_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/holding'
 CREATE_HOLDING_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/holding'
 GET_INVESTMENT_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/investment'
 CREATE_INVESTMENT_API = 'http://localhost:8001/v1/api/user/{}/portfolio/{}/investment'
 GET_WATCHLSIT_API = 'http://localhost:8001/v1/api/user/{}/watchlist'
 GET_USER_PORTFOLIO_API = 'http://localhost:8001/v1/api/user/{}/portfolio'
