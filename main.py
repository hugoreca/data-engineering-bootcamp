import pandas as pd
import time
import openpyxl

# Location Where the big file is located
file = "C:\\Users\\HUGOREYESCASANOVA\\Box\\Kaizen\\DE\\all_data.csv"

# Read the file in chunks and merge them
reader = pd.read_csv(file, chunksize=10000000, low_memory=False)
frames = []
for chunk in reader:
    frames.append(chunk)
all_data = pd.concat(frames)

# Copy the product column to create pivot easily
all_data['sum_product'] = all_data.product

# Output Location
output = 'C:\\Users\\HUGOREYESCASANOVA\\Documents'

# Variables to answer the questions
store_num = all_data.cadenaComercial.value_counts()[:10]
products = all_data.producto.value_counts()[:10]
categories = all_data.categoria.value_counts()[:10]
catalogues = all_data.catalogo.value_counts()[:10]
top_states = all_data.estado.value_counts()[:10]
bottom_states = all_data.estado.value_counts()[-10:].index.tolist()
type_of_store_num = type(store_num)
distinct = all_data.cadenaComercial.nunique()
list_of_states = all_data['estado'].unique()

########### ANSWER # 1 ###########
print(f"The number of rows is {all_data.shape[0]}\n")
print(f"Answer 1: The number of stores is monitorized by Profeco is: {distinct}\n")

########### ANSWER # 2 ###########
print(f"Answer 2: What are the top 10 monitored products by State?:\n")
states_frame = []
for state in list_of_states:
    sliced_pivot = all_data[(all_data.estado == state)]
    grouped = sliced_pivot.groupby(['estado', 'producto'])['sum_product'].count().nlargest(10)
    states_frame.append(grouped)
top_products_by_state = pd.concat(states_frame)
top_products_by_state.to_excel(f"{output}\\output.xlsx", index=True, header=True)
print(top_products_by_state)

########### ANSWER # 3 ###########
print(f"\nAnswer 3: The store with the highest number of monitored products: {store_num.index[0]}\n")

########### ANSWER # 4 ###########
print(f"\nAnswer 4: Use the data to find an interesting fact:\n")

# Additional Data used for checking interesting facts
print(f"Top ten states are:")
for state in top_states.index.tolist():
    print(f"{top_states.index.tolist().index(state)+1}. {state}")

print(f"\nBottom ten states are:")
for state in reversed(bottom_states):
    print(f"{bottom_states.index(state)+1}. {state}")

print(f"\nTop ten products are:")
for product in products.index.tolist():
    print(f"{products.index.tolist().index(product)+1}. {product}")

print(f"\nTop ten categories are:")
for category in categories.index.tolist():
    print(f"{categories.index.tolist().index(category)+1}. {category}")

print(f"\nTop ten catalogues are:")
for catalogue in catalogues.index.tolist():
    print(f"{catalogues.index.tolist().index(catalogue)+1}. {catalogue}")
