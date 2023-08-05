# Import libraries for Python Advanced
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.outliers_influence as oi
from statsmodels.stats.outliers_influence import OLSInfluence

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef


# Linear Regression Variable Selection
def forward_selection(y, X):
    if 'const' in X.columns:
        X = X.drop(labels = ['const'], axis = 1)
    Xvars = set(X.columns)
    dat = pd.concat(objs = [X, y], axis = 1)
    
    formula = f'{y.name} ~ 1'
    curr_aic = smf.ols(formula = formula, data = dat).fit().aic
    
    selected = []
    while Xvars:
        Xvar_aic = []
        for Xvar in Xvars:
            formula = f'{y.name} ~ {" + ".join(selected + [Xvar])} + 1'
            aic = smf.ols(formula = formula, data = dat).fit().aic
            aic = np.round(a = aic, decimals = 4)
            Xvar_aic.append((aic, Xvar))
        
        Xvar_aic.sort(reverse = True)
        new_aic, best_Xvar = Xvar_aic.pop()
        
        if curr_aic > new_aic:
            Xvars.remove(best_Xvar)
            selected.append(best_Xvar)
            curr_aic = new_aic
        else:
            break
    
    formula = f'{y.name} ~ {" + ".join(selected)} + 1'
    model = smf.ols(formula = formula, data = dat).fit()
    return model

def backward_selection(y, X):
    if 'const' in X.columns:
        X = X.drop(labels = ['const'], axis = 1)
    Xvars = set(X.columns)
    dat = pd.concat(objs = [X, y], axis = 1)
    
    formula = f'{y.name} ~ {" + ".join(list(Xvars))}'
    curr_aic = smf.ols(formula = formula, data = dat).fit().aic
    
    selected = []
    while Xvars:
        Xvar_aic = []
        for Xvar in Xvars:
            sub = dat.drop(labels = selected + [Xvar], axis = 1).copy()
            sub_Xvars = set(sub.columns) - set([y.name])
            formula = f'{y.name} ~ {" + ".join(list(sub_Xvars))} + 1'
            aic = smf.ols(formula = formula, data = sub).fit().aic
            aic = np.round(a = aic, decimals = 4)
            Xvar_aic.append((aic, Xvar))
        
        Xvar_aic.sort(reverse = True)
        new_aic, best_Xvar = Xvar_aic.pop()
        
        if curr_aic > new_aic:
            Xvars.remove(best_Xvar)
            selected.append(best_Xvar)
            curr_aic = new_aic
        else:
            break
    
    dat = dat.drop(labels = selected, axis = 1)
    dat_Xvars = set(dat.columns) - set([y.name])
    
    formula = f'{y.name} ~ {" + ".join(list(dat_Xvars))} + 1'
    model = smf.ols(formula = formula, data = dat).fit()
    return model

def stepwise_selection(y, X):
    if 'const' in X.columns:
        X = X.drop(labels = ['const'], axis = 1)
    Xvars = set(X.columns)
    dat = pd.concat(objs = [X, y], axis = 1)
    
    formula = f'{y.name} ~ 1'
    curr_aic = smf.ols(formula = formula, data = dat).fit().aic
    
    selected = []
    while Xvars:
        Xvar_aic = []
        for Xvar in Xvars:
            formula = f'{y.name} ~ {" + ".join(selected + [Xvar])} + 1'
            aic = smf.ols(formula = formula, data = dat).fit().aic
            aic = np.round(a = aic, decimals = 4)
            Xvar_aic.append((aic, 'add', Xvar))
        
        if selected:
            for Xvar in selected:
                sub = dat[selected + [y.name]].copy()
                sub = sub.drop(labels = [Xvar], axis = 1)
                sub_Xvars = set(sub.columns) - set([y.name])
                formula = f'{y.name} ~ {" + ".join(list(sub_Xvars))} + 1'
                aic = smf.ols(formula = formula, data = sub).fit().aic
                aic = np.round(a = aic, decimals = 4)
                Xvar_aic.append((aic, 'sub', Xvar))
        
        Xvar_aic.sort(reverse = True)
        new_aic, how, best_Xvar = Xvar_aic.pop()
        
        if curr_aic > new_aic and how == 'add':
            Xvars.remove(best_Xvar)
            selected.append(best_Xvar)
            curr_aic = new_aic
        elif curr_aic > new_aic and how == 'sub':
            Xvars.append(best_Xvar)
            selected.remove(best_Xvar)
            curr_aic = new_aic
        elif curr_aic <= new_aic:
            break
    
    formula = f'{y.name} ~ {" + ".join(selected)} + 1'
    model = smf.ols(formula = formula, data = dat).fit()
    return model

def stepwise(y, X, direction = 'both'):
    if direction == 'forward':
        model = forward_selection(y, X)
    elif direction == 'backward':
        model = backward_selection(y, X)
    elif direction == 'both':
        model = stepwise_selection(y, X)
    else:
        model = None
    return model


# Linear Regression Diagnosis
def regressionDiagnosis(model):
    plt.figure(figsize = (10, 10), dpi = 100)
    
    # Linearity
    # lowess: locally weighted linear regression
    ax1 = plt.subplot(2, 2, 1)
    sns.regplot(
        x = model.fittedvalues, 
        y = model.resid, 
        lowess = True, 
        scatter_kws = dict(color = '0.8', ec = '0.3', s = 15),
        line_kws = dict(color = 'red', lw = 1), 
        ax = ax1
    )
    plt.axhline(
        y = 0, 
        color = '0.5', 
        lw = 1, 
        ls = '--'
    )
    plt.title(
        label = 'Residuals vs Fitted', 
        fontdict = dict(size = 16)
    )
    plt.xlabel(
        xlabel = 'Fitted values', 
        fontdict = dict(size = 15)
    )
    plt.ylabel(
        ylabel = 'Residuals', 
        fontdict = dict(size = 15)
    )
    
    # Normality
    ax2 = plt.subplot(2, 2, 2)
    
    # Standardized residuals
    stdres = stats.zscore(a = model.resid)
    
    # Theoretical Quantiles
    (x, y), _ = stats.probplot(x = stdres)
    
    # Q-Q plot
    sns.scatterplot(
        x = x, 
        y = y, 
        color = '0.8', 
        ec = '0.3', 
        size = 2, 
        legend = False, 
        ax = ax2
    )
    plt.plot(
        [-4, 4], 
        [-4, 4], 
        color = '0.5', 
        lw = 1, 
        ls = '--'
    )
    plt.title(
        label = 'Normal Q-Q', 
        fontdict = dict(size = 16)
    )
    plt.xlabel(
        xlabel = 'Theoretical Quantiles', 
        fontdict = dict(size = 15)
    )
    plt.ylabel(
        ylabel = 'Standardized residuals', 
        fontdict = dict(size = 15)
    )
    
    # Homoscedasticity
    ax3 = plt.subplot(2, 2, 3)
    sns.regplot(
        x = model.fittedvalues, 
        y = np.sqrt(stdres.abs()), 
        lowess = True,
        scatter_kws = dict(color = '0.8', ec = '0.3', s = 15),
        line_kws = dict(color = 'red', lw = 1), 
        ax = ax3
    )
    plt.title(
        label = 'Scale-Location', 
        fontdict = dict(size = 16)
    )
    plt.xlabel(
        xlabel = 'Fitted values', 
        fontdict = dict(size = 15)
    )
    plt.ylabel(
        ylabel = 'Sqrt of Standardized residuals', 
        fontdict = dict(size = 15)
    )

    # Outliers using Cook's distance
    ax4 = plt.subplot(2, 2, 4)
    sm.graphics.influence_plot(
        results = model, 
        criterion = 'cooks', 
        size = 24, 
        plot_alpha = 0.2, 
        ax = ax4
    )
    
    plt.tight_layout()
    plt.show()


# Influence Points
def influencePoints(model):
    cd, _ = OLSInfluence(results = model).cooks_distance
    cd = cd.sort_values(ascending = False)
    return cd

# Hat Matrix
def hat_matrix(X):
    X = np.array(object = X)
    XtX = np.matmul(X.transpose(), X)
    XtX_inv = np.linalg.inv(XtX)
    result = np.matmul(
        np.matmul(X, XtX_inv), 
        X.transpose()
    )
    return result

# Leverage: Hat Value
def leverage(X):
    n = X.shape[0]
    hatMat = hat_matrix(X = X)
    X['Leverage'] = np.array([hatMat[i][i] for i in range(n)])
    X = X.iloc[:, -1].sort_values(ascending = False)
    return X

# Standardized residuals
def std_Resid(model):
    stdres = stats.zscore(a = model.resid)
    locs = stdres.abs().sort_values(ascending = False)
    return stdres[locs.index]


# Effect Points for Linear Regression
def augment(model):
    infl = model.get_influence()
    df1 = pd.DataFrame(
        data = {model.model.endog_names: infl.endog},
        index = model.fittedvalues.index
    )
    df2 = pd.DataFrame(
        data = {
            'fitted': model.fittedvalues,
            'resid': model.resid,
            'hat': infl.hat_matrix_diag,
            'sigma': np.sqrt(infl.sigma2_not_obsi),
            'cooksd': infl.cooks_distance[0],
            'std_resid': infl.resid_studentized
        }
    )
    result = pd.concat(objs = [df1, df2], axis = 1)
    return result

# Residual Homoscedasticity Test: Breusch-Pagan Lagrange Multiplier Test
def breushpagan(model):
    test = sm.stats.het_breuschpagan(
        resid = model.resid, 
        exog_het = model.model.exog
    )
    result = pd.DataFrame(
        data = test, 
        index = ['Statistic', 'P-Value', 'F-Value', 'F P-Value']
    ).T
    return result


# Metrics for Regression: MSE, RMSE, MSE, MAPE
def regmetrics(y_true, y_pred):
    MSE = mean_squared_error(
        y_true = y_true, 
        y_pred = y_pred
    )
    
    RMSE = MSE**(1/2)
    
    minus_count = y_pred.lt(0).sum()
    if minus_count > 0:
        MSLE = None
        RMSLE = None
    else:
        MSLE = mean_squared_log_error(
            y_true = y_true, 
            y_pred = y_pred
        )
        RMSLE = MSLE ** (1/2)
    
    MAE = mean_absolute_error(
        y_true = y_true, 
        y_pred = y_pred
    )
    
    MAPE = mean_absolute_percentage_error(
        y_true = y_true, 
        y_pred = y_pred
    )
    
    result = pd.DataFrame(
        data = [MSE, RMSE, RMSLE, MAE, MAPE], 
        index = ['MSE', 'RMSE', 'RMSLE', 'MAE', 'MAPE']
    ).T
    
    # result = result.round(3)
    return result


# Metrics for Classification: ROC, AUC
def plot_roc(
    y_true, 
    y_prob, 
    pos = None, 
    color = None
):
    y_class = y_true.value_counts().sort_index()
    
    if pos == None:
        pos = y_class.loc[y_class == y_class.min()].index[0]
    
    idx = np.where(y_class.index == pos)[0][0]
    
    if y_prob.ndim == 2:
        y_prob = y_prob[:, idx]
        
    fpr, tpr, _ = roc_curve(
        y_true = y_true, 
        y_score = y_prob, 
        pos_label = pos
    )
    
    auc_ = auc(x = fpr, y = tpr)
    
    plt.plot(
        fpr, 
        tpr, 
        color = color, 
        label = f'AUC = {auc_:.4f}', 
        lw = 1.0
    )
    
    plt.plot(
        [0, 1], 
        [0, 1], 
        color = 'k', 
        linestyle = '--'
    )
    
    plt.title(label = 'ROC Curve')
    plt.xlabel(xlabel = 'FPR')
    plt.ylabel(ylabel = 'TPR')
    plt.legend(loc = 'lower right');


# Metrics for Classification: PR, AP
def plot_pr(
    y_true, 
    y_prob, 
    pos = None, 
    name = None, 
    color = None
):
    y_class = y_true.value_counts().sort_index()
    
    if pos == None:
        pos = y_class.loc[y_class == y_class.min()].index[0]
    
    idx = np.where(y_class.index == pos)[0][0]
    
    if y_prob.ndim == 2:
        y_prob = y_prob[:, idx]
    
    pr = PrecisionRecallDisplay.from_predictions(
        y_true = trReal, 
        y_pred = trProb, 
        pos_label = pos, 
        name = name, 
        color = color
    )
    
    plt.title(label = 'PR Curve')
    plt.xlabel(xlabel = 'Recall')
    plt.ylabel(ylabel = 'Precision')
    plt.legend(loc = 'best');


# Variance Inflation factor
def vif(X):
    X2 = X.copy()
    if 'const' not in X2.columns:
        X2.insert(loc = 0, column = 'const', value = 1)
    
    func = oi.variance_inflation_factor
    ncol = X2.shape[1]
    vifs = [func(exog = X2.values, exog_idx = i) for i in range(1, ncol)]
    result = pd.DataFrame(data = vifs, index = X2.columns[1:]).T
    return result

# Coefficients for Regression
def coefs(model):
    if model.coef_.ndim == 1:
        coefs = pd.Series(
            data = model.coef_, 
            index = model.feature_names_in_
        )
    elif model.coef_.ndim == 2:
        coefs = pd.Series(
            data = model.coef_[0], 
            index = model.feature_names_in_
        )
    else:
        coefs = pd.Series()
    return coefs

# Standardized Coefficients
def std_coefs(model):
    model_type = str(type(model.model))
    X = pd.DataFrame(
        data = model.model.exog, 
        columns = model.model.exog_names
    )
    if 'OLS' in model_type:
        y = model.model.endog
        result = model.params * (X.std() / y.std())
    elif 'GLM' in model_type:
        y = 1
        result = model.params * (X.std() / 1)
    return result


# Metrics for Classification: Confusion Matrix, F1 Score
def clfmetrics(y_true, y_pred):
    print('▶ Confusion Matrix')
    print(
        confusion_matrix(
            y_true = y_true, 
            y_pred = y_pred
        )
    )
    
    print()
    
    print('▶ Classification Report')
    print(
        classification_report(
            y_true = y_true, 
            y_pred = y_pred, 
            digits = 4
        )
    )


# Classification metrics with Cutoff for Logistic Regression
# Plus, Matthew's Correlation coefficient
def clfCutoffs(y_true, y_prob):
    cutoffs = np.linspace(0, 1, 101)
    sens = []
    spec = []
    prec = []
    mccs = []
    
    for cutoff in cutoffs:
        pred = np.where(y_prob >= cutoff, 1, 0)
        clfr = classification_report(
            y_true = y_true, 
            y_pred = pred, 
            output_dict = True, 
            zero_division = True
        )
        sens.append(clfr['1']['recall'])
        spec.append(clfr['0']['recall'])
        prec.append(clfr['1']['precision'])
        
        mcc = matthews_corrcoef(
            y_true = y_true, 
            y_pred = pred
        )
        mccs.append(mcc)
        
    result = pd.DataFrame(
        data = {
            'Cutoff': cutoffs, 
            'Sensitivity': sens, 
            'Specificity': spec, 
            'Precision': prec, 
            'MCC': mccs
        }
    )
    
    # The Optimal Point is the sum of Sensitivity and Specificity.
    result['Optimal'] = result['Sensitivity'] + result['Specificity']
    
    # TPR and FPR for ROC Curve.
    result['TPR'] = result['Sensitivity']
    result['FPR'] = 1 - result['Specificity']
    
    # Set Column name.
    cols = ['Cutoff', 'Sensitivity', 'Specificity', 'Optimal', \
            'Precision', 'TPR', 'FPR', 'MCC']
    result = result[cols]
    return result

# Draw ROC Curve with Optimal Cutoff
def EpiROC(obj):
    
    # Draw ROC curve
    sns.lineplot(
        data = obj, 
        x = 'FPR', 
        y = 'TPR', 
        color = 'black'
    )
    plt.title(label = '최적의 분리 기준점 탐색')
    
    # Draw diagonal line
    plt.plot(
        [0, 1], 
        [0, 1], 
        color = '0.5', 
        ls = '--'
    )
    
    # Add the Optimal Point
    opt = obj.iloc[[obj['Optimal'].argmax()]]
    sns.scatterplot(
        data = opt, 
        x = 'FPR', 
        y = 'TPR', 
        color = 'red'
    )
    
    # Add tangent line
    optX = opt['FPR'].iloc[0]
    optY = opt['TPR'].iloc[0]
    
    # x1 = optX - 0.1
    # y1 = optY - 0.1
    # x2 = optX + 0.1
    # y2 = optY + 0.1
    # 
    # plt.plot(
    #     [x1, x2],
    #     [y1, y2],
    #     color = 'red',
    #     lw = 0.5,
    #     ls = '-.'
    # )
    
    b = optY - optX
    plt.plot(
        [0, 1-b], 
        [b, 1], 
        color = 'red', 
        lw = 0.5, 
        ls = '-.'
    )
    
    # Add text
    plt.text(
        x = opt['FPR'].values[0] - 0.01, 
        y = opt['TPR'].values[0] + 0.01, 
        s = f"Cutoff = {opt['Cutoff'].round(2).values[0]}", 
        ha = 'right', 
        va = 'bottom'
    );


## End of Document
