import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score


def visualize_confusion_matrix(y_test, y_predict):
    """
    Visualization.
    
    :param y_test:variable 
    
    :param y_predict:variable 
    
    :return:chart 
    
    """
    confusion_matrix_ = confusion_matrix(y_test, y_predict)
    cm_display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix_, display_labels=[False, True])
    cm_display.plot()
    print({"Accuracy": accuracy_score(y_test, y_predict),
           "Precision": precision_score(y_test, y_predict),
           "Sensitivity_recall": recall_score(y_test, y_predict),
           "Specificity": recall_score(y_test, y_predict, pos_label=0),
           "F1_score": f1_score(y_test, y_predict)
           })
    plt.show()


def plot_roc_curve(true_y, y_prob):
    """
    Plot roc curve.

    :param true_y: variable

    :param y_prob: variable

    :return:AUC score and chart
    """
    fpr, tpr, thresholds = roc_curve(true_y, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()
    print(f"AUC score: {roc_auc_score(true_y, y_prob)}")