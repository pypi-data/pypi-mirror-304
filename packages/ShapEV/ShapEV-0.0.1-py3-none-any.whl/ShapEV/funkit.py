import numpy as np
from itertools import combinations
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Define the function used

def joint_shap(interaction_values, first_feature_index, second_feature_index):
    """
    Calculate the joint SHAP values for two features.

    Parameters:
    interaction_values (np.ndarray): 3D tensor of SHAP interaction values.
    first_feature_index (int): Index of the first feature.
    second_feature_index (int): Index of the second feature.

    Returns:
    np.ndarray: Calculated joint SHAP values.
    """
    fir_main_fea = interaction_values[:, first_feature_index, first_feature_index]
    sec_main_fea = interaction_values[:, second_feature_index, second_feature_index]
    interaction = interaction_values[:, first_feature_index, second_feature_index]
    return fir_main_fea + sec_main_fea + 2 * interaction

def generate_combinations(input_list):
    """
    Generate all unique combinations of two features.

    Parameters:
    input_list (list): List of feature names.

    Returns:
    list: All unique combinations of two features.
    """
    return list(combinations(input_list, 2)) 

def base_search(shap_interaction_values, list_comb, fea_list, X, SPACE=5):
    """
    Find the best feature combinations based on joint SHAP values.

    Parameters:
    shap_interaction_values (np.ndarray): 3D tensor of SHAP interaction values.
    list_comb (list): List of feature combinations.
    fea_list (pd.Index): Original features name list.
    X (pd.DataFrame): Original features matrix.
    SPACE (int): Maximum number of combinations to return.

    Returns:
    list: Set of best feature combinations.
    """
    best_combinations = []  # Store best combinations
    best_r2_values = []     # Store corresponding R² values

    SPACE = min(SPACE, len(list_comb))  # Adjust SPACE to be within bounds

    for k in range(len(list_comb)):
        first_feature_index = fea_list.get_loc(list_comb[k][0])
        second_feature_index = fea_list.get_loc(list_comb[k][1])
        
        # Calculate joint SHAP values
        joint_shap_values = joint_shap(shap_interaction_values, first_feature_index, second_feature_index)
        
        # Get feature values
        first_x = X.iloc[:, first_feature_index].to_numpy().reshape(-1, 1)
        second_x = X.iloc[:, second_feature_index].to_numpy().reshape(-1, 1)
        
        # Combine features into a matrix
        X_combined = np.hstack((first_x, second_x))
        
        # Fit linear regression
        model = LinearRegression()
        model.fit(X_combined, joint_shap_values)
        
        # Predict and calculate R²
        predictions = model.predict(X_combined)
        current_r2 = r2_score(joint_shap_values, predictions)

        # Update best combinations list
        if len(best_r2_values) < 3 or current_r2 > min(best_r2_values):
            if current_r2 in best_r2_values:
                index = best_r2_values.index(current_r2)
                best_combinations[index] = list_comb[k]
                best_r2_values[index] = current_r2
            else:
                if len(best_r2_values) < 3:
                    best_combinations.append(list_comb[k])
                    best_r2_values.append(current_r2)
                else:
                    min_index = best_r2_values.index(min(best_r2_values))
                    if current_r2 > best_r2_values[min_index]:
                        best_combinations[min_index] = list_comb[k]
                        best_r2_values[min_index] = current_r2

    # Create a combined results list and sort by R² values
    combined_results = list(zip(best_combinations, best_r2_values))
    combined_results.sort(key=lambda x: x[1], reverse=True)  # Sort by R² value

    # Merge top combinations and remove duplicates
    merged_combination = set()
    for combo, _ in combined_results[:SPACE]:
        merged_combination.update(combo)

    return list(merged_combination)  # Return unique combinations list

def cal_equal_coef(interaction_values, best_combination, fea_list, X):
    """
    Calculate the contribution of main and interaction features.

    Parameters:
    interaction_values (np.ndarray): 3D tensor of SHAP interaction values.
    best_combination (list): Best feature combinations.
    fea_list (pd.Index): Original features name list.
    X (pd.DataFrame): Original features matrix.

    Returns:
    tuple: R² value, linear formula, updated SHAP values, and equivalent values.
    """
    # Calculate main feature contributions
    _main = np.zeros(interaction_values.shape[0])
    for feature in best_combination:
        _fea_index = fea_list.get_loc(feature)
        _main += interaction_values[:, _fea_index, _fea_index]

    # Calculate interaction contributions
    _interaction = np.zeros(interaction_values.shape[0])
    each_pair = generate_combinations(best_combination)
    for pair in each_pair:
        first_feature_index = fea_list.get_loc(pair[0])
        second_feature_index = fea_list.get_loc(pair[1])
        _interaction += 2 * interaction_values[:, first_feature_index, second_feature_index]
    
    # Combine SHAP values
    joint_shap_values = _interaction + _main

    # Prepare combined feature matrix
    X_combined = np.zeros((X.shape[0], len(best_combination)))  # Initialize
    for k, feature in enumerate(best_combination):
        _fea_index = fea_list.get_loc(feature)
        X_combined[:, k] = X.iloc[:, _fea_index].to_numpy()  # Store feature values

    # Fit linear regression
    model = LinearRegression()
    model.fit(X_combined, joint_shap_values)

    # Predict and calculate R²
    predictions = model.predict(X_combined)
    current_r2 = r2_score(joint_shap_values, predictions)

    # Construct linear formula
    coefficients = model.coef_
    intercept = model.intercept_
    
    formula_terms = [f"{coef:.4f} * {feature}" for coef, feature in zip(coefficients, best_combination)]
    formula = f"y = {intercept:.4f} + " + " + ".join(formula_terms) # Correct formula construction
    
    print("Equivalent value:", formula)
    print(f'R² is {current_r2:.4f}')

    # Prepare the output strings
    output_text = f"Equivalent value: {formula}\n"
    output_text += f"R² is {current_r2:.4f}\n"

    # Write to a local text file
    with open("./ShapEV/equations.txt", "w", encoding="utf-8") as file:
        file.write(output_text)

    return current_r2, formula, cal_update_shap(predictions, best_combination, X), predictions  # Return R² value and linear formula

def cal_update_shap(Eq_value, best_combination, X):
    """
    Convert original features into the representation of equivalent values.

    Parameters:
    Eq_value (np.ndarray): Equivalent values from the model.
    best_combination (list): Best feature combinations.
    X (pd.DataFrame): Original features matrix.

    Returns:
    pd.DataFrame: Updated DataFrame with equivalent values.
    """
    X_updated = X.drop(columns=best_combination, errors='ignore')
    X_updated.insert(0, 'equ_v', Eq_value)  # Insert new column for equivalent values
    return X_updated

def plot_scatter(Joint_shap, equival_value):
    y_true = equival_value
    y_pred = Joint_shap

    # Calculate R-squared and MAE values
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)

    # Create DataFrame for plotting
    data = pd.DataFrame({
        'True': y_true,
        'Predicted': y_pred,
        'Data Set': 'All'
    })

    # Custom color palette
    palette = {'All': '#4c72b0'}  # Nature-like blue tone

    # Set font properties to Arial and adjust font sizes
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 24

    # Create a JointGrid object
    plt.figure(figsize=(6, 6), dpi=500)
    g = sns.JointGrid(data=data, x="True", y="Predicted", height=8)

    # Plot the scatter plot
    g.plot_joint(sns.scatterplot, alpha=0.6, s=60, color=palette['All'])

    # Add regression line
    sns.regplot(data=data, x="True", y="Predicted", scatter=False, ax=g.ax_joint,
                color='#4c72b0', line_kws={"lw": 2}, label='Regression Line')

    # Plot the marginal histograms
    g.plot_marginals(sns.histplot, kde=False, element='bars', color='#b4c7e7', alpha=0.6)

    # Add text for R^2 and MAE
    ax = g.ax_joint
    ax.text(0.9, 0.1, f'MAE = {mae:.2f}', transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
    ax.text(0.9, 0.05, f'$R^2$ = {r2:.3f}', transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

    # Add y=x line for comparison
    ax.plot([data['True'].min(), data['True'].max()], 
            [data['True'].min(), data['True'].max()], c="black", alpha=0.7, linestyle='--', label='x=y')

    # Set x and y axis labels with custom font sizes
    g.ax_joint.set_xlabel('Equivalent Values', fontsize=25)
    g.ax_joint.set_ylabel('Joint SHAP values', fontsize=25)

    # Add legend
    ax.legend(fontsize=22,loc=2)

    # Save the figure
    plt.savefig('./ShapEV/scatter.png', dpi=500)
    plt.savefig('./ShapEV/scatter.svg', dpi=500)
    plt.show()