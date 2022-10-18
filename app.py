import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cached convert from:
# https://docs.streamlit.io/library/api-reference/widgets/st.download_button
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


sns.set_context("talk")

st.title("Cell/ROI csv plotting App")
st.text(
    "Use this app to load the cell/ROI csv files\nand it will plot the Mean versus Slice traces."
)
st.markdown("------")

with st.sidebar:
    # input_columns = st.columns(2)
    st.subheader("Data upload")
    csv_files = st.file_uploader(
        "Load the csv files:", type=["csv"], accept_multiple_files=True
    )

    st.subheader("Area thresholding")
    area_threshold = st.number_input(
        "Set the minimum Area threshold value: ", 0, 20000, 0, 100
    )

    st.subheader("Resting state range for dF/F calculation")
    bg_range = st.columns(2)
    bg_lower = bg_range[0].number_input(
        "Set the lower bound of Slice in defining the resting state:", 0
    )

    bg_upper = bg_range[1].number_input(
        "Set the upper bound of Slice in defining the resting state:",
        0,
        1000,
        40,
        1,
    )

if len(csv_files):
    # We'll store each loaded csv in this dict.
    df_dict = dict()

    for file in csv_files:
        df = pd.read_csv(file)
        id = int(file.name[:-4])
        df_dict[id] = df
    # st.write(id)
    # st.dataframe(df_dict[id])

    df_all = pd.DataFrame()
    first = True
    for key in sorted(df_dict.keys()):
        x = df_dict[key]["Slice"].values
        y = df_dict[key]["Mean"].values
        f0 = y[bg_lower:bg_upper].mean()
        df = y - f0
        dff = df / f0
        areas = df_dict[key]["Area"].values
        # st.write(areas)
        if not np.any(areas < area_threshold):
            if first:
                df_all["Slice"] = x
                first = False
            df_all[str(key)] = dff

    st.header("Interactive plot:")
    st.line_chart(
        data=df_all,
        x="Slice",
        y=list(df_all.columns[1:]),
    )

    st.header("Static plot:")
    # fig, ax = plt.subplots()
    # sns.lineplot(data=df_all, x="Slice", y=list(df_all.columns[1:]), ax=ax)
    # st.pyplot(fig)
    fig, ax = plt.subplots()
    for col in df_all.columns[1:]:
        x = df_all["Slice"].values
        y = df_all[col].values
        # areas = df_dict[key]["Area"].values
        # st.write(areas)
        # if not np.any(areas < area_threshold):
        ax.plot(x, y, label=col)
    lgd = plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5), frameon=False)
    ax.set_ylabel("$\Delta F / F$")
    ax.set_xlabel("Slice")
    sns.despine()
    st.pyplot(fig)
    out_csv = convert_df(df_all)
    st.markdown("------")
    st.download_button(
        "Download the dF/F traces.",
        data=out_csv,
        file_name="dff_out.csv",
        mime="text/csv",
    )
    # st.markdown("------")
    # if st.button("Plot cell heat map"):
    #     fig2, ax2 = plt.subplots()
    #     cells = list()
    #     cell_ids = list()
    #     for col in df_all.columns[1:]:
    #         x = df_all["Slice"].values
    #         y = df_all[col].values
    #         cells.append(y)
    #         cell_ids.append(int(col))
    #     # lgd = plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))
    #     im = ax2.imshow(
    #         cells,
    #         cmap="viridis",
    #         extent=[np.min(x), np.max(x), np.min(cell_ids), np.max(cell_ids)],
    #     )
    #     plt.colorbar(im, label="$\Delta F / F$")
    #     ax2.set_ylabel("Cell/ROI Number")
    #     ax2.set_xlabel("Slice")
    #     # ax2.set_ylim((np.min(cell_ids), np.max(cell_ids)))
    #     # ax2.set_yticks(ticks=np.arange(len(cell_ids)), labels=cell_ids)
    #     st.pyplot(fig2)
