"""
task b (and task g): plot terrain, approximate terrain with OLS (own implementation and scikit) and calculate MSE, R2 &
                     beta over model complexity for real data. Performs task_b, so no resampling.
"""
# Our own library of functions
from utils import *
from Schedulers import *
from FFNN import FFNN
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import metrics


np.random.seed(42069)

cancer = datasets.load_breast_cancer()

X = cancer.data
z = cancer.target


X_train, X_test, z_train, z_test = train_test_split(X, z)

scaler = StandardScaler()
scaler.fit(X_train)

scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

X_train_sc = scaler.transform(X_train)
X_test_sc = scaler.transform(X_test)


# parameters
neural_dims = (30, 100, 1)
logreg_dims = (30, 1)
eta = 0.001
rho = 0.90
rho2 = 0.999
z_train = z_train.reshape(z_train.shape[0], 1)
z_test = z_test.reshape(z_test.shape[0], 1)
z = z.reshape(z.shape[0], 1)
batches = 10

neural = FFNN(neural_dims, hidden_func=RELU, output_func=sigmoid, cost_func=CostLogReg)
# neural = FFNN(logreg_dims, output_func=sigmoid, cost_func=CostLogReg)

momentum = 0.5

sched = RMS_prop
sched = Adam
# params = [eta, momentum]
# params = [eta]
params = [eta, rho, rho2]
# params = [eta]
# params = [eta, rho]
folds = 5

scores = neural.cross_val(
    folds,
    X,
    z,
    sched,
    *params,
    batches=batches,
    epochs=500,
    # lam=0.01,
    # X_test=X_test_sc,
    # t_test=z_test,
    use_best_weights=True
)
train_errors = scores["train_errors"]
test_errors = scores["test_errors"]
plt.plot(train_errors, label="train")
plt.plot(test_errors, label="test")
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("LogLoss")
plt.title("LogLoss over Epochs")
plt.show()

plot_confusion(scores["confusion"])
