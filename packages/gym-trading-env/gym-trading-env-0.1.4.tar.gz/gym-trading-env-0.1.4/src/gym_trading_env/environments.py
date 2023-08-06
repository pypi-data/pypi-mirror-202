import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np
import datetime
import glob
from pathlib import Path    

from collections import Counter
from .utils.history import History
from .utils.portfolio import Portfolio, TargetPortfolio

import tempfile, os
import warnings
warnings.filterwarnings("error")

class TradingEnv(gym.Env):
    """A trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}
    def __init__(self,
                df : pd.DataFrame,
                positions : list = [0, 1],
                reward_function = lambda history : np.log(history["portfolio_valuation", -1] / history["portfolio_valuation", -2]),
                windows = None,
                trading_fees = 0,
                borrow_interest_rate = 0,
                max_leverage = None,
                portfolio_initial_value = 1000,
                initial_position = 0,
                name = "Stock",
                ):
        self.name = name
        self._set_df(df)
        self.positions = positions
        self.reward_function = reward_function
        self.windows = windows
        self.trading_fees = trading_fees
        self.borrow_interest_rate = borrow_interest_rate
        self.max_leverage =max_leverage
        self.portfolio_initial_value = float(portfolio_initial_value)
        self.initial_position = initial_position

        self.action_space = spaces.Discrete(len(positions))
        self.observation_space = spaces.Dict(
            {
                "features": spaces.Box(
                    self._obs_array.min() if self._nb_features > 0 else 0,
                    self._obs_array.max() if self._nb_features > 0 else 1,
                    shape = (self._nb_features, self.windows) if self.windows is not None else (self._nb_features, )
                ),
                "position": spaces.Box(-1, 1)
            }
        )

    def _set_df(self, df):
        self._features_columns = [col for col in df.columns if "feature" in col]
        self._info_columns = list(set(list(df.columns) + ["close"]) - set(self._features_columns))
        self._nb_features = len(self._features_columns)

        self.df = df
        self._obs_array = np.array(self.df[self._features_columns])
        self._info_array = np.array(self.df[self._info_columns])
        self._price_array = np.array(self.df["close"])

    
    def _get_ticker(self, delta = 0):
        return self.df.iloc[self._step + delta]
    def _get_price(self, delta = 0):
        return self._price_array[self._step + delta]

    def _leverage_check(self, portfolio_distribution, price):
        if (portfolio_distribution["borrowed_asset"] * price + portfolio_distribution["borrowed_fiat"]) > 0.95*self.max_leverage * (portfolio_distribution["asset"] * price + portfolio_distribution["fiat"]):
            return True
        return False
    

    def _get_obs(self):
        if self.windows is None: _step_index = self._step
        else: _step_index = np.arange(self._step + 1 - self.windows , self._step + 1)
        return {
            "features" : self._obs_array[_step_index],
            "position" : self._position
            }
    
    def reset(self, seed = None):
        super().reset(seed = seed)
        self._step = 0
        self._limit_orders = {}
        if self.windows is not None: self._step = self.windows

        self._portfolio  = TargetPortfolio(
            position=self.initial_position,
            value= self.portfolio_initial_value,
            price = self._get_price()
        )
        self._position = self.initial_position
        self.historical_info = History(max_size= len(self.df))
        self.historical_info.set(
            step = self._step,
            date = self.df.index.values[self._step],
            action = None,
            position = self._position,
            data =  dict(zip(self._info_columns, self._info_array[self._step])),
            portfolio_valuation = self.portfolio_initial_value,
            portfolio_distribution = self._portfolio.get_portfolio_distribution(),
            reward = 0,
        )
        return self._get_obs(), self.historical_info[0]

    def _trade(self, position, price = None):
        self._portfolio.trade_to_position(
            position, 
            price = self._get_price() if price is None else price, 
            trading_fees = self.trading_fees
        )
        self._position = position

    def _take_action(self, position):
        if position != self._position:
            self._trade(position)
    
    def _take_action_order_limit(self):
        if len(self._limit_orders) > 0:
            ticker = self._get_ticker()
            for position, params in self._limit_orders.items():
                if position != self._position and params['limit'] <= ticker["high"] and params['limit'] >= ticker["low"]:
                    self._trade(position, price= params['limit'])
                    if not params['persistent']: del self._limit_orders[position]


    
    def add_limit_order(self, position, limit, persistent = False):
        self._limit_orders[position] = {
            'limit' : limit,
            'persistent': persistent
        }
    
    def step(self, position_index = None):
        if position_index is not None: self._take_action(self.positions[position_index])
        self._step += 1

        self._take_action_order_limit()
        price = self._get_price()
        self._portfolio.update_interest(borrow_interest_rate= self.borrow_interest_rate)
        portfolio_value = self._portfolio.valorisation(price)
        portfolio_distribution = self._portfolio.get_portfolio_distribution()
        done, truncated = False, False
        if self.max_leverage is not None:
            done = self._leverage_check(portfolio_distribution, price)
        if self._step >= len(self.df) - 1:
            truncated = True
        
        self.historical_info.add(
            step = self._step,
            date = self.df.index.values[self._step],
            action = position_index,
            position = self._position,
            data =  dict(zip(self._info_columns, self._info_array[self._step])),
            portfolio_valuation = portfolio_value,
            portfolio_distribution = portfolio_distribution, 
            reward = 0
        )
        reward = self.reward_function(self.historical_info)
        self.historical_info["reward", -1] = reward
        return self._get_obs(),  self.reward_function(self.historical_info), done, truncated, self.historical_info[-1]
    
    def save_for_render(self, dir = "render_logs"):
        assert "open" in self.df and "high" in self.df and "low" in self.df and "close" in self.df, "Your DataFrame needs to contain columns : open, high, low, close to render !"
        columns = list(set(self.historical_info.columns) - set([f"date_{col}" for col in self._info_columns]))
        history_df = pd.DataFrame(
            self.historical_info[columns], columns= columns
        )
        history_df.set_index("date", inplace= True)
        history_df.sort_index(inplace = True)
        render_df = self.df.join(history_df, how = "inner")
        
        if not os.path.exists(dir):os.makedirs(dir)
        render_df.to_pickle(f"{dir}/{self.name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pkl")

class MultiDatasetTradingEnv(TradingEnv):
    def __init__(self, dataset_dir, preprocess, *args, **kwargs):
        self.dataset_dir = dataset_dir
        self.preprocess = preprocess
        self.dataset_pathes = glob.glob(self.dataset_dir)
        self.dataset_nb_uses = np.zeros(shape=(len(self.dataset_pathes), ))
        super().__init__(self.next_dataset(), *args, **kwargs)

    def next_dataset(self):
        # Find the indexes of the less explored dataset
        potential_dataset_pathes = np.where(self.dataset_nb_uses == self.dataset_nb_uses.min())[0]
        # Pick one of them
        random_int = np.random.randint(potential_dataset_pathes.size)
        dataset_path = self.dataset_pathes[random_int]
        self.dataset_nb_uses[random_int] += 1 # Update nb use counts

        self.name = Path(dataset_path).name
        return self.preprocess(pd.read_pickle(dataset_path))

    def reset(self, seed=None):
        self._set_df(
            self.next_dataset()
        )
        print(f"Selected dataset {self.name} ...")
        return super().reset(seed)
    
