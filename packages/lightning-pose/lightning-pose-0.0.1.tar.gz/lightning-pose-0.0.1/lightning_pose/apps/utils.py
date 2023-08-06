"""Utility functions for streamlit apps."""

import numpy as np
import pandas as pd
from pathlib import Path
import streamlit as st
import os
from typing import List, Dict, Tuple
from collections import defaultdict

pix_error_key = "pixel error"
conf_error_key = "confidence"
temp_norm_error_key = "temporal norm"
pcamv_error_key = "pca multiview"
pcasv_error_key = "pca singleview"


@st.cache(allow_output_mutation=True)
def update_labeled_file_list(model_preds_folder: list):
    # use_cli_preds = False
    per_model_preds = []
    for i in range(len(model_preds_folder)):
        # pull labeled results from each model folder; wrap in Path so that it looks like an UploadedFile object
        model_preds = [f for f in os.listdir(model_preds_folder[i]) if os.path.isfile(os.path.join(model_preds_folder[i], f))]
        ret_files = []
        for file in model_preds:
            if 'predictions' in file and 'new' not in file:
                ret_files.append(Path(file))
        per_model_preds.append(ret_files)
    return per_model_preds


@st.cache(allow_output_mutation=True)
def update_vid_metric_files_list(video: str, model_preds_folder: list):
    per_vid_preds = []
    for i in range(len(model_preds_folder)):
        # pull each prediction file associated with a particular video; wrap in Path so that it looks like an UploadedFile object
        model_preds = [f for f in os.listdir(os.path.join(model_preds_folder[i], 'video_preds')) \
        if os.path.isfile(os.path.join(model_preds_folder[i], 'video_preds', f))]
        ret_files = []
        for file in model_preds:
            if video in file:
                ret_files.append(Path(file))
        per_vid_preds.append(ret_files)
    return per_vid_preds


@st.cache(allow_output_mutation=True)
def get_all_videos(model_preds_folder: list):
    # find each video that is predicted on by the models; wrap in Path so that it looks like an UploadedFile object
    # returned by streamlit's file_uploader
    ret_videos = set()
    for i in range(len(model_preds_folder)):
        model_preds = [f for f in os.listdir(os.path.join(model_preds_folder[i], 'video_preds')) \
        if os.path.isfile(os.path.join(model_preds_folder[i], 'video_preds', f))]
        for file in model_preds:
            if 'temporal' in file:
                vid_file = file.split('_temporal_norm.csv')[0]
                ret_videos.add(vid_file)
            elif 'temporal' not in file and 'pca' not in file:
                vid_file = file.split('.csv')[0]
                ret_videos.add(vid_file)
    
    return list(ret_videos)


@st.cache
def concat_dfs(dframes: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, List[str]]:
    counter = 0
    for model_name, dframe in dframes.items():
        if counter == 0:
            df_concat = dframe.copy()
            # base_colnames = list(df_concat.columns.levels[0])  # <-- sorts names, bad!
            base_colnames = list([c[0] for c in df_concat.columns[1::3]])
            df_concat = strip_cols_append_name(df_concat, model_name)
        else:
            df = strip_cols_append_name(dframe.copy(), model_name)
            df_concat = pd.concat([df_concat, df], axis=1)
        counter += 1
    return df_concat, base_colnames

@st.cache
def get_df_box(df_orig, keypoint_names, model_names):
    df_boxes = []
    for keypoint in keypoint_names:
        for model_curr in model_names:
            tmp_dict = {
                "keypoint": keypoint,
                "metric": "Pixel error",
                "value": df_orig[df_orig.model_name == model_curr][keypoint],
                "model_name": model_curr,
            }
            df_boxes.append(pd.DataFrame(tmp_dict))
    return pd.concat(df_boxes)


@st.cache
def get_df_scatter(df_0, df_1, data_type, model_names, keypoint_names):
    df_scatters = []
    for keypoint in keypoint_names:
        df_scatters.append(pd.DataFrame({
            "img_file": df_0.img_file[df_0.set == data_type],
            "keypoint": keypoint,
            model_names[0]: df_0[keypoint][df_0.set == data_type],
            model_names[1]: df_1[keypoint][df_1.set == data_type],
        }))
    return pd.concat(df_scatters)


def get_col_names(keypoint: str, coordinate: str, models: List[str]) -> List[str]:
    return [get_full_name(keypoint, coordinate, model) for model in models]


def strip_cols_append_name(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df.columns = ["_".join(col).strip() for col in df.columns.values]
    df.columns = [col + "_" + name for col in df.columns.values]
    return df


def get_full_name(keypoint: str, coordinate: str, model: str) -> str:
    return "_".join([keypoint, coordinate, model])


# ----------------------------------------------
# compute metrics
# ----------------------------------------------
@st.cache
def build_precomputed_metrics_df(
    dframes: Dict[str, pd.DataFrame], keypoint_names: List[str], **kwargs
) -> dict:
    concat_dfs = defaultdict(list)
    for model_name, df_dict in dframes.items():
        for metric_name, df in df_dict.items():
            if 'confidence' in metric_name:
                df_ = compute_confidence(df=df, keypoint_names=keypoint_names, model_name=model_name, **kwargs)
                concat_dfs[conf_error_key].append(df_)

            df_ = get_precomputed_error(df, keypoint_names, model_name, **kwargs)
            if 'single' in metric_name:
                concat_dfs[pcasv_error_key].append(df_)
            elif 'multi' in metric_name:
                concat_dfs[pcamv_error_key].append(df_)
            elif 'temporal' in metric_name:
                concat_dfs[temp_norm_error_key].append(df_)
            elif 'pixel' in metric_name:
                concat_dfs[pix_error_key].append(df_)

    for key in concat_dfs.keys():
        concat_dfs[key] = pd.concat(concat_dfs[key])

    return concat_dfs

@st.cache
def get_precomputed_error(
    df: pd.DataFrame, keypoint_names: List[str], model_name: str
) -> pd.DataFrame:
    # collect results
    df_ = df
    df_["model_name"] = model_name
    df_["mean"] = df_[keypoint_names[:-1]].mean(axis=1)
    df_.rename(columns={df.columns[0]:'img_file'}, inplace=True)

    return df_


@st.cache
def compute_confidence(
        df: pd.DataFrame, keypoint_names: List[str], model_name: str, **kwargs
) -> pd.DataFrame:

    if df.shape[1] % 3 == 1:
        # get rid of "set" column if present
        tmp = df.iloc[:, :-1].to_numpy().reshape(df.shape[0], -1, 3)
        set = df.iloc[:, -1].to_numpy()
    else:
        tmp = df.to_numpy().reshape(df.shape[0], -1, 3)
        set = None

    results = tmp[:, :, 2]

    # collect results
    df_ = pd.DataFrame(columns=keypoint_names)
    for c, col in enumerate(keypoint_names):  # loop over keypoints
        df_[col] = results[:, c]
    df_["model_name"] = model_name
    df_["mean"] = df_[keypoint_names[:-1]].mean(axis=1)
    if set is not None:
        df_["set"] = set
        df_["img_file"] = df.index

    return df_


@st.cache
def compute_temporal_norms(
    df: pd.DataFrame, keypoint_names: List[str], model_name: str, **kwargs
) -> pd.DataFrame:
    # compute the norm just for one dataframe
    df_norms = pd.DataFrame(columns=keypoint_names)
    diffs = df.diff(periods=1)  # not using .abs
    for col in keypoint_names:  # loop over keypoints
        df_norms[col] = diffs[col][["x", "y"]].apply(
            np.linalg.norm, axis=1
        )  # norm of the difference for that keypoint
    df_norms["model_name"] = model_name
    df_norms["mean"] = df_norms[keypoint_names[:-1]].mean(axis=1)
    return df_norms