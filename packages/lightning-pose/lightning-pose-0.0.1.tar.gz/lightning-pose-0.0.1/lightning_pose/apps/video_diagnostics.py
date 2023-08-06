"""Analyze predictions on video data.

Refer to apps.md for information on how to use this file.

"""

import argparse
import os
import pandas as pd
from pathlib import Path
import streamlit as st
from collections import defaultdict

from lightning_pose.apps.utils import build_precomputed_metrics_df, get_col_names, concat_dfs
from lightning_pose.apps.utils import update_vid_metric_files_list, get_all_videos
from lightning_pose.apps.plots import get_y_label
from lightning_pose.apps.plots import make_seaborn_catplot, make_plotly_catplot, plot_precomputed_traces

st.session_state["n_submits"] = 0

catplot_options = ["boxen", "box", "bar", "violin", "strip"]
scale_options = ["linear", "log"]


def run():

    args = parser.parse_args()

    st.title("Video Diagnostics")

    st.sidebar.header("Data Settings")

    all_videos_: list = get_all_videos(args.model_folders)

    # choose from the different videos that were predicted
    video_to_plot = st.selectbox(
        "Select a video:", [*all_videos_], key="video")

    prediction_files = update_vid_metric_files_list(video=video_to_plot, model_preds_folder=args.model_folders)

    if len(prediction_files) > 0:  # otherwise don't try to proceed

        # ---------------------------------------------------
        # load data
        # ---------------------------------------------------
        dframes_metrics = defaultdict(dict)
        dframes_traces = {}
        for p, model_pred_files in enumerate(prediction_files):
            # use provided names from cli
            if len(args.model_names) > 0:
                model_name = args.model_names[p]
                model_folder = args.model_folders[p]

            for model_pred_file in model_pred_files:
                model_pred_file_path = os.path.join(model_folder, 'video_preds', model_pred_file)
                if not isinstance(model_pred_file, Path):
                    model_pred_file.seek(0)  # reset buffer after reading
                if 'pca' in str(model_pred_file) or 'temporal' in str(model_pred_file) or 'pixel' in str(model_pred_file):
                    dframe = pd.read_csv(model_pred_file_path, index_col=None)
                    dframes_metrics[model_name][str(model_pred_file)] = dframe
                else:
                    dframe = pd.read_csv(model_pred_file_path, header=[1, 2], index_col=0)
                    dframes_traces[model_name] = dframe
                    dframes_metrics[model_name]['confidence'] = dframe
                data_types = dframe.iloc[:, -1].unique()

        # edit model names if desired, to simplify plotting
        st.sidebar.write("Model display names (editable)")
        new_names = []
        og_names = list(dframes_metrics.keys())
        for name in og_names:
            new_name = st.sidebar.text_input(label="", value=name)
            new_names.append(new_name)

        # change dframes key names to new ones
        for n_name, o_name in zip(new_names, og_names):
            dframes_metrics[n_name] = dframes_metrics.pop(o_name)

        # ---------------------------------------------------
        # compute metrics
        # ---------------------------------------------------

        # concat dataframes, collapsing hierarchy and making df fatter.
        df_concat, keypoint_names = concat_dfs(dframes_traces)
        df_metrics = build_precomputed_metrics_df(
            dframes=dframes_metrics, keypoint_names=keypoint_names)
        metric_options = list(df_metrics.keys())

        # ---------------------------------------------------
        # plot diagnostics
        # ---------------------------------------------------

        # choose which metric to plot
        metric_to_plot = st.selectbox("Select a metric:", metric_options, key="metric")

        x_label = "Model Name"
        y_label = get_y_label(metric_to_plot)

        # plot diagnostic averaged overall all keypoints
        plot_type = st.selectbox("Select a plot type:", catplot_options, key="plot_type")
        plot_scale = st.radio("Select y-axis scale", scale_options, key="plot_scale")
        log_y = False if plot_scale == "linear" else True
        fig_cat = make_seaborn_catplot(
            x="model_name", y="mean", data=df_metrics[metric_to_plot], log_y=log_y, x_label=x_label,
            y_label=y_label, title="Average over all keypoints", plot_type=plot_type)
        st.pyplot(fig_cat)

        # select keypoint to plot
        keypoint_to_plot = st.selectbox(
            "Select a keypoint:", pd.Series([*keypoint_names, "mean"]), key="keypoint_to_plot",
        )
        # show boxplot per keypoint
        fig_box = make_plotly_catplot(
            x="model_name", y=keypoint_to_plot, data=df_metrics[metric_to_plot], x_label=x_label,
            y_label=y_label, title=keypoint_to_plot, plot_type="box")
        st.plotly_chart(fig_box)
        # show histogram per keypoint
        fig_hist = make_plotly_catplot(
            x=keypoint_to_plot, y=None, data=df_metrics[metric_to_plot], x_label=y_label,
            y_label="Frame count", title=keypoint_to_plot, plot_type="hist"
        )
        st.plotly_chart(fig_hist)

        # ---------------------------------------------------
        # plot traces
        # ---------------------------------------------------
        st.header("Trace diagnostics")

        models = st.multiselect(
            "Select models:", pd.Series(list(dframes_metrics.keys())), default=list(dframes_metrics.keys())
        )
        keypoint = st.selectbox("Select a keypoint:", pd.Series(keypoint_names))
        cols = get_col_names(keypoint, "x", models)
        fig_traces = plot_precomputed_traces(df_metrics, df_concat, cols)
        st.plotly_chart(fig_traces)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--model_folders', action='append', default=[])
    parser.add_argument('--model_names', action='append', default=[])

    run()
