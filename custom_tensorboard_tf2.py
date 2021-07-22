import numpy as np
from tensorflow.keras.callbacks import TensorBoard


class AddTensorBoard(TensorBoard):
    """举例：添加 top3_val_acc to tensorboard"""

    def __init__(self, val_label_list, top=3):
        self.val_label_list = val_label_list
        self.top = top
        super().__init__()

    def on_epoch_end(self, epoch, logs=None):
        val_pred = self.model.predict(self.validation_data[0])
        temp = []
        for i in range(len(self.val_label_list)):
            if self.val_label_list[i] in np.argsort(val_pred[i])[-self.top:]:
                temp.append(1)
            else:
                temp.append(0)

        top3_val_acc = np.mean(temp)

        logs.update({'top3_val_acc': top3_val_acc})
        super().on_epoch_end(epoch, logs)
