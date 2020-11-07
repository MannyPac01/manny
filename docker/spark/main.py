#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

import numpy as np
import seaborn as sns

spark = SparkSession.builder.appName("PysparkExample").config("spark.some.config.option", "some-value").getOrCreate()


df = spark.read.csv('Vermont_Vendor_Payments.csv', header='true', inferSchema = True)
df = df.withColumn("Amount", df["Amount"].cast("double"))

df

# Show first 5 rows
df.show(5)

# Show first row
df.head()

# Describe table detail
df.describe().show()

# creating temp table query with SQL
df.createOrReplaceTempView('VermontVendor')
spark.sql('''
SELECT `Quarter Ending`, Department, Amount, State FROM VermontVendor 
LIMIT 10
''').show()


# using spark lib to query data
df.select('Quarter Ending', 'Department','Amount', 'State').show(10)

# Filter data using SQL
spark.sql('''
SELECT `Quarter Ending`, Department, Amount, State FROM
VermontVendor
WHERE Department = 'Education'
LIMIT 10
''').show()

# Filter data using Pythonic Python
df.select('Quarter Ending', 'Department', 'Amount', 'State').filter("Department = 'Education'").show(10)

plot_df = spark.sql(
'''
SELECT Department, SUM(Amount) as Total FROM VermontVendor 
GROUP BY Department
ORDER BY Total DESC
LIMIT 10
'''
).toPandas()

fig,ax = plt.subplots(1,1,figsize=(10,6))
plot_df.plot(x = 'Department', y = 'Total', kind = 'barh', color = 'C0', ax = ax, legend = False)
ax.set_xlabel('Department', size = 16)
ax.set_ylabel('Total', size = 16)
plt.savefig('barplot.png')
plt.show()



plot_df2 = spark.sql(
'''
SELECT Department, SUM(Amount) as Total FROM VermontVendor 
GROUP BY Department
'''
).toPandas()
plt.figure(figsize = (10,6))
sns.distplot(np.log(plot_df2['Total']))
plt.title('Histogram of Log Totals for all Departments in Dataset', size = 16)
plt.ylabel('Density', size = 16)
plt.xlabel('Log Total', size = 16)
plt.savefig('distplot.png')
plt.show()




