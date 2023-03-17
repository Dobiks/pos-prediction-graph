import pandas as pd

path = 'static_graph.csv'

df = pd.read_csv(path)
df[['x', 'y', 'z']] = df['coords_x_y_z'].str.split('/', expand=True)
df.drop(columns=['coords_x_y_z'], inplace=True)
# Print the updated DataFrame
#change number,x, y,z to int
df['x'] = df['x'].astype(float)
df['y'] = df['y'].astype(float)
df['z'] = df['z'].astype(float)

print(df)
#len of df
print(len(df))
#save to csv

#add parent column
df['parent'] = 0
df.to_csv('corrected_static.csv', index=False)