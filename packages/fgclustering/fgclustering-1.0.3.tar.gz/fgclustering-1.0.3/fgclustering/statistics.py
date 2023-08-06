############################################
# imports
############################################

import numpy as np
import pandas as pd

from bisect import bisect
from scipy.stats import f_oneway, chisquare
from statsmodels.stats import multitest
from sklearn.utils import resample


############################################
# functions
############################################


def compute_balanced_average_impurity(
    categorical_values, cluster_labels, rescaling_factor=None
):
    """Compute balanced average impurity as score for categorical values in a clustering.
    Impurity score is an Gini Coefficient of the classes within each cluster.
    The class sizes are balanced by rescaling with the inverse size of the class in the overall dataset.

    :param categorical_values: Values of categorical feature / target.
    :type categorical_values: pandas.Series
    :param cluster_labels: Cluster labels for each value.
    :type cluster_labels: numpy.ndarray
    :param rescaling_factor: Dictionary with rescaling factor for each class / unique feature value.
        If parameter is set to None, the rescaling factor will be computed from the input data categorical_values, defaults to None
    :type rescaling_factor: dict
    :return: Impurity score.
    :rtype: float
    """
    # compute the number of datapoints for each class to use it then for rescaling of the
    # class sizes within each cluster --> rescaling with inverse class size
    if rescaling_factor is None:
        rescaling_factor = {
            class_: 1 / sum(categorical_values == class_)
            for class_ in np.unique(categorical_values)
        }
    balanced_impurities = []

    for cluster in np.unique(cluster_labels):
        categorical_values_cluster = categorical_values[cluster_labels == cluster]

        # compute balanced class probabilities (rescaled with overall class size)
        class_probabilities_unnormalized = [
            sum(categorical_values_cluster == class_) * rescaling_factor[class_]
            for class_ in np.unique(categorical_values)
        ]
        class_probabilities_unnormalized = np.array(class_probabilities_unnormalized)
        normalization_factor = class_probabilities_unnormalized.sum()
        class_probabilities = class_probabilities_unnormalized / normalization_factor

        # compute (balanced) gini impurity
        gini_impurity = 1 - np.sum(class_probabilities**2)
        balanced_impurities.append(gini_impurity)

    score = np.mean(balanced_impurities)

    return score


def compute_total_within_cluster_variation(continuous_values, cluster_labels):
    """Compute total within cluster variation as score for continuous values in a clustering.

    :param continuous_values: Values of continuous feature / target.
    :type continuous_values: pandas.Series
    :param cluster_labels: Cluster labels for each value.
    :type cluster_labels: numpy.ndarray
    :return: Within cluster variation score.
    :rtype: float
    """
    score = 0
    for cluster in np.unique(cluster_labels):
        continuous_values_cluster = continuous_values[cluster_labels == cluster]
        score += np.var(continuous_values_cluster) * len(continuous_values_cluster)

    return score


def _anova_test(list_of_df):
    """Perform one way ANOVA test on continuous features.

    :param list_of_df: List of dataframes, where each dataframe contains
        the feature values for one cluster.
    :type list_of_df: list
    :return: P-value of ANOVA test.
    :rtype: float
    """
    anova = f_oneway(*list_of_df)
    return anova.pvalue


def _chisquare_test(df, list_of_df):
    """Perform chi square test on categorical features.

    :param df: Dataframe with feature and cluster.
    :type df: pandas.DataFrame
    :param list_of_df: List of dataframes, where each dataframe contains
        the feature values for one cluster.
    :type list_of_df: list
    :return: P-value of chi square test.
    :rtype: float
    """
    cat_vals = df.feature.unique()
    count_global = np.array([(df.feature == cat_val).sum() for cat_val in cat_vals])
    count_global = count_global / count_global.sum()

    p_values = []
    for df_ in list_of_df:
        counts_clusters = np.array([(df_ == cat_val).sum() for cat_val in cat_vals])
        number_datapoints_in_cluster = counts_clusters.sum()
        p_values.append(
            chisquare(
                counts_clusters, f_exp=count_global * number_datapoints_in_cluster
            ).pvalue
        )

    _, p_values = multitest.fdrcorrection(p_values)
    return min(p_values)


def _rank_features(X, y, p_value_of_features):
    """Rank features by lowest p-value.

    :param X: Feature matrix.
    :type X: pandas.DataFrame
    :param y: Target column.
    :type y: pandas.Series
    :param p_value_of_features: Computed p-values of all features.
    :type p_value_of_features: dict
    :return: Ranked feature matrix.
    :rtype: pandas.DataFrame
    """
    data_clustering_ranked = X.copy()
    data_clustering_ranked["target"] = y
    p_value_of_features["target"] = -1
    p_value_of_features["cluster"] = -1

    # sort features by p-value
    features_sorted = [
        k for k, v in sorted(p_value_of_features.items(), key=lambda item: item[1])
    ]
    data_clustering_ranked = data_clustering_ranked.reindex(features_sorted, axis=1)

    return data_clustering_ranked


def _sort_clusters_by_target(data_clustering_ranked, model_type):
    """Sort clusters by mean target values in clusters.

    :param data_clustering_ranked: Filtered and ranked data frame incl features, target and cluster numbers.
    :type data_clustering_ranked: pandas.DataFrame
    :param model_type: Model type of Random Forest model: classifier or regression.
    :type model_type: str
    :return: Filtered and ranked feature matrix with ordered clusters.
    :rtype: pandas.DataFrame
    """
    # When using a classifier, the target value is label encoded, such that we can sort the clusters by target values
    if model_type == "classifier":
        data_clustering_ranked["target_orig"] = data_clustering_ranked["target"]
        data_clustering_ranked["target"] = (
            data_clustering_ranked["target_orig"].astype("category").cat.codes
        )

    means = (
        data_clustering_ranked.groupby(["cluster"])
        .mean()
        .sort_values(by="target", ascending=True)
    )
    means["target"] = range(means.shape[0])
    mapping = dict(means["target"])
    mapping = dict(sorted(mapping.items(), key=lambda item: item[1]))
    data_clustering_ranked = data_clustering_ranked.replace({"cluster": mapping})
    data_clustering_ranked["cluster"] = pd.Categorical(
        data_clustering_ranked["cluster"],
        sorted(data_clustering_ranked["cluster"].unique()),
    )

    # Decode target values and remove encoded values
    if model_type == "classifier":
        data_clustering_ranked["target"] = data_clustering_ranked["target_orig"]
        data_clustering_ranked.drop(["target_orig"], axis=1, inplace=True)

    return data_clustering_ranked


def calculate_global_feature_importance(X, y, cluster_labels, model_type):
    """Calculate global feature importance for each feature.
    The higher the importance for a feature, the lower the p-value obtained by
    an ANOVA (continuous feature) or chi-square (categorical feature) test.
    Returned as p-value, hence importance is 1-p-value.

    :param X: Feature matrix.
    :type X: pandas.DataFrame
    :param y: Target column.
    :type y: pandas.Series
    :param cluster_labels: Clustering labels.
    :type cluster_labels: numpy.ndarray
    :param model_type: Model type of Random Forest model: classifier or regression.
    :type model_type: str
    :return: Data Frame incl features, target and cluster numbers ranked by p-value of statistical test
        and dictionary with computed p-values of all features.
    :rtype: pandas.DataFrame and dict
    """
    X = X.copy()
    X["cluster"] = cluster_labels
    p_value_of_features = dict()

    # statistical test for each feature
    for feature in X.columns:
        assert pd.api.types.is_categorical_dtype(
            X[feature]
        ) or pd.api.types.is_numeric_dtype(
            X[feature]
        ), f"Feature {feature} has to be of type category of numeric!"

        df = pd.DataFrame({"cluster": X["cluster"], "feature": X[feature]})
        list_of_df = [df.feature[df.cluster == cluster] for cluster in set(df.cluster)]

        if pd.api.types.is_categorical_dtype(X[feature]):
            chisquare_p_value = _chisquare_test(df, list_of_df)
            p_value_of_features[feature] = chisquare_p_value

        else:
            anova_p_value = _anova_test(list_of_df)
            p_value_of_features[feature] = anova_p_value

    data_clustering_ranked = _rank_features(X, y, p_value_of_features)
    data_clustering_ranked = _sort_clusters_by_target(
        data_clustering_ranked, model_type
    )
    data_clustering_ranked.sort_values(by=["cluster", "target"], axis=0, inplace=True)

    return data_clustering_ranked, p_value_of_features


def _calculate_p_value_categorical(
    X_feature_cluster, X_feature, cluster, cluster_size, bootstraps
):
    """Calculate bootstrapped p-value for categorical features to
    determine the importance of the feature for a certain cluster.
    The lower the bootstrapped p-value, the lower the impurity of the
    feature in the respective cluster.

    :param X_feature_cluster: Categorical feature values in cluster.
    :type X_feature_cluster: pandas.Series
    :param X_feature: Categorical feature values.
    :type X_feature: pandas.Series
    :param cluster: Cluster number.
    :type cluster: int
    :param cluster_size: Size of cluster, i.e. number of data points in cluster.
    :type cluster_size: int
    :param bootstraps: Number of bootstraps to be drawn for computation of p-value.
    :type bootstraps: int
    :return: Bootstrapped p-value for categorical feature.
    :rtype: float
    """
    cluster_label = [cluster] * cluster_size
    rescaling_factor = {class_: 1 for class_ in np.unique(X_feature)}
    X_feature_cluster_impurity = compute_balanced_average_impurity(
        X_feature_cluster, cluster_label, rescaling_factor=rescaling_factor
    )

    bootstrapped_impurity = list()
    for b in range(bootstraps):
        bootstrapped_X_feature = resample(
            X_feature, replace=False, n_samples=cluster_size
        )
        bootstrapped_impurity.append(
            compute_balanced_average_impurity(
                bootstrapped_X_feature, cluster_label, rescaling_factor=rescaling_factor
            )
        )

    bootstrapped_impurity = sorted(bootstrapped_impurity)
    p_value = bisect(bootstrapped_impurity, X_feature_cluster_impurity) / bootstraps
    return p_value


def _calculate_p_value_continuous(
    X_feature_cluster, X_feature, cluster_size, bootstraps
):
    """Calculate bootstrapped p-value for continuous features to
    determine the importance of the feature for a certain cluster.
    The lower the bootstrapped p-value, the lower the variance of the
    feature in the respective cluster.

    :param X_feature_cluster: Continuous feature values in cluster.
    :type X_feature_cluster: pandas.Series
    :param X_feature: Continuous feature values.
    :type X_feature: pandas.Series
    :param cluster_size: Size of cluster, i.e. number of data points in cluster.
    :type cluster_size: int
    :param bootstraps: Number of bootstraps to be drawn for computation of p-value.
    :type bootstraps: int
    :return: Bootstrapped p-value for continuous feature.
    :rtype: float
    """
    X_feature_cluster_var = X_feature_cluster.var()

    bootstrapped_var = list()
    for b in range(bootstraps):
        bootstrapped_X_feature = resample(
            X_feature, replace=True, n_samples=cluster_size
        )
        bootstrapped_var.append(bootstrapped_X_feature.var())

    bootstrapped_var = sorted(bootstrapped_var)
    p_value = bisect(bootstrapped_var, X_feature_cluster_var) / bootstraps
    return p_value


def calculate_local_feature_importance(data_clustering_ranked, bootstraps_p_value):
    """Calculate local importance of each feature within each cluster.
    The higher the importance for a feature, the lower the variance (continuous feature)
    or impurity (categorical feature) of that feature within the cluster.
    Returned as p-value, hence importance is 1-p-value.

    :param data_clustering_ranked: Filtered and ranked data frame incl features, target and cluster numbers.
    :type data_clustering_ranked: pandas.DataFrame
    :param bootstraps_p_value: Number of bootstraps to be drawn for computation of p-value.
    :type bootstraps_p_value: int
    :return: p-value matrix of all features per cluster.
    :rtype: pandas.DataFrame
    """
    data_clustering_ranked = data_clustering_ranked.copy()
    clusters = data_clustering_ranked["cluster"]
    clusters_size = clusters.value_counts()
    data_clustering_ranked.drop(["cluster", "target"], axis=1, inplace=True)

    features = data_clustering_ranked.columns.tolist()
    p_value_of_features_per_cluster = pd.DataFrame(
        columns=clusters.unique(), index=features
    )

    for feature in data_clustering_ranked.columns:
        assert pd.api.types.is_categorical_dtype(
            data_clustering_ranked[feature]
        ) or pd.api.types.is_numeric_dtype(
            data_clustering_ranked[feature]
        ), f"Feature {feature} has dytpye {data_clustering_ranked[feature].dtype} but has to be of type category or numeric!"

        if pd.api.types.is_categorical_dtype(data_clustering_ranked[feature]):
            for cluster in clusters.unique():
                X_feature_cluster = data_clustering_ranked.loc[
                    clusters == cluster, feature
                ]
                X_feature = data_clustering_ranked[feature]
                p_value_of_features_per_cluster.loc[
                    feature, cluster
                ] = _calculate_p_value_categorical(
                    X_feature_cluster,
                    X_feature,
                    cluster,
                    clusters_size.loc[cluster],
                    bootstraps_p_value,
                )

        else:
            for cluster in clusters.unique():
                X_feature_cluster = data_clustering_ranked.loc[
                    clusters == cluster, feature
                ]
                X_feature = data_clustering_ranked[feature]
                p_value_of_features_per_cluster.loc[
                    feature, cluster
                ] = _calculate_p_value_continuous(
                    X_feature_cluster,
                    X_feature,
                    clusters_size.loc[cluster],
                    bootstraps_p_value,
                )

    return p_value_of_features_per_cluster
