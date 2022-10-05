import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Cell/ROI csv plotting App")
st.text(
    "Use this app to load the cell/ROI csv files\nand it will plot the Mean versus Slice traces."
)
st.markdown("------")

# input_columns = st.columns(2)
csv_files = st.file_uploader(
    "Load the csv files:", type=["csv"], accept_multiple_files=True
)

area_threshold = st.number_input(
    "Set the minimum Area threshold value: ", 0, 20000, 0, 100
)

st.markdown("------")

# We'll store each loaded csv in this dict.
df_dict = dict()
for file in csv_files:
    df = pd.read_csv(file)
    id = int(file.name[:-4])
    df_dict[id] = df
# st.write(id)
# st.dataframe(df_dict[id])
fig, ax = plt.subplots()
for key in sorted(df_dict.keys()):
    x = df_dict[key]["Slice"].values
    y = df_dict[key]["Mean"].values
    areas = df_dict[key]["Area"].values
    # st.write(areas)
    if not np.any(areas < area_threshold):
        ax.plot(x, y, label=key)
lgd = plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))
ax.set_ylabel("Mean")
ax.set_xlabel("Slice")
st.pyplot(fig)

# fig2, ax2 = plt.subplots()
# for key in sorted(df_dict.keys()):
#     x = df_dict[key]['Slice'].values
#     y = df_dict[key]['Mean'].values
#     areas = df_dict[key]['Area'].values
#     if (areas < area_threshold).any():
#         ax2.plot(x,y, label=key)
# lgd = plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))
# ax2.set_ylabel('Mean')
# ax2.set_xlabel('Slice')
# st.pyplot(fig2)
