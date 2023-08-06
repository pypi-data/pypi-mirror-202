import pandas as pd

class LinearRegression:
	def __init__(self, df):
		if isinstance(df, pd.DataFrame):
			self.df = df
		else:
			raise ValueError('Argument provided is not a pandas dataframe')

def testing():
	print("ok c'est bon")
