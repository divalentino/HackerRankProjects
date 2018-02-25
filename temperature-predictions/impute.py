from pandas import read_csv
from sklearn.preprocessing import Imputer
import numpy
dataset = read_csv('pima-indians-diabetes.csv', header=None)
# mark zero values as missing or NaN
dataset[[1,2,3,4,5]] = dataset[[1,2,3,4,5]].replace(0, numpy.NaN)
# fill missing values with mean column values
values = dataset.values
imputer = Imputer()
transformed_values = imputer.fit_transform(values)

print transformed_values

# count the number of NaN values in each column
print(numpy.isnan(transformed_values).sum())
