from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.lib import hub

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


class SimpleMonitor13(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self.monitor)

        # Train model at start
        self.flow_training()

    def monitor(self):
        while True:
            hub.sleep(10)

    # ================= ML TRAINING =================
    def flow_training(self):

        self.logger.info("Flow Training ...")

        flow_dataset = pd.read_csv('FlowStatsfile.csv')

        # ✅ Drop non-numeric / non-useful columns
        flow_dataset = flow_dataset.drop(columns=[
            flow_dataset.columns[2],  # flow_id
            flow_dataset.columns[3],  # ip_src
            flow_dataset.columns[5]   # ip_dst
        ])

        # Features & Labels
        X_flow = flow_dataset.iloc[:, :-1].values.astype('float64')
        y_flow = flow_dataset.iloc[:, -1].values

        # Train/Test split
        X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(
            X_flow, y_flow, test_size=0.25, random_state=0
        )

        # Model
        classifier = RandomForestClassifier(
            n_estimators=10, criterion="entropy", random_state=0
        )
        self.flow_model = classifier.fit(X_flow_train, y_flow_train)

        # Prediction
        y_flow_pred = self.flow_model.predict(X_flow_test)

        self.logger.info("------------------------------------------------------")
        self.logger.info("Confusion Matrix")
        cm = confusion_matrix(y_flow_test, y_flow_pred)
        self.logger.info(cm)

        acc = accuracy_score(y_flow_test, y_flow_pred)
        self.logger.info("Success Accuracy = {0:.2f}%".format(acc * 100))

        fail = 1.0 - acc
        self.logger.info("Fail Accuracy = {0:.2f}%".format(fail * 100))
        self.logger.info("------------------------------------------------------")

    # ================= PREDICTION =================
    def flow_predict(self):

        try:
            predict_flow_dataset = pd.read_csv('PredictFlowStatsfile.csv')

            # Same preprocessing as training
            predict_flow_dataset = predict_flow_dataset.drop(columns=[
                predict_flow_dataset.columns[2],
                predict_flow_dataset.columns[3],
                predict_flow_dataset.columns[5]
            ])

            X_predict_flow = predict_flow_dataset.values.astype('float64')

            y_flow_pred = self.flow_model.predict(X_predict_flow)

            legitimate_trafic = 0
            ddos_trafic = 0

            for i in y_flow_pred:
                if i == 0:
                    legitimate_trafic += 1
                else:
                    ddos_trafic += 1

            self.logger.info("------------------------------------------------------")

            if (legitimate_trafic / len(y_flow_pred) * 100) > 80:
                self.logger.info("Legitimate Traffic Detected")
            else:
                self.logger.info("DDoS Traffic Detected")

            self.logger.info("------------------------------------------------------")

        except Exception as e:
            self.logger.info("Prediction Error: {}".format(e))
